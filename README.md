# Chompy

**Download and watch videos easily on iOS**

Chompy wraps [youtube-dl](https://youtube-dl.org/) in an API, allowing downloads on devices that
can't run youtube-dl directly, such as iOS.

## Usage

Deploy me via Docker

Look at `/docs` for API definition

## Development

Run locally
```
poetry install
poetry shell
uvicorn chompy:app --reload
```

Download something

```
http -v localhost:8000/download url=="https://www.youtube.com/watch?v=zW_DDebgIC4"

http -v localhost:8000/videos path=="downloads/If Pokedex Entries Were Literal (Volume 20).mp4"
```

Run with docker

```
docker build -t chompy .

docker run -p 8000:8000 chompy
```
