use serde::{Deserialize, Serialize};
use time::Date;
use utoipa::{IntoParams, ToSchema};

#[derive(Deserialize, Debug)]
pub struct Config {
    pub dbhost: String,
    pub dbuser: String,
    pub dbpass: String,
    pub dbname: String,
}

#[derive(Serialize, ToSchema)]
pub struct LineDelay {
    pub line: String,
    pub avg_delay: f32,
}

#[derive(Serialize, ToSchema)]
pub struct StationDelay {
    pub name: String,
    pub line: String,
    pub avg_delay: f32,
}

#[derive(Serialize, ToSchema)]
pub struct StationInfo {
    pub name: String,
    pub short: String,
    pub long: String,
    pub date: Date,
}

#[derive(Serialize, ToSchema)]
pub struct Incident {
    pub station: String,
    pub line: String,
    pub train_number: i32,
    pub incident: String,
    pub date: Date,
}
#[derive(Serialize, ToSchema)]
pub struct JsonError {
    pub status: String,
    pub message: String,
}

#[derive(Deserialize, IntoParams)]
pub struct RequestDate {
    pub date: String,
}

#[derive(Deserialize, IntoParams)]
pub struct RequestTimeFrame {
    pub lower_limit: String,
    pub upper_limit: String,
}
