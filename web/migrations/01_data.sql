CREATE TABLE IF NOT EXISTS public.station_delay (
    stop_name text,
    line_number text,
    departure_planned timestamp without time zone,
    departure_estimated timestamp without time zone,
    delay integer
);
