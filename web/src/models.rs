#[derive(sqlx::FromRow)]
pub struct StationDelay {
    pub stop_name: String,
    pub delay: f32,
}

#[derive(sqlx::FromRow)]
pub struct LineDelay {
    pub name: String,
    pub delay: f32,
}
