import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import cv2
import numpy as np

from utils.preprocess import preprocess_image
from utils.predict import predict_image
from utils.gradcam import generate_gradcam

UPLOAD_FOLDER = "static/uploads/"
RESULT_FOLDER = "static/results/"
ALLOWED_EXTENSIONS = {"png","jpg","jpeg"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["RESULT_FOLDER"] = RESULT_FOLDER

# ------------------ Cek ekstensi file ------------------
def allowed_file(filename):
    return "." in filename and filename.rsplit(".",1)[1].lower() in ALLOWED_EXTENSIONS

# ------------------ Route homepage ------------------
@app.route("/", methods=["GET","POST"])
def index():
    if request.method=="POST":
        if "file" not in request.files:
            return redirect(request.url)
        file = request.files["file"]
        if file.filename=="":
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(upload_path)

            try:
                # Buat folder results jika belum ada
                os.makedirs(app.config["RESULT_FOLDER"], exist_ok=True)

                # ------------------ Preprocessing ------------------
                img_in, seg_img, orig_img = preprocess_image(upload_path)

                # ------------------ Predict ------------------
                result = predict_image(img_in)

                # ------------------ Grad-CAM ------------------
                overlay = generate_gradcam(seg_img, img_in, class_idx=0)  # Plant Grad-CAM

                # Simpan overlay
                result_path = os.path.join(app.config["RESULT_FOLDER"], filename)
                cv2.imwrite(result_path, cv2.cvtColor(overlay, cv2.COLOR_RGB2BGR))

                return render_template("index.html",
                                       filename=filename,
                                       result=result,
                                       result_path=result_path)
            except Exception as e:
                return render_template("index.html", error=f"Terjadi error saat prediksi: {str(e)}")

    return render_template("index.html", filename=None)

# ------------------ Route untuk menampilkan gambar upload ------------------
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return redirect(url_for("static", filename="uploads/"+filename))

# ------------------ Route untuk menampilkan hasil Grad-CAM ------------------
@app.route("/results/<filename>")
def result_file(filename):
    return redirect(url_for("static", filename="results/"+filename))

# ------------------ Jalankan Flask ------------------
if __name__=="__main__":
    app.run(debug=True, port=5050)
