#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from random import randint

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
    #locationUrlFromLatLong = "https://developers.zomato.com/api/v2.1/cities?lat=28&lon=77"
    locationUrlFromLatLong = "https://developers.zomato.com/api/v2.1/search?entity_id=259&entity_type=city&q=abbotsford"
    header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": "7b065f2ab284ab99edbeb7168ee19d27"}

    #curl -X GET --header "Accept: application/json" --header "user-key: 7b065f2ab284ab99edbeb7168ee19d27" "https://developers.zomato.com/api/v2.1/search?entity_id=259&entity_type=city&q=abbotsford"
    response = requests.get(locationUrlFromLatLong, headers=header)

    responseJson = response.json()
    totalCount = responseJson.get("results_found")
    
    selected = responseJson.get("restaurants")[randint(0, 20)].get("restaurant")
    print(selected)

    speechResult = "I would suggest you to try " + selected.get("name") + " at " + selected.get("location").get("address")
    displayTextResult = "Try " + selected.get("name") + "\n You can find the menu here " + selected.get("menu_url")

    return {
        "speech": displayTextResult,
        "displayText": displayTextResult,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-jash",
        "slack": {
            "text": "This is an example of *bold*, _italic_, and `code`."
        }
    }
    #print(response.json())


def makeResult(req):
    #if req.get("contexts").get("name") == "context_name"

    #for item in req.get("result").get("contexts"):
    #    print(item["name"])
    #    if item["name"] == "context_name":
    #        resultName = item["parameters"].get("any")

    whatToReturn = whattoeat("resultName")


    return whatToReturn

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
