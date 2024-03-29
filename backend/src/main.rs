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
        get_station_delays_prime,
        get_line_delays,
        get_line_delays_date,
        get_line_delays_timeframe,
        get_line_delays_prime,
        get_station_infos,
        get_station_infos_date,
        get_station_infos_timeframe,
    ),
    components(schemas(StationDelay, StationInfo, LineDelay, JsonError))
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
        .route("/stations/prime", get(get_station_delays_prime))
        .route("/lines", get(get_line_delays))
        .route("/lines/date", get(get_line_delays_date))
        .route("/lines/timeframe", get(get_line_delays_timeframe))
        .route("/lines/prime", get(get_line_delays_prime))
        .route("/infos", get(get_station_infos))
        .route("/infos/date", get(get_station_infos_date))
        .route("/infos/timeframe", get(get_station_infos_timeframe))
        .route("/incidents", get(get_incidents))
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
    path = "/api/v1/lines/date",
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
    path = "/api/v1/lines/timeframe",
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
    path = "/api/v1/lines/prime",
    responses(
        (status = 200, description = "Returns delay averages in prime timeframe (06:00-09:00 and 16:00-19:00, Mon-Fri)",
         body = [StationDelay], content_type = "application/json"), 
        (status = 500, description = "Server error",
         body = JsonError, content_type = "application/json")
        ),
    )
    ]
async fn get_line_delays_prime(
    State(pool): State<ConnectionPool>,
) -> Result<Json<Vec<LineDelay>>, Json<JsonError>> {
    let conn = pool.get().await.map_err(internal_error)?;

    let query_string = "select split_part(transportation_name, ' ', 2), avg(delay)::real
        from station_delay
        where ((departureTimePlanned::time > '06:00:00' and departureTimePlanned::time < '09:00:00') or 
	    (departureTimePlanned::time > '16:00:00' and departureTimePlanned::time < '19:00:00')) 
	    and (EXTRACT(DOW FROM departureTimePlanned) > 0 and EXTRACT(DOW FROM departureTimePlanned) < 6)
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
    path = "/api/v1/stations",
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
            line: row.try_get(1).map_err(internal_error)?,
            avg_delay: row.try_get(2).map_err(internal_error)?,
        };
        result.push(x);
    }
    Ok(Json(result))
}

#[utoipa::path(
    get,
    path = "/api/v1/stations/date",
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
            line: row.try_get(1).map_err(internal_error)?,
            avg_delay: row.try_get(2).map_err(internal_error)?,
        };
        result.push(x);
    }
    Ok(Json(result))
}

#[utoipa::path(
    get,
    path = "/api/v1/stations/timeframe",
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
            line: row.try_get(1).map_err(internal_error)?,
            avg_delay: row.try_get(2).map_err(internal_error)?,
        };
        result.push(x);
    }
    Ok(Json(result))
}

#[utoipa::path(
    get,
    path = "/api/v1/stations/prime",
    responses(
        (status = 200, description = "Returns delay averages in prime timeframe (06:00-09:00 and 16:00-19:00, Mon-Fri)",
         body = [StationDelay], content_type = "application/json"), 
        (status = 500, description = "Server error",
         body = JsonError, content_type = "application/json")
        ),
    )]
async fn get_station_delays_prime(
    State(pool): State<ConnectionPool>,
) -> Result<Json<Vec<StationDelay>>, Json<JsonError>> {
    let conn = pool.get().await.map_err(internal_error)?;

    let query_string = "select name, split_part(transportation_name, ' ', 2), avg(delay)::real
            from station_delay
            where ((departureTimePlanned::time > '06:00:00' and departureTimePlanned::time < '09:00:00')
	            or (departureTimePlanned::time > '16:00:00' and departureTimePlanned::time < '19:00:00'))
	            and (EXTRACT(DOW FROM departureTimePlanned) > 0 and EXTRACT(DOW FROM departureTimePlanned) < 6)
            group by name, split_part(transportation_name, ' ', 2);";
    let rows = conn
        .query(query_string, &[])
        .await
        .map_err(internal_error)?;

    let mut result = vec![];
    for row in rows {
        let x = StationDelay {
            name: row.try_get(0).map_err(internal_error)?,
            line: row.try_get(1).map_err(internal_error)?,
            avg_delay: row.try_get(2).map_err(internal_error)?,
        };
        result.push(x);
    }
    Ok(Json(result))
}

#[utoipa::path(
    get,
    path = "/api/v1/infos",
    responses(
        (status = 200, description = "Returns all information about all stations stored in database", 
         body = [StationInfo], content_type = "application/json"),
        (status = 500, description = "Server error",
         body = JsonError, content_type = "application/json")
        )
    )]
async fn get_station_infos(
    State(pool): State<ConnectionPool>,
) -> Result<Json<Vec<StationInfo>>, Json<JsonError>> {
    let conn = pool.get().await.map_err(internal_error)?;
    let query_string = "select name, urlText, content, date::Date from station_info group by (name, urlText, content, date::date);";

    let rows = conn
        .query(query_string, &[])
        .await
        .map_err(internal_error)?;

    let mut result = vec![];
    for row in rows {
        let x = StationInfo {
            name: row.try_get(0).map_err(internal_error)?,
            short: row.try_get(1).map_err(internal_error)?,
            long: row.try_get(2).map_err(internal_error)?,
            date: row.try_get(3).map_err(internal_error)?,
        };
        result.push(x);
    }
    Ok(Json(result))
}

#[utoipa::path(
    get,
    path = "/api/v1/infos/date",
    responses(
        (status = 200, description = "Returns all information about all stations at given date stored in database", 
         body = [StationInfo], content_type = "application/json"),
        (status = 500, description = "Server error",
         body = JsonError, content_type = "application/json")
        ),
    params(("date" = String, Query, description = "Date string like YYYY-MM-DD"))
    )]
async fn get_station_infos_date(
    State(pool): State<ConnectionPool>,
    request_date: Query<RequestDate>,
) -> Result<Json<Vec<StationInfo>>, Json<JsonError>> {
    let conn = pool.get().await.map_err(internal_error)?;
    let query_string = format!(
        "select name, urlText, content, date::Date from station_info
        where date::date = '{}'
        group by (name, urlText, content, date::date);",
        request_date.date
    );

    let rows = conn
        .query(&query_string, &[])
        .await
        .map_err(internal_error)?;

    let mut result = vec![];
    for row in rows {
        let x = StationInfo {
            name: row.try_get(0).map_err(internal_error)?,
            short: row.try_get(1).map_err(internal_error)?,
            long: row.try_get(2).map_err(internal_error)?,
            date: row.try_get(3).map_err(internal_error)?,
        };
        result.push(x);
    }
    Ok(Json(result))
}

#[utoipa::path(
    get,
    path = "/api/v1/infos/timeframe",
    responses(
        (status = 200, description = "Returns all information about all stations at given date stored in database", 
         body = [StationInfo], content_type = "application/json"),
        (status = 500, description = "Server error",
         body = JsonError, content_type = "application/json")
        ),
    params(("lower_limit" = String, Query, description = "Timestamp string like 'YYYY-MM-DD hh:mm:ss'"),
        ("upper_limit" = String, Query, description = "Timestamp string like 'YYYY-MM-DD hh:mm:ss'")
        )
    )]
async fn get_station_infos_timeframe(
    State(pool): State<ConnectionPool>,
    request_timeframe: Query<RequestTimeFrame>,
) -> Result<Json<Vec<StationInfo>>, Json<JsonError>> {
    let conn = pool.get().await.map_err(internal_error)?;
    let query_string = format!(
        "select name, urlText, content, date::Date from station_info
        where date::date > '{0}' and date::date <= '{1}'
        group by (name, urlText, content, date::date);",
        request_timeframe.lower_limit, request_timeframe.upper_limit
    );

    let rows = conn
        .query(&query_string, &[])
        .await
        .map_err(internal_error)?;

    let mut result = vec![];
    for row in rows {
        let x = StationInfo {
            name: row.try_get(0).map_err(internal_error)?,
            short: row.try_get(1).map_err(internal_error)?,
            long: row.try_get(2).map_err(internal_error)?,
            date: row.try_get(3).map_err(internal_error)?,
        };
        result.push(x);
    }
    Ok(Json(result))
}

#[utoipa::path(
    get,
    path = "/api/v1/incidents",
    responses(
        (status = 200, description = "Returns all information about all stations stored in database", 
         body = [StationInfo], content_type = "application/json"),
        (status = 500, description = "Server error",
         body = JsonError, content_type = "application/json")
        ),
    params(("date" = String, Query, description = "Date string like 'YYYY-MM-DD'"),
        ("line" = String, Query, description = "Line name formatted like 'S1' or 'MEX19'"))
    )]
async fn get_incidents(
    State(pool): State<ConnectionPool>,
    request_date: Query<RequestDate>,
    request_line: Query<RequestLine>,
) -> Result<Json<Vec<Incident>>, Json<JsonError>> {
    let conn = pool.get().await.map_err(internal_error)?;
    let query_string = format!("select name, split_part(transportation_name, ' ', 2), transportation_properties_trainnumber, content, date::date
                                from train_incident
                                where date::date = '{0}' and split_part(transportation_name, ' ', 2) = '{1}';", request_date.date, request_line.line);
    let rows = conn
        .query(&query_string, &[])
        .await
        .map_err(internal_error)?;

    let mut result = vec![];
    for row in rows {
        let x = Incident {
            station: row.try_get(0).map_err(internal_error)?,
            line: row.try_get(1).map_err(internal_error)?,
            train_number: row.try_get(2).map_err(internal_error)?,
            incident: row.try_get(3).map_err(internal_error)?,
            date: row.try_get(4).map_err(internal_error)?,
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
