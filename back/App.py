from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from builder import workoutBuilder
from dataBase import GetFitFile_from_db
import os

import tempfile

app = Flask(__name__)
CORS(app)  # Enables CORS for all routes


class infoWorkout:
    def __init__(self):
        self.min = []
        self.zone = []
        self.FileName = ""


data = []

# Example route


@app.route('/')
def home():
    return "Welcome to the Flask API!"


@app.route('/api/fitFile', methods=['GET'])
def getFitFile():
    fitFile = request.args.get('filename')
    print(fitFile)
    if not fitFile:
        return jsonify({"error": "O parâmetro 'filename' é obrigatório"}), 400

    binaryData = GetFitFile_from_db(fitFile)
    if not binaryData:
        return jsonify({"error": f"O ficheiro '{fitFile}' não foi encontrado"}), 404

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(binaryData)

    response = send_file(
        temp_file.name,
        download_name=fitFile,
        as_attachment=True,
        mimetype="application/octet-stream"
    )
    response.headers["Content-Disposition"] = "attachment; filename=tempo_bike_workout.fit"
    return response


@app.route('/api/data', methods=['POST'])
def post_data():
    if request.is_json:
        data = request.get_json()
        infoWorkout.min = data["Vmin"]
        infoWorkout.zone = data["Vzone"]
        infoWorkout.FileName = data["FileName"]
        Bdata = workoutBuilder(infoWorkout)
        print("Received JSON Data:", data)

        if len(data["FileName"]) > 0:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(Bdata)

            response = send_file(
                temp_file.name,
                as_attachment=True,
                download_name=data["FileName"],
                mimetype="application/octet-stream"
            )
            response.headers["Content-Disposition"] = "attachment; filename=tempo_bike_workout.fit"
            return response

        else:
            return jsonify({"error": "File not found"}), 404
    else:
        return jsonify({"error": "Request must be JSON"}), 400


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
