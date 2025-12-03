import sys
import json
import joblib
import os
import numpy as np

# Load once and keep in memory
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'model', 'chili_variant_10k.joblib')
MODEL_PATH = os.path.abspath(MODEL_PATH)

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    print(json.dumps({"error": f"Model not available: {e}"}))
    sys.exit()

FEATURE_NAMES = ['N', 'P', 'K', 'pH_Value', 'Moisture', 'Temperature', 'Humidity', 'Rainfall']
FEATURE_INDICES = {name: idx for idx, name in enumerate(FEATURE_NAMES)}

def main():
    raw_input = sys.stdin.read().strip()
    
    if not raw_input:
        print(json.dumps({"error": "No input received"}))
        return
    
    try:
        data = json.loads(raw_input)
        # Pre-allocate array for better performance
        values = np.zeros(len(FEATURE_NAMES), dtype=np.float32)
        
        for i, feature in enumerate(FEATURE_NAMES):
            values[i] = float(data[feature])
        
        prediction = model.predict(values.reshape(1, -1))[0]
        
        # Fast type conversion
        if hasattr(prediction, 'item'):
            prediction = prediction.item()
        elif isinstance(prediction, np.ndarray):
            prediction = prediction.tolist()
        
        print(json.dumps({"prediction": prediction}))
        
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    main()