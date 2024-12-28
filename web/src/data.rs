use sqlx::PgPool;

use crate::models;

pub async fn get_stations(pool: &PgPool) -> Vec<models::StationDelay> {
    let sql = "SELECT stop_name, avg(delay)::real as delay FROM station_delay GROUP BY stop_name ORDER BY delay DESC LIMIT 5"
        .to_string();
    sqlx::query_as::<_, models::StationDelay>(&sql)
        .fetch_all(pool)
        .await
        .unwrap()
}

pub async fn get_lines(pool: &PgPool) -> Vec<models::LineDelay> {
    let sql = "SELECT line_number as name, avg(delay)::real as delay FROM station_delay GROUP BY line_number ORDER BY delay DESC LIMIT 5"
        .to_string();
    sqlx::query_as::<_, models::LineDelay>(&sql)
        .fetch_all(pool)
        .await
        .unwrap()
}
