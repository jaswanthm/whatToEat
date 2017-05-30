#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import requests
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def whattoeat(postcode):
    locationUrlFromLatLong = "https://developers.zomato.com/api/v2.1/cities?lat=28&lon=77"
    header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": "7b065f2ab284ab99edbeb7168ee19d27"}
    response = requests.get(locationUrlFromLatLong, headers=header)
    print(response.json())


def makeResult(req):
    #if req.get("contexts").get("name") == "context_name"

    #for item in req.get("result").get("contexts"):
    #    print(item["name"])
    #    if item["name"] == "context_name":
    #        resultName = item["parameters"].get("any")

    whattoeat(resultName)
    luckyNumber = "Hi"

    return {
        "speech": luckyNumber,
        "displayText": luckyNumber,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-jash",
        "possibleIntents": [
        {
          "intent": "actions.intent.PERMISSION",
          "inputValueData": {
            "@type": "type.googleapis.com/google.actions.v2.PermissionValueSpec",
            "optContext": "To deliver your order",
            "permissions": [
              "NAME",
              "DEVICE_PRECISE_LOCATION"
            ]
          }
        }
      ]
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
