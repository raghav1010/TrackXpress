

## Running

First fork the repo then do a `git clone`.

    git clone https://github.com/<yournamehere>/TrackXpress.git

You should also have [docker](https://docs.docker.com/install/). If you're on linux, you probably also want docker-compose. Last I checked (over a year ago) it did not come with docker by default. For Mac and Windows you get it with the default installation.

Once you have all of that, you should be good. No need to install [Postgres](https://www.postgresql.org/) or even Python.

```
docker-compose build --no-cache  # Build the containers

docker-compose up # Run the app

```

For running UTs:

```
docker exec app_track_xpress python -m unittest discover
```

For Github-Actions:

```
Whenever making a pull request to feature branch or main branch, the build and tests would run as part of actions.
```