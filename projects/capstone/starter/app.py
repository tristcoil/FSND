import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Ticker, Data



def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  return app

#APP = create_app()
app = create_app()


# ---------- GET ----------

@app.route("/public", methods=["GET"])
def public_endpoint():

    return jsonify({
                      "message": "public endpoint",
                  })



@app.route("/tickers", methods=["GET"])
def retrieve_tickers():
    #try:
    selection = Ticker.query.order_by(Ticker.id).all()
    tickers = [ ticker.format() for ticker in selection ]
    
    if len(tickers) == 0:
        abort(404)


    return jsonify(
                    {
                      "success": True,
                      "tickers": tickers,
                      "total_elements": len(Ticker.query.all())
                    }
                  )




@app.route("/prices", methods=["GET"])
def retrieve_prices():
    #try:
    selection = Data.query.order_by(Data.id).all()
    data_list = [ data.format() for data in selection ]
    
    if len(data_list) == 0:
        abort(404)


    return jsonify(
                    {
                      "success": True,
                      "data": data_list,
                      "total_elements": len(Data.query.all())
                    }
                  )
















# ---------- POST ----------

@app.route("/tickers", methods=["POST"])
def create_ticker():
    body = request.get_json()
    
    symbol      = body.get("symbol", None)
    name        = body.get("name", None)
    industry    = body.get("industry", None)
    description = body.get("description", None)

    ticker = Ticker(symbol=symbol, name=name, industry=industry, description=description)
    ticker.insert()
    
    selection = Ticker.query.order_by(Ticker.id).all()
    tickers = [ ticker.format() for ticker in selection ]

    return jsonify(
                    {
                      "success": True,
                      "created": ticker.id,
                      "tickers": tickers,
                      "total_elements": len(Ticker.query.all())
                    }
                  )



@app.route("/prices", methods=["POST"])
def create_price():
    body = request.get_json()
    
    date         = body.get("date", None)
    price        = body.get("price", None)
    ticker_id    = body.get("ticker_id", None)
    

    data = Data(date=date, price=price, ticker_id=ticker_id)
    data.insert()
    
    selection = Data.query.order_by(Data.id).all()
    data_list = [ data.format() for data in selection ]

    return jsonify(
                    {
                      "success": True,
                      "created": data.id,
                      "data": data_list,
                      "total_elements": len(Data.query.all())
                    }
                  )


















# ---------- PATCH ----------

@app.route("/tickers/<int:ticker_id>", methods=["PATCH"])
def update_ticker(ticker_id):
    body = request.get_json()
    
    
    ticker = Ticker.query.filter(Ticker.id == ticker_id).one_or_none()
    if ticker is None:
        abort(404)
        
    if "symbol" in body:
        ticker.symbol = str(body.get("symbol"))
    elif "industry" in body:
        ticker.industry = str(body.get("industry"))        
    elif "description" in body:
        ticker.description = str(body.get("description"))        
        
        
    ticker.update()
    
    return jsonify({
                    "success": True
                  })        
    


@app.route("/prices/<int:price_id>", methods=["PATCH"])
def update_price(price_id):
    body = request.get_json()
    
    
    data = Data.query.filter(Data.id == price_id).one_or_none()
    if data is None:
        abort(404)
        
    if "date" in body:
        data.date = str(body.get("date"))
    elif "price" in body:
        data.price = str(body.get("price"))        
    elif "ticker_id" in body:
        data.ticker_id = str(body.get("ticker_id"))        
        
        
    data.update()
    
    return jsonify({
                    "success": True
                  })     











 


# ---------- DELETE ----------

@app.route("/tickers/<int:ticker_id>", methods=["DELETE"])
def delete_ticker(ticker_id):

    ticker = Ticker.query.filter(Ticker.id == ticker_id).one_or_none()
    
    if ticker is None:
        abort(404)

    ticker.delete()
    
    selection = Ticker.query.order_by(Ticker.id).all()
    tickers = [ ticker.format() for ticker in selection ]


    return jsonify(
                    {
                      "success": True,
                      "deleted": ticker_id,
                      "tickers": tickers,
                      "total_elements": len(Ticker.query.all())
                    }
                  )




@app.route("/prices/<int:price_id>", methods=["DELETE"])
def delete_price(price_id):

    data = Data.query.filter(Data.id == price_id).one_or_none()
    
    if data is None:
        abort(404)

    data.delete()
    
    selection = Data.query.order_by(Data.id).all()
    data_list = [ data.format() for data in selection ]


    return jsonify(
                    {
                      "success": True,
                      "deleted": price_id,
                      "data": data_list,
                      "total_elements": len(Data.query.all())
                    }
                  )








# ---------- Error Handlers ------------ 
@app.errorhandler(404)
def not_found(error):
    return (
        jsonify({"success": False, "error": 404, "message": "resource not found"}),
        404
    )

@app.errorhandler(422)
def unprocessable(error):
    return (
        jsonify({"success": False, "error": 422, "message": "unprocessable"}),
        422
    )
    
@app.errorhandler(400)
def bad_request(error):
    return (
        jsonify({"success": False, "error": 400, "message": "bad request"}),
        400
    )    

@app.errorhandler(405)
def method_not_allowed(error):
    return (
        jsonify({"success": False, "error": 405, "message": "method not allowed"}),
        405
    )

@app.errorhandler(500)
def server_error(error):
    return (
        jsonify({"success": False, "error": 500, "message": "server error"}),
        500
    )




if __name__ == '__main__':
    #APP.run(host='0.0.0.0', port=8080, debug=True)
    app.run(host='0.0.0.0', port=8080, debug=True)