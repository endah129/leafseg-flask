import numpy as np
from tensorflow.keras.models import load_model  # type: ignore

# Label sesuai Colab
PLANT_LABELS = ["Cherry","Grape","Potato","Strawberry"]
COND_LABELS  = ["Healthy","Diseased"]

# Load model sekali
MODEL_PATH = "leaf_segmentation_mobilenetv2.h5"
model = load_model(MODEL_PATH, compile=False)

def predict_image(img_in):
    """
    Input : img_in -> numpy array (1,224,224,3) hasil preprocess_image
    Output: dict {plant_label, plant_prob, cond_label, cond_prob}
    """
    plant_pred, cond_pred = model.predict(img_in, verbose=0)

    # Plant
    plant_idx   = np.argmax(plant_pred)
    plant_label = PLANT_LABELS[plant_idx]
    plant_prob  = float(plant_pred[0][plant_idx])

    # Condition
    cond_label = COND_LABELS[0] if cond_pred[0][0] < 0.5 else COND_LABELS[1]
    cond_prob  = float(cond_pred[0][0] if cond_label=="Diseased" else 1-cond_pred[0][0])

    return {
        "plant_label": plant_label,
        "plant_prob" : plant_prob,
        "cond_label" : cond_label,
        "cond_prob"  : cond_prob
    }

# Optional test
if __name__ == "__main__":
    from utils.preprocess import preprocess_image
    img_in, seg, img = preprocess_image("static/uploads/kentang_sakit.jpg")
    result = predict_image(img_in)
    print(result)
