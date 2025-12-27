import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from .predict import model

def generate_gradcam(img_orig, img_in, class_idx, layer_name="Conv_1"):
    """
    img_orig  : gambar asli / segmentasi (RGB) untuk overlay
    img_in    : input model (1,224,224,3)
    class_idx : int, indeks class output (0=np.argmax(plant), 1=condition)
    """
    # Pilih output layer
    output_layer = model.get_layer("cond").output if class_idx==1 else model.get_layer("plant").output

    # Model untuk Grad-CAM
    grad_model = Model([model.inputs], [model.get_layer(layer_name).output, output_layer])

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_in)
        if class_idx==1:
            loss = predictions[:,0]  # condition
        else:
            loss = predictions[:,tf.argmax(predictions[0])]  # plant

    grads = tape.gradient(loss, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0,1,2))
    conv_outputs = conv_outputs[0]
    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    heatmap = np.maximum(heatmap,0)
    heatmap /= np.max(heatmap)+1e-8

    # Resize heatmap ke ukuran asli
    heatmap = cv2.resize(heatmap, (img_orig.shape[1], img_orig.shape[0]))
    heatmap = np.uint8(255*heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    # Overlay
    overlay = cv2.addWeighted(img_orig.astype(np.uint8), 0.6, heatmap, 0.4, 0)
    return overlay
