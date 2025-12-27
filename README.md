# 🍃 LeafSeg — Leaf Disease Detection Web App

LeafSeg adalah aplikasi web berbasis **Flask + Deep Learning** yang digunakan untuk
**mendeteksi jenis tanaman dan kondisi daun (sehat / sakit)** dari citra daun
menggunakan **MobileNetV2** dan **segmentasi HSV**.

Proyek ini dibuat sebagai bagian dari **UAS Pengolahan Citra Digital**.

---

## ✨ Fitur Utama
- Upload gambar daun (JPG / PNG)
- Segmentasi daun menggunakan **HSV Color Space**
- Klasifikasi:
  - **Jenis tanaman** (Cherry, Grape, Potato, Strawberry)
  - **Kondisi daun** (Sehat / Sakit)
- Visualisasi **Grad-CAM Heatmap**
- Tampilan web modern (Bootstrap)

---

## 🧠 Model & Metode
- **CNN Architecture**: MobileNetV2 (Transfer Learning)
- **Input Size**: 224 × 224
- **Preprocessing**:
  - Resize
  - HSV segmentation
  - `preprocess_input` MobileNetV2
- **Output**:
  - Multi-output model:
    - Softmax → jenis tanaman
    - Sigmoid → kondisi daun

---

## 📊 Akurasi Model (Testing)
- **Plant Classification Accuracy**: ±99%
- **Condition Classification Accuracy**: ±100%

> Akurasi diperoleh dari evaluasi pada dataset test di Google Colab.

---

## 📁 Struktur Folder
flask_backend/
│
├── app.py
├── requirements.txt
├── leaf_segmentation_mobilenetv2.h5
│
├── static/
│ ├── css/
│ ├── js/
│ ├── uploads/
│ └── results/
│
├── templates/
│ └── index.html
│
├── utils/
│ ├── preprocess.py
│ ├── predict.py
│ └── gradcam.py
│
└── README.md

---

## ⚙️ Cara Menjalankan Aplikasi

1️⃣ Clone Repository
'''bash
git clone https://github.com/USERNAME/leafseg.git
cd flask_backend
'''

2️⃣ Buat Virtual Environment
python -m venv venv
venv\Scripts\activate

3️⃣ Install Dependency
pip install -r requirements.txt

4️⃣ Jalankan Flask
python app.py

Akses di browser:

http://127.0.0.1:5050

🧪 Dataset

Dataset citra daun tanaman yang terdiri dari:

Cherry, Grape, Potato, Strawberry

Dengan dua kondisi:

Healthy & Diseased

Dataset diproses ulang dan dibagi menjadi train / validation / test.

👩‍💻 Author

Endah Komariyah Lestari
Mahasiswa S1
Universitas Bumigora Mataram