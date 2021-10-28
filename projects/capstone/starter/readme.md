




## API documentation

```
Endpoints:
GET      '/tickers'
GET      '/prices'
POST     '/tickers'
POST     '/prices'
PATCH    '/tickers/<int:ticker_id>'
PATCH    '/prices/<int:price_id>'
DELETE   '/tickers/<int:ticker_id>'
DELETE   '/prices/<int:price_id>'



GET '/tickers'
coil@coil-VM:~/Desktop$ curl http://127.0.0.1:5000/tickers
{"success":true,"tickers":[{"description":"pretty cool company","id":1,"industry":"consumer electronics","name":"Apple","symbol":"AAPL"}],"total_elements":1}



GET '/prices'
coil@coil-VM:~/Desktop$ curl http://127.0.0.1:5000/prices
{"data":[{"date":"2021-10-20","id":1,"price":1,"ticker_id":"1"}],"success":true,"total_elements":1}
coil@coil-VM:~/Desktop$ 





POST '/tickers'

coil@coil-VM:~/Desktop$ curl -X POST -H "Content-Type: application/json" -d '{"symbol":"AAPL", "name": "Apple", "industry": "consumer electronics", "description": "one of FAANG companies"}' http://127.0.0.1:5000/tickers
{"created":1,"success":true,"tickers":[{"description":"one of FAANG companies","id":1,"industry":"consumer electronics","name":"Apple","symbol":"AAPL"}],"total_tickers":1}
coil@coil-VM:~/Desktop$ 


POST '/prices'

coil@coil-VM:~/Desktop$ curl -X POST -H "Content-Type: application/json" -d '{"date":"2021-10-20", "price": "150", "ticker_id": "1"}' http://127.0.0.1:5000/prices
{"created":1,"data":[{"date":"2021-10-20","id":1,"price":150,"ticker_id":"1"}],"success":true,"total_elements":1}
coil@coil-VM:~/Desktop$ 






PATCH    '/tickers/<int:ticker_id>'

coil@coil-VM:~/Desktop$ curl -X PATCH -H "Content-Type: application/json" -d '{"description": "pretty cool company"}' http://127.0.0.1:5000/tickers/1
{"success":true}
coil@coil-VM:~/Desktop$ 



PATCH    '/prices/<int:price_id>'

coil@coil-VM:~/Desktop$ curl -X PATCH -H "Content-Type: application/json" -d '{"price": "1"}' http://127.0.0.1:5000/prices/1
{"success":true}
coil@coil-VM:~/Desktop$ 






DELETE   '/tickers/<int:ticker_id>'
coil@coil-VM:~/Desktop$ curl -X DELETE http://127.0.0.1:5000/tickers/1
{"deleted":1,"success":true,"tickers":[],"total_elements":0}






DELETE   '/prices/<int:price_id>'
coil@coil-VM:~/Desktop$ curl -X DELETE http://127.0.0.1:5000/prices/1
{"data":[],"deleted":1,"success":true,"total_elements":0}







```











## Sources:

install dotenv library
https://pypi.org/project/python-dotenv/

bad json in tests
https://stackoverflow.com/questions/16573332/jsondecodeerror-expecting-value-line-1-column-1-char-0








