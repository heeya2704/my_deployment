import time
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def test_api():
    print("Testing Flask Prediction API endpoints...\n")
    
    # 1. Test Root Endpoint GET /
    try:
        r_home = requests.get(f"{BASE_URL}/")
        print("1. GET / Response:")
        print(f"   Status Code: {r_home.status_code}")
        print(f"   Response Text: {r_home.text}\n")
    except Exception as e:
        print(f"1. GET / Error: {e}\n")

    # 2. Test /predict-price POST
    try:
        payload_price = {"base_price": 499.0, "discount": 50.0}
        headers = {"Content-Type": "application/json"}
        r_price = requests.post(f"{BASE_URL}/predict-price", json=payload_price, headers=headers)
        print("2. POST /predict-price Response:")
        print(f"   Status Code: {r_price.status_code}")
        print(f"   Response JSON: {json.dumps(r_price.json(), indent=2)}\n")
    except Exception as e:
        print(f"2. POST /predict-price Error: {e}\n")

    # 3. Test /predict-delivery POST
    try:
        payload_delivery = {"distance_km": 4.5, "order_size": 3}
        headers = {"Content-Type": "application/json"}
        r_delivery = requests.post(f"{BASE_URL}/predict-delivery", json=payload_delivery, headers=headers)
        print("3. POST /predict-delivery Response:")
        print(f"   Status Code: {r_delivery.status_code}")
        print(f"   Response JSON: {json.dumps(r_delivery.json(), indent=2)}\n")
    except Exception as e:
        print(f"3. POST /predict-delivery Error: {e}\n")

if __name__ == "__main__":
    test_api()
