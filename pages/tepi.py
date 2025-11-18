import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("🔍 Deteksi Tepi pada Citra")
st.write("Upload gambar untuk melihat hasil deteksi tepi (Canny).")

# Upload file
uploaded_file = st.file_uploader("Upload gambar", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Baca gambar
    image = Image.open(uploaded_file)
    img_array = np.array(image)

    # Tampilkan gambar asli
    st.subheader("Gambar Asli")
    st.image(img_array, use_column_width=True)

    # Konversi ke grayscale
    gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)

    # Slider untuk threshold Canny
    st.subheader("Pengaturan Canny Edge Detection")
    thresh1 = st.slider("Threshold 1", 0, 255, 100)
    thresh2 = st.slider("Threshold 2", 0, 255, 200)

    # Deteksi tepi
    edges = cv2.Canny(gray, thresh1, thresh2)

    # Tampilkan hasil
    st.subheader("Hasil Deteksi Tepi")
    st.image(edges, use_column_width=True, clamp=True)
