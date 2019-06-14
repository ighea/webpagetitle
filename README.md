# webpagetitle - retrieve remote web page´s title

A microservice for retrieving web page title contents. Uses selenium with Firefox to render page. Fallbacks to basic dom manipulation if selenium does not provide reasonable results (request timeouts or throws exceptions).

## usage with curl
curl -d "url=https://google.com" -H "Content-Type: application/x-www-form-urlencoded" -X POST http://localhost:9999/
