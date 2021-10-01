from flask import Flask, jsonify, make_response

# ------------------------------------------------------------
#                   Flask Configuration
# ------------------------------------------------------------

app = Flask(__name__)

headers = {
    'charset': 'utf-8',
    'Content-Type': 'application/json',
}

def response(message={}, code=200):
    reponse = jsonify(message=message, headers=headers)
    return make_response(reponse, code)

def error_response(error='', code=400):
    reponse = jsonify(error=error, headers=headers)
    return make_response(reponse, code)


# ------------------------------------------------------------
#                   API endpoints
# ------------------------------------------------------------

@app.route("/")
def root():
    return response(message='root')

@app.errorhandler(400)
def bad_request(error='Bad request!'):
    return error_response(error=error, code=400)

@app.errorhandler(404)
def not_found(error='Not found!'):
    return error_response(error=error, code=404)
