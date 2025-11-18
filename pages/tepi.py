import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.title("🔍 Deteksi Tepi pada Citra")
st.write("Upload gambar dan sistem akan melakukan deteksi tepi otomatis.")

# Upload file
uploaded_file = st.file_uploader("Upload gambar", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Baca gambar
    image = Image.open(uploaded_file)
    img = np.array(image)

    # Tampilkan gambar asli
    st.subheader("Gambar Asli")
    st.image(img, use_column_width=True)

    # Konversi ke grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Deteksi tepi otomatis (Canny default)
    edges = cv2.Canny(gray, 100, 200)

    # Tampilkan hasil
    st.subheader("Hasil Deteksi Tepi (Canny)")
    st.image(edges, use_column_width=True, clamp=True)
