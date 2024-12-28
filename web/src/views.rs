use axum::{routing::get, Extension, Router};
use sqlx::PgPool;

use crate::{
    data,
    templates::{self, MainTemplate},
};

pub fn app(db: PgPool) -> Router {
    Router::new()
        .route("/", get(main_page))
        .layer(Extension(db))
}

async fn main_page(Extension(pool): Extension<PgPool>) -> templates::MainTemplate {
    let stations = data::get_stations(&pool).await;
    let lines = data::get_lines(&pool).await;
    MainTemplate { stations, lines }
}
