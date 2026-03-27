import pickle
import pandas as pd
import os

# import the trained model
model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
with open(model_path, "rb") as f:
    model = pickle.load(f)

# Comes from MLFlow or any other model registry
MODEL_VERSION = "1.0.0"

# Get class labels from the model (important for mapping probabilities to actual category names)
class_labels = model.classes_.tolist()

def predict_output(user_input:dict):
    df = pd.DataFrame([user_input])

    # Predict the class
    predicted_class = model.predict(df)[0]

    # Get probabilities for all classes
    probabilities = model.predict_proba(df)[0]
    confidence = max(probabilities)

    # Create mapping of class labels to their probabilities
    class_prob_mapping = dict(zip(class_labels, map(lambda p: round(p, 4), probabilities)))
    
    return {
        "predicted_category": predicted_class,
        "confidence": round(confidence, 4),
        "class_probabilities": class_prob_mapping
    }