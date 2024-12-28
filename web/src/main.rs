use std::env;

use anyhow::Context;
use sqlx::postgres::PgPoolOptions;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "vvs_mining_web=debug".into()),
        )
        .with(tracing_subscriber::fmt::layer())
        .init();
    let database_url = env::var("DATABASE_URL")
        // The error from `var()` doesn't mention the environment variable.
        .context("DATABASE_URL must be set")?;

    let db = PgPoolOptions::new()
        .max_connections(20)
        .connect(&database_url)
        .await
        .context("failed to connect to DATABASE_URL")?;

    tracing::debug!("Running database migrations");
    sqlx::migrate!().run(&db).await?;
    tracing::debug!("Ran migrations successfully");

    web::serve(db).await
}
