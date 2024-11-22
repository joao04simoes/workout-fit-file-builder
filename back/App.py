from flask import Flask, jsonify, request
from flask_cors import CORS
from builder import workoutBuilder
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
        infoWorkout.zone = data["Vzones"]
        workoutBuilder(infoWorkout)
        print("Received JSON Data:", data)
        return jsonify({"received": data}), 201
    else:
        return jsonify({"error": "Request must be JSON"}), 400


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
