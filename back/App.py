from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from builder import workoutBuilder
import os
app = Flask(__name__)
CORS(app)  # Enables CORS for all routes


class infoWorkout:
    def __init__(self, min, zone):
        self.min = []
        self.zone = []


data = []

# Example route


@app.route('/')
def home():
    return "Welcome to the Flask API!"


@app.route('/api/data', methods=['POST'])
def post_data():
    if request.is_json:
        data = request.get_json()
        infoWorkout.min = data["Vmin"]
        infoWorkout.zone = data["Vzone"]
        workoutBuilder(infoWorkout)
        print("Received JSON Data:", data)

        file_path = "/home/joaosimoes/Desktop/workout_fit_file_builder/tempo_bike_workout.fit"

        # Verifica se o ficheiro existe
        if os.path.exists(file_path):
            # Retorna o ficheiro

            response = send_file(
                file_path,
                as_attachment=True,            # Forces download
                download_name="workout.fit",   # Name for the downloaded file
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
