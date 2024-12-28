use askama::Template;

use crate::models::{LineDelay, StationDelay};

#[derive(Template)]
#[template(path = "main.html")]
pub struct MainTemplate {
    pub stations: Vec<StationDelay>,
    pub lines: Vec<LineDelay>,
}
