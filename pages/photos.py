import streamlit as st
from PIL import Image, ImageOps, ImageEnhance
import numpy as np
import cv2

st.set_page_config(page_title="🧠 Pengolahan Citra Digital", layout="wide")

st.markdown("<h1 style='text-align:center;'>🧠 Pengolahan Citra Digital</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Grayscale, Biner, Brightness, Aritmatika, Boolean, Geometri</p>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("📤 Upload gambar", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    img_np = np.array(image)
    st.image(image, caption="Gambar Asli", use_container_width=True)

    st.markdown("---")
    operasi = st.selectbox(
        "🔹 Pilih Operasi Pengolahan Citra:",
        [
            "Grayscale",
            "Biner (Threshold)",
            "Brightness",
            "Aritmatika (+, -)",
            "Boolean (AND, OR, XOR)",
            "Geometri (Rotate, Flip)"
        ]
    )

    # ======== 1. GRAYSCALE ========
    if operasi == "Grayscale":
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        st.image(gray, caption="Hasil Grayscale", use_container_width=True, channels="GRAY")

    # ======== 2. BINER ========
    elif operasi == "Biner (Threshold)":
        gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
        thresh_val = st.slider("Tentukan Nilai Threshold", 0, 255, 128)
        _, binary = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY)
        st.image(binary, caption=f"Hasil Citra Biner (Threshold={thresh_val})", use_container_width=True, channels="GRAY")

    # ======== 3. BRIGHTNESS ========
    elif operasi == "Brightness":
        bright_val = st.slider("Atur Brightness", 0.1, 3.0, 1.0, 0.1)
        enhancer = ImageEnhance.Brightness(image)
        bright_img = enhancer.enhance(bright_val)
        st.image(bright_img, caption=f"Brightness x{bright_val}", use_container_width=True)

    # ======== 4. ARITMATIKA ========
    elif operasi == "Aritmatika (+, -)":
        st.info("Upload gambar kedua untuk operasi aritmatika.")
        file2 = st.file_uploader("📎 Upload gambar kedua", type=["jpg", "jpeg", "png"], key="img2")
        if file2:
            image2 = Image.open(file2).convert("RGB").resize(image.size)
            img2_np = np.array(image2)
            col1, col2 = st.columns(2)
            with col1: st.image(image, caption="Gambar 1")
            with col2: st.image(image2, caption="Gambar 2")

            jenis = st.radio("Pilih Operasi:", ["Penjumlahan (+)", "Pengurangan (-)"])
            if jenis == "Penjumlahan (+)":
                result = cv2.add(img_np, img2_np)
                st.image(result, caption="Hasil Penjumlahan", use_container_width=True)
            else:
                result = cv2.subtract(img_np, img2_np)
                st.image(result, caption="Hasil Pengurangan", use_container_width=True)

    # ======== 5. BOOLEAN ========
    elif operasi == "Boolean (AND, OR, XOR)":
        st.info("Upload dua citra biner (hitam putih) untuk operasi boolean.")
        file2 = st.file_uploader("📎 Upload gambar kedua", type=["jpg", "jpeg", "png"], key="bool2")
        if file2:
            img1_gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
            _, img1_bin = cv2.threshold(img1_gray, 128, 255, cv2.THRESH_BINARY)

            img2 = Image.open(file2).convert("RGB").resize(image.size)
            img2_np = np.array(img2)
            img2_gray = cv2.cvtColor(img2_np, cv2.COLOR_RGB2GRAY)
            _, img2_bin = cv2.threshold(img2_gray, 128, 255, cv2.THRESH_BINARY)

            operasi_bool = st.radio("Pilih Operasi Boolean:", ["AND", "OR", "XOR"])
            if operasi_bool == "AND":
                result = cv2.bitwise_and(img1_bin, img2_bin)
            elif operasi_bool == "OR":
                result = cv2.bitwise_or(img1_bin, img2_bin)
            else:
                result = cv2.bitwise_xor(img1_bin, img2_bin)

            col1, col2, col3 = st.columns(3)
            with col1: st.image(img1_bin, caption="Citra 1 (Biner)", channels="GRAY")
            with col2: st.image(img2_bin, caption="Citra 2 (Biner)", channels="GRAY")
            with col3: st.image(result, caption=f"Hasil {operasi_bool}", channels="GRAY")

    # ======== 6. GEOMETRI ========
    elif operasi == "Geometri (Rotate, Flip)":
        aksi = st.radio("Pilih Transformasi:", ["Rotate 90°", "Flip Horizontal", "Flip Vertical"])
        if aksi == "Rotate 90°":
            rotated = cv2.rotate(img_np, cv2.ROTATE_90_CLOCKWISE)
            st.image(rotated, caption="Rotasi 90°", use_container_width=True)
        elif aksi == "Flip Horizontal":
            flipped = cv2.flip(img_np, 1)
            st.image(flipped, caption="Flip Horizontal", use_container_width=True)
        else:
            flipped = cv2.flip(img_np, 0)
            st.image(flipped, caption="Flip Vertical", use_container_width=True)

else:
    st.info("📁 Silakan upload gambar terlebih dahulu.")
