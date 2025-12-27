import cv2
import numpy as np
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input  # type: ignore

# Fungsi segmentasi daun menggunakan HSV
def segment_leaf_hsv(img):
    """
    Input  : img (RGB numpy array)
    Output : segmented leaf image (RGB numpy array)
    """
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    lower = np.array([25,40,40])
    upper = np.array([85,255,255])
    mask = cv2.inRange(hsv, lower, upper)
    segmented = cv2.bitwise_and(img, img, mask=mask)
    return segmented

# Fungsi preprocessing untuk model
def preprocess_image(img_path):
    """
    Input  : img_path (path gambar)
    Output : preprocessed image siap masuk model (numpy array 1,224,224,3)
    """
    # Baca gambar
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Segmentasi daun
    seg = segment_leaf_hsv(img)

    # Resize
    img_in = cv2.resize(seg, (224,224))

    # Convert ke float32 & preprocess MobileNetV2
    img_in = img_in.astype(np.float32)
    img_in = preprocess_input(img_in)

    # Tambah batch dimension
    img_in = np.expand_dims(img_in, axis=0)

    return img_in, seg, img  # seg & img dikembalikan untuk visualisasi
