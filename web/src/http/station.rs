use askama::Template;
use axum::{routing::get, Router};

#[derive(Template)]
#[template(path = "station.html")]
struct StationTemplate {
    stations: Vec<(String, f32)>,
}

async fn station_delay() -> StationTemplate {
    StationTemplate {
        stations: vec![("test".to_string(), 0.3)],
    }
}

pub(crate) fn router() -> Router {
    Router::new().route("/", get(station_delay))
}
