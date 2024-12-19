use askama::Template;
use axum::{routing::get, Extension, Router};
use sqlx::PgPool;

#[derive(Template)]
#[template(path = "station.html")]
struct StationTemplate {
    stations: Vec<StationDelay>,
}

#[derive(sqlx::FromRow)]
pub struct StationDelay {
    pub stop_name: String,
    pub delay: f32,
}

async fn station_delay(Extension(pool): Extension<PgPool>) -> StationTemplate {
    let sql = "SELECT stop_name, avg(delay)::real as delay FROM station_delay GROUP BY stop_name ORDER BY delay DESC LIMIT 5"
        .to_string();
    let stations = sqlx::query_as::<_, StationDelay>(&sql)
        .fetch_all(&pool)
        .await
        .unwrap();
    StationTemplate { stations }
}

pub(crate) fn router() -> Router {
    Router::new().route("/", get(station_delay))
}
