#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from flask import Flask
from flask import jsonify
from flask.ext.cors import CORS 

app = Flask(__name__)
cors = CORS(app)

@app.route("/route")
def get_route():
    # get the sound from our database
    route = [{'a': 'yes', 'b': 'no'}, {'c': 'maybe'}]
    res = json.dumps(route)
    return res

if __name__ == "__main__":
    app.run(debug=True)

