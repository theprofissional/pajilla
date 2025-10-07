from flask import Flask, request, jsonify
import numpy as np
from xgboost import XGBClassifier

app = Flask(__name__)

# نموذج مبدئي للتجربة
model = XGBClassifier()
model.fit(np.random.rand(10, 5), np.random.randint(0, 3, 10))

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    features = np.array(data.get("features", []))
    if features.ndim == 1:
        features = features.reshape(1, -1)
    preds = model.predict_proba(features)
    return jsonify({"prediction": preds.tolist()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
