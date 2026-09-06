import os
import joblib
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variable for loaded ML model
MODEL_PATH = 'delivery_model.joblib'
delivery_model = None

if os.path.exists(MODEL_PATH):
    delivery_model = joblib.load(MODEL_PATH)
    print(f"Loaded ML model from '{MODEL_PATH}'")
else:
    print(f"Warning: Model file '{MODEL_PATH}' not found. Please train the model first.")

@app.route('/', methods=['GET'])
def home():
    """Task 1: Root URL displaying welcome message."""
    return 'Welcome to the Prediction API'

@app.route('/predict-price', methods=['POST'])
def predict_price():
    """
    Task 2: REST API endpoint accepting JSON input with 'base_price' 
    and 'discount', returning the final price after discount.
    """
    try:
        data = request.get_json()
        if not data or 'base_price' not in data or 'discount' not in data:
            return jsonify({
                "status": "error",
                "message": "Missing required fields: 'base_price' and 'discount'"
            }), 400
            
        base_price = float(data['base_price'])
        discount = float(data['discount'])
        
        # Calculate final price after applying discount amount
        final_price = max(0.0, base_price - discount)
        
        return jsonify({
            "status": "success",
            "base_price": base_price,
            "discount": discount,
            "final_price": final_price
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/predict-delivery', methods=['POST'])
def predict_delivery():
    """
    Task 3 & 4: Uses loaded scikit-learn model to predict delivery time 
    and returns a JSON response with predicted time and a friendly Swiggy/Zomato style note.
    """
    global delivery_model
    try:
        # Lazy load model if not loaded at startup
        if delivery_model is None:
            if os.path.exists(MODEL_PATH):
                delivery_model = joblib.load(MODEL_PATH)
            else:
                return jsonify({
                    "status": "error",
                    "message": f"Model file '{MODEL_PATH}' not found on server."
                }), 500

        data = request.get_json()
        if not data or 'distance_km' not in data or 'order_size' not in data:
            return jsonify({
                "status": "error",
                "message": "Missing required fields: 'distance_km' and 'order_size'"
            }), 400

        distance_km = float(data['distance_km'])
        order_size = float(data['order_size'])

        # Predict using trained LinearRegression model
        input_features = np.array([[distance_km, order_size]])
        prediction = delivery_model.predict(input_features)[0]
        estimated_minutes = max(5.0, round(float(prediction), 1))

        # Task 4: Custom Zomato/Swiggy style friendly message
        friendly_message = (
            f"🛵 Hungry? Hot & fresh food is on its way! "
            f"Estimated delivery time is approximately {estimated_minutes} minutes. Bon Appétit!"
        )

        return jsonify({
            "status": "success",
            "distance_km": distance_km,
            "order_size": int(order_size),
            "estimated_delivery_time_minutes": estimated_minutes,
            "message": friendly_message
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    # Run Flask server locally on port 5000
    app.run(host='127.0.0.1', port=5000, debug=True)
