use anyhow::Context;
use axum::{Extension, Router};
use sqlx::PgPool;

mod station;

pub fn app(db: PgPool) -> Router {
    Router::new().merge(station::router()).layer(Extension(db))
}

pub async fn serve(db: PgPool) -> anyhow::Result<()> {
    let listener = tokio::net::TcpListener::bind("::0:3000").await?;
    axum::serve(listener, app(db))
        .await
        .context("failed to serve API")
}
