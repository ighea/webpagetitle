# webpagetitle - retrieve remote web page´s title

A microservice for retrieving web page title contents. Uses selenium with Firefox to render pages. Fallbacks to basic dom manipulation if selenium does not provide reasonable results (request timeouts or throws exceptions).

## build image

```
docker build -t webpagetitle .
```

## run server

Run the container, expose internal port 9999 as external 9999 and bind to host 0.0.0.0 for listening for all connections.

```
docker run -p 9999:9999 webpagetitle --port 9999 --host=0.0.0.0
```

## usage with curl
```
curl -d "url=https://google.com" -H "Content-Type: application/x-www-form-urlencoded" -X POST http://localhost:9999/
```
