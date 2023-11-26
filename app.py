from flask import request, Flask, jsonify, make_response
from configs import PORT, ENV_SERVICE, APP

# from flask_cors import CORS
from main import getDataExperian

app = Flask(__name__)
# cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/", methods=["GET"])
def home():
    return "Service up on PROD PORT {}, {} [{}]".format(PORT, APP, ENV_SERVICE)


@app.route("/api/v1/getdata", methods=["GET"])
def get_data():
    if request.method == "GET":
        try:
            document = request.args.get("document")
            lastname = request.args.get("lastname")
            if not lastname or not document:
                return make_response(
                    jsonify({"success": False, "data": [], "error": 'Los parámetros document y lastname son obligatorios.'}),
                    400
                )
            response_data = getDataExperian(document=document, lastname=lastname)
            return jsonify(response_data)

        except Exception as error_response:
            print(error_response)
            return make_response(
                jsonify(
                    {
                        "message": "Ha ocurrido un error interno, por favor intente mas tarde.",
                        "trace": str(error_response),
                    }
                ),
                500,
            )


def run():
    app.debug = True
    app.run(host="0.0.0.0", port=PORT)


if __name__ == "__main__":
    run()

"""
Ejecutar Flask
python -m  flask run --host=0.0.0.0 --port=5500
"""
