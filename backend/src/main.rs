use axum::{
    extract::{Query, State},
    http::StatusCode,
    routing::get,
    Json, Router,
};
use bb8::Pool;
use bb8_postgres::PostgresConnectionManager;
use serde::{Deserialize, Serialize};
use std::net::SocketAddr;
use tokio_postgres::NoTls;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};
use utoipa::OpenApi;
use utoipa_swagger_ui::SwaggerUi;

#[derive(Deserialize, Debug)]
struct Config {
    dbhost: String,
    dbuser: String,
    dbpass: String,
    dbname: String,
}

#[derive(Serialize)]
struct StationDelay {
    name: String,
    train: String,
    avg_delay: f32,
}

#[derive(Deserialize)]
struct RequestDate {
    date: String,
}

#[derive(Deserialize)]
struct RequestTimeFrame {
    lower_limit: String,
    upper_limit: String,
}

#[derive(OpenApi)]
#[openapi(paths(
    using_connection_pool_extractor,
    get_station_delays,
    get_station_delays_date,
    get_station_delays_timeframe
))]
struct ApiDoc;

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

    // set up connection pool
    let psql_url = format!(
        "host={0} user={1} password={2} dbname={3}",
        config.dbhost, config.dbuser, config.dbpass, config.dbname,
    );
    let manager = PostgresConnectionManager::new_from_stringlike(psql_url, NoTls).unwrap();
    let pool = Pool::builder().build(manager).await.unwrap();

    // build our application with some routes
    let app = Router::new()
        .route("/", get(using_connection_pool_extractor))
        .route("/stations", get(get_station_delays))
        .route("/stations/date", get(get_station_delays_date))
        .route("/stations/timeframe", get(get_station_delays_timeframe))
        .with_state(pool)
        .merge(SwaggerUi::new("/docs").url("/docs/openapi.json", ApiDoc::openapi()));
    // run it with hyper
    let addr = SocketAddr::from(([127, 0, 0, 1], 3000));
    tracing::debug!("listening on {}", addr);
    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .await
        .unwrap();
}

type ConnectionPool = Pool<PostgresConnectionManager<NoTls>>;

#[utoipa::path(
    get,
    path = "/",
    responses(
        (status = 200, description = "Return first row first string of station_delay")
        )
    )]
async fn using_connection_pool_extractor(
    State(pool): State<ConnectionPool>,
) -> Result<String, (StatusCode, String)> {
    let conn = pool.get().await.map_err(internal_error)?;

    let row = conn
        .query("select * from station_delay", &[])
        .await
        .map_err(internal_error)?;
    let two: String = row[0].try_get(0).map_err(internal_error)?;

    Ok(two.to_string())
}

#[utoipa::path(
    get,
    path = "/stations",
    responses(
        (status = 200, description = "Returns delay average of all trips stored in database")
        )
    )]
async fn get_station_delays(
    State(pool): State<ConnectionPool>,
) -> Result<Json<Vec<StationDelay>>, (StatusCode, String)> {
    let conn = pool.get().await.map_err(internal_error)?;
    let query_string = "select name, transportation_name, avg(delay)::real 
            from station_delay 
            group by name, transportation_name;";

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
        (status = 200, description = "Returns delay averages for given day")
        ),
    params(("date" = String, Query, description = "Date string like YYYY-MM-DD"))
    )]
async fn get_station_delays_date(
    State(pool): State<ConnectionPool>,
    request_date: Query<RequestDate>,
) -> Result<Json<Vec<StationDelay>>, (StatusCode, String)> {
    let conn = pool.get().await.map_err(internal_error)?;

    let query_string = format!(
        "select name, transportation_name, avg(delay)::real 
        from station_delay 
        where departureTimePlanned::date = '{}' 
        group by name, transportation_name;",
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
        (status = 200, description = "Returns delay averages in given timeframe")
        ),
    params(("lower_limit" = String, Query, description = "Timestamp string like 'YYYY-MM-DD hh:mm:ss'"),
    ("upper_limit" = String, Query, description = "Timestamp string like 'YYYY-MM-DD hh:mm:ss'"))
    )]
async fn get_station_delays_timeframe(
    State(pool): State<ConnectionPool>,
    request_frame: Query<RequestTimeFrame>,
) -> Result<Json<Vec<StationDelay>>, (StatusCode, String)> {
    let conn = pool.get().await.map_err(internal_error)?;

    let query_string = format!(
        "select tmp.name, tmp.transportation_name, avg(tmp.delay)::real 
        from (
            select * 
            from station_delay
            where departureTimePlanned > '{0}' and departureTimePlanned <= '{1}'
            ) as tmp
        group by name, transportation_name;",
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
fn internal_error<E>(err: E) -> (StatusCode, String)
where
    E: std::error::Error,
{
    (StatusCode::INTERNAL_SERVER_ERROR, err.to_string())
}
