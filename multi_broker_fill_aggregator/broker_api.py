from flask import jsonify, request
from . import app


@app.route("/api/brokera/<account_id>/fills?start=<start_date>...&end=<end_date>")
def broker_a_api():
    """
        [
      {"fill_id":"fa1","ts":"2025-06-01T14:03:10Z","symbol":"AAPL","side":"BUY","qty":2,"price":201.2,"order_id":"oa9"}
    ]

    """
    start_date = request.args.get("start")
    end_date = request.args.get("end")
    return jsonify(
        [
            {
                "fill_id": "fa1",
                "ts": "2025-06-01T14:03:10Z",
                "symbol": "AAPL",
                "side": "BUY",
                "qty": 2,
                "price": 201.2,
                "order_id": "oa9",
            }
        ]
    )


@app.route("/api/brokerb/<account_id>/fills?start=<start_date>...&end=<end_date>")
def broker_b_api():
    """
        {
      "fills": [
        {"id":"fb9","timestamp_ms":1748796190000,"ticker":"AAPL","direction":"B","filled_qty":2,"fill_price":201.2,"orderRef":"ob2"}
      ]
    }

    """
    start_date = requests.args.get("start")
    end_date = requests.args.get("end")
