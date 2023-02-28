# vvs-mining backend

This backend is written in Rust. You will need to set some environment variables before running it with `cargo`.

Variables:
```
DBHOST=<host of postgres database>
DBNAME=<name of the database inside postgres>
DBUSER=<username of postgres user>
DBPASS=<password of postgres user>
```

You can then start the API backend with `cargo run`. Setting up the environment and running the application can also be combined:
```
DBHOST=10.0.1.37 DBUSER=admin DBPASS=admin DBNAME=data cargo run
```

The instance will be running on `localhost:3000`. There is documentation on the API available at `localhost:3000/docs`.
