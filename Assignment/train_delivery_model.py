import joblib
import numpy as np
from sklearn.linear_model import LinearRegression

def train_and_save_delivery_model():
    # Training Data: Features = [distance_km, order_size (items)]
    # Target = delivery_time_minutes
    X = np.array([
        [1.0, 1],
        [2.5, 2],
        [3.0, 4],
        [5.0, 3],
        [6.0, 5],
        [8.0, 2],
        [10.0, 6]
    ])
    
    y = np.array([12, 18, 24, 30, 38, 40, 55])
    
    # Train LinearRegression Model
    model = LinearRegression()
    model.fit(X, y)
    
    # Save trained model to file using joblib
    model_filename = 'delivery_model.joblib'
    joblib.dump(model, model_filename)
    print(f"LinearRegression model trained and saved successfully as '{model_filename}'.")
    
    # Verify sample prediction
    sample_input = np.array([[4.0, 3]])
    predicted_time = model.predict(sample_input)[0]
    print(f"Sample Prediction for distance=4.0km, order_size=3 items: {predicted_time:.2f} minutes")

if __name__ == '__main__':
    train_and_save_delivery_model()
