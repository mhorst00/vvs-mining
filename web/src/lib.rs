use anyhow::Context;
use sqlx::PgPool;

pub mod data;
pub mod models;
pub mod templates;
pub mod views;

pub async fn serve(db: PgPool) -> anyhow::Result<()> {
    let listener = tokio::net::TcpListener::bind("::0:3000").await?;
    axum::serve(listener, views::app(db))
        .await
        .context("failed to serve API")
}
