mod models;
use models::*;

use axum::{
    extract::{Query, State},
    http::{Method, StatusCode},
    routing::get,
    Json, Router,
};
use bb8::Pool;
use bb8_postgres::PostgresConnectionManager;
use std::net::SocketAddr;
use tokio::signal;
use tokio_postgres::NoTls;
use tower_http::cors::{Any, CorsLayer};
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};
use utoipa::OpenApi;
use utoipa_swagger_ui::SwaggerUi;

#[derive(OpenApi)]
#[openapi(
    paths(
        get_station_delays,
        get_station_delays_date,
        get_station_delays_timeframe,
        get_line_delays,
        get_line_delays_date,
        get_line_delays_timeframe
    ),
    components(schemas(StationDelay, LineDelay, JsonError))
)]
struct ApiDoc;

type ConnectionPool = Pool<PostgresConnectionManager<NoTls>>;

#[tokio::main]
async fn main() {
    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "backend=debug".into()),
        )
        .with(tracing_subscriber::fmt::layer())
        .init();

    // get env config
    let config = envy::from_env::<Config>().expect("Please provide all env vars");

    // setup cors
    let cors = CorsLayer::new()
        .allow_methods(Method::GET)
        .allow_origin(Any);

    // set up connection pool
    let psql_url = format!(
        "host={0} user={1} password={2} dbname={3}",
        config.dbhost, config.dbuser, config.dbpass, config.dbname,
    );
    let manager = PostgresConnectionManager::new_from_stringlike(psql_url, NoTls).unwrap();
    let pool = Pool::builder().build(manager).await.unwrap();

    // build our application with some routes
    let app = Router::new()
        .route("/stations", get(get_station_delays))
        .route("/stations/date", get(get_station_delays_date))
        .route("/stations/timeframe", get(get_station_delays_timeframe))
        .route("/lines", get(get_line_delays))
        .route("/lines/date", get(get_line_delays_date))
        .route("/lines/timeframe", get(get_line_delays_timeframe))
        .with_state(pool)
        .layer(cors)
        .merge(SwaggerUi::new("/docs").url("/docs/openapi.json", ApiDoc::openapi()));
    // run it with hyper
    let addr = SocketAddr::from(([0, 0, 0, 0], 3000));
    tracing::debug!("listening on http://{}", addr);
    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .with_graceful_shutdown(shutdown_signal())
        .await
        .unwrap();
}

async fn shutdown_signal() {
    let ctrl_c = async {
        signal::ctrl_c()
            .await
            .expect("failed to install Ctrl+C handler");
    };

    #[cfg(unix)]
    let terminate = async {
        signal::unix::signal(signal::unix::SignalKind::terminate())
            .expect("failed to install signal handler")
            .recv()
            .await;
    };

    #[cfg(not(unix))]
    let terminate = std::future::pending::<()>();

    tokio::select! {
        _ = ctrl_c => {},
        _ = terminate => {},
    }

    println!("signal received, starting graceful shutdown");
}

#[utoipa::path(
    get,
    path = "/lines",
    responses(
        (status = 200, description = "Get average delay of all lines in database",
         body = [LineDelay], content_type = "application/json"),
        (status = 500, description = "Server error",
         body = JsonError, content_type = "application/json")
        )
    )]
#[axum_macros::debug_handler]
async fn get_line_delays(
    State(pool): State<ConnectionPool>,
) -> Result<Json<Vec<LineDelay>>, Json<JsonError>> {
    let conn = pool.get().await.map_err(internal_error)?;
    let query_string = "select split_part(transportation_name, ' ', 2), avg(delay)::real
                        from station_delay
                        group by split_part(transportation_name, ' ', 2);";

    let rows = conn
        .query(query_string, &[])
        .await
        .map_err(internal_error)?;

    let mut result = vec![];
    for row in rows {
        let x = LineDelay {
            line: row.try_get(0).map_err(internal_error)?,
            avg_delay: row.try_get(1).map_err(internal_error)?,
        };
        result.push(x);
    }
    Ok(Json(result))
}

#[utoipa::path(
    get,
    path = "/lines/date",
    responses(
        (status = 200, description = "Get average delay of all lines on specific date in database",
         body = [LineDelay], content_type = "application/json"),
        (status = 500, description = "Server error",
         body = JsonError, content_type = "application/json")
        ),
    params(("date" = String, Query, description = "Date string like YYYY-MM-DD"))
    )]
async fn get_line_delays_date(
    State(pool): State<ConnectionPool>,
    request_date: Query<RequestDate>,
) -> Result<Json<Vec<LineDelay>>, Json<JsonError>> {
    let conn = pool.get().await.map_err(internal_error)?;
    let query_string = format!(
        "select split_part(transportation_name, ' ', 2), avg(delay)::real
        from station_delay
        where departureTimePlanned::date = '{}'
        group by split_part(transportation_name, ' ', 2);",
        request_date.date
    );

    let rows = conn
        .query(&query_string, &[])
        .await
        .map_err(internal_error)?;

    let mut result = vec![];
    for row in rows {
        let x = LineDelay {
            line: row.try_get(0).map_err(internal_error)?,
            avg_delay: row.try_get(1).map_err(internal_error)?,
        };
        result.push(x);
    }
    Ok(Json(result))
}

#[utoipa::path(
    get,
    path = "/lines/timeframe",
    responses(
        (status = 200, description = "Get average delay of all lines in specific timeframe in database",
         body = [LineDelay], content_type = "application/json"),
        (status = 500, description = "Server error",
         body = JsonError, content_type = "application/json")
    ),
    params(
        ("lower_limit" = String, Query, description = "Timestamp string like 'YYYY-MM-DD hh:mm:ss'"),
        ("upper_limit" = String, Query, description = "Timestamp string like 'YYYY-MM-DD hh:mm:ss'")
    )
)]
async fn get_line_delays_timeframe(
    State(pool): State<ConnectionPool>,
    request_frame: Query<RequestTimeFrame>,
) -> Result<Json<Vec<LineDelay>>, Json<JsonError>> {
    let conn = pool.get().await.map_err(internal_error)?;
    let query_string = format!(
        "select split_part(transportation_name, ' ', 2), avg(delay)::real
        from station_delay
        where departureTimePlanned > '{0}' and departureTimePlanned <= '{1}'
        group by split_part(transportation_name, ' ', 2);",
        request_frame.lower_limit, request_frame.upper_limit
    );

    let rows = conn
        .query(&query_string, &[])
        .await
        .map_err(internal_error)?;

    let mut result = vec![];
    for row in rows {
        let x = LineDelay {
            line: row.try_get(0).map_err(internal_error)?,
            avg_delay: row.try_get(1).map_err(internal_error)?,
        };
        result.push(x);
    }
    Ok(Json(result))
}

#[utoipa::path(
    get,
    path = "/stations",
    responses(
        (status = 200, description = "Returns delay average of all trains at all stations stored in database", 
         body = [LineDelay], content_type = "application/json"),
        (status = 500, description = "Server error",
         body = JsonError, content_type = "application/json")
        )
    )]
async fn get_station_delays(
    State(pool): State<ConnectionPool>,
) -> Result<Json<Vec<StationDelay>>, Json<JsonError>> {
    let conn = pool.get().await.map_err(internal_error)?;
    let query_string = "select name, split_part(transportation_name, ' ', 2), avg(delay)::real 
            from station_delay 
            group by name, split_part(transportation_name, ' ', 2);";

    let rows = conn
        .query(query_string, &[])
        .await
        .map_err(internal_error)?;

    let mut result = vec![];
    for row in rows {
        let x = StationDelay {
            name: row.try_get(0).map_err(internal_error)?,
            train: row.try_get(1).map_err(internal_error)?,
            avg_delay: row.try_get(2).map_err(internal_error)?,
        };
        result.push(x);
    }
    Ok(Json(result))
}

#[utoipa::path(
    get,
    path = "/stations/date",
    responses(
        (status = 200, description = "Returns delay averages for given day",
         body = [StationDelay], content_type = "application/json"),
        (status = 500, description = "Server error",
         body = JsonError, content_type = "application/json")
        ),
    params(("date" = String, Query, description = "Date string like YYYY-MM-DD"))
    )]
async fn get_station_delays_date(
    State(pool): State<ConnectionPool>,
    request_date: Query<RequestDate>,
) -> Result<Json<Vec<StationDelay>>, Json<JsonError>> {
    let conn = pool.get().await.map_err(internal_error)?;

    let query_string = format!(
        "select name, split_part(transportation_name, ' ', 2), avg(delay)::real 
        from station_delay 
        where departureTimePlanned::date = '{}' 
        group by name, split_part(transportation_name, ' ', 2);",
        request_date.date
    );

    let rows = conn
        .query(&query_string, &[])
        .await
        .map_err(internal_error)?;

    let mut result = vec![];
    for row in rows {
        let x = StationDelay {
            name: row.try_get(0).map_err(internal_error)?,
            train: row.try_get(1).map_err(internal_error)?,
            avg_delay: row.try_get(2).map_err(internal_error)?,
        };
        result.push(x);
    }
    Ok(Json(result))
}

#[utoipa::path(
    get,
    path = "/stations/timeframe",
    responses(
        (status = 200, description = "Returns delay averages in given timeframe",
         body = [StationDelay], content_type = "application/json"), 
        (status = 500, description = "Server error",
         body = JsonError, content_type = "application/json")
        ),
    params(("lower_limit" = String, Query, description = "Timestamp string like 'YYYY-MM-DD hh:mm:ss'"),
    ("upper_limit" = String, Query, description = "Timestamp string like 'YYYY-MM-DD hh:mm:ss'"))
    )]
async fn get_station_delays_timeframe(
    State(pool): State<ConnectionPool>,
    request_frame: Query<RequestTimeFrame>,
) -> Result<Json<Vec<StationDelay>>, Json<JsonError>> {
    let conn = pool.get().await.map_err(internal_error)?;

    let query_string = format!(
        "select name, split_part(transportation_name, ' ', 2), avg(delay)::real 
        from station_delay
        where departureTimePlanned > '{0}' and departureTimePlanned <= '{1}'
        group by name, split_part(transportation_name, ' ', 2);",
        request_frame.lower_limit, request_frame.upper_limit
    );

    let rows = conn
        .query(&query_string, &[])
        .await
        .map_err(internal_error)?;

    let mut result = vec![];
    for row in rows {
        let x = StationDelay {
            name: row.try_get(0).map_err(internal_error)?,
            train: row.try_get(1).map_err(internal_error)?,
            avg_delay: row.try_get(2).map_err(internal_error)?,
        };
        result.push(x);
    }
    Ok(Json(result))
}

/// Utility function for mapping any error into a `500 Internal Server Error`
/// response.
fn internal_error<E>(err: E) -> Json<JsonError>
where
    E: std::error::Error,
{
    let error = JsonError {
        status: StatusCode::INTERNAL_SERVER_ERROR.to_string(),
        message: err.to_string(),
    };
    Json(error)
}
