import os
import json
import pickle
import joblib
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

def task1_and_task2_spotify_model():
    print("==================================================")
    print("TASK 1 & 2: Spotify Song Genre Model (Pickle)")
    print("==================================================")
    
    # Features: [Tempo (BPM), Energy (0-100), Danceability (0-100)]
    X_songs = np.array([
        [120, 80, 85],  # Pop
        [140, 90, 60],  # Rock
        [128, 95, 90],  # EDM
        [70,  20, 30],  # Classical
        [118, 75, 80],  # Pop
        [145, 85, 55],  # Rock
        [130, 92, 88],  # EDM
        [65,  15, 25]   # Classical
    ])
    y_genres = np.array(['Pop', 'Rock', 'EDM', 'Classical', 'Pop', 'Rock', 'EDM', 'Classical'])
    
    # Train DecisionTreeClassifier
    dt_classifier = DecisionTreeClassifier(random_state=42)
    dt_classifier.fit(X_songs, y_genres)
    print("DecisionTreeClassifier trained successfully.")
    
    # Save model using Pickle
    model_filename = 'song_genre_model.pkl'
    with open(model_filename, 'wb') as f:
        pickle.dump(dt_classifier, f)
    print(f"Task 1 Complete: Model saved to '{model_filename}' using Pickle.\n")
    
    # Task 2: Load model and predict
    with open(model_filename, 'rb') as f:
        loaded_dt_model = pickle.load(f)
    
    # Predict for a new song: Tempo=126 BPM, Energy=94, Danceability=91
    new_song_features = np.array([[126, 94, 91]])
    predicted_genre = loaded_dt_model.predict(new_song_features)[0]
    
    print(f"Task 2 Complete: Loaded '{model_filename}'")
    print(f"New Song Features: Tempo=126 BPM, Energy=94, Danceability=91")
    print(f"Predicted Genre: {predicted_genre}\n")


def task3_flipkart_knn_model():
    print("==================================================")
    print("TASK 3: Flipkart Product Category Model (Joblib)")
    print("==================================================")
    
    # Features: [Weight (grams), Price (INR), Battery Included (1=Yes, 0=No)]
    X_products = np.array([
        [500,  25000, 1],  # electronics (smartphone)
        [200,   1500, 0],  # fashion (t-shirt)
        [1200, 45000, 1],  # electronics (laptop)
        [350,   2200, 0],  # fashion (jeans)
        [150,   3500, 1],  # electronics (earbuds)
        [400,   1200, 0]   # fashion (jacket)
    ])
    y_categories = np.array(['electronics', 'fashion', 'electronics', 'fashion', 'electronics', 'fashion'])
    
    # Train KNeighborsClassifier
    knn_classifier = KNeighborsClassifier(n_neighbors=3)
    knn_classifier.fit(X_products, y_categories)
    print("KNeighborsClassifier trained successfully.")
    
    # Save model using Joblib
    joblib_filename = 'product_category_model.joblib'
    joblib.dump(knn_classifier, joblib_filename)
    print(f"Task 3 Complete: Model saved to '{joblib_filename}' using Joblib.")
    
    # Verify by loading and predicting
    loaded_knn = joblib.load(joblib_filename)
    test_product = np.array([[180, 2900, 1]])  # Earbuds-like product
    pred_category = loaded_knn.predict(test_product)[0]
    print(f"Verification Prediction for [Weight=180g, Price=2900, Battery=1]: {pred_category}\n")


def task4_zomato_model_versioning():
    print("==================================================")
    print("TASK 4: Zomato Rating Model Versioning")
    print("==================================================")
    
    # Create directory structure for model versioning
    os.makedirs('models/v1', exist_ok=True)
    os.makedirs('models/v2', exist_ok=True)
    
    # Save model v1
    model_v1_path = 'models/v1/zomato_rating_model_v1.pkl'
    dummy_model_v1 = {"version": "v1.0.0", "algorithm": "LinearRegression", "mae": 0.35}
    with open(model_v1_path, 'wb') as f:
        pickle.dump(dummy_model_v1, f)
        
    # Save model v2
    model_v2_path = 'models/v2/zomato_rating_model_v2.pkl'
    dummy_model_v2 = {"version": "v2.0.0", "algorithm": "RandomForestRegressor", "mae": 0.18}
    with open(model_v2_path, 'wb') as f:
        pickle.dump(dummy_model_v2, f)
        
    # Metadata config file to track currently deployed model version
    deployment_config = {
        "active_version": "v2",
        "deployed_model_path": model_v2_path,
        "deployment_timestamp": "2026-09-06T22:38:00Z",
        "deployed_by": "MLOps_Pipeline"
    }
    
    config_path = 'models/deployed_version.json'
    with open(config_path, 'w') as f:
        json.dump(deployment_config, f, indent=4)
        
    print("Created directory structure:")
    print("  |-- models/")
    print("  |   |-- v1/zomato_rating_model_v1.pkl")
    print("  |   |-- v2/zomato_rating_model_v2.pkl")
    print("  |   `-- deployed_version.json (Tracks current live version)")
    print("Task 4 Complete.\n")

if __name__ == "__main__":
    task1_and_task2_spotify_model()
    task3_flipkart_knn_model()
    task4_zomato_model_versioning()
