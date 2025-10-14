# file: app.py
import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageOps
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Aplikasi Pengolahan Citra Digital (PCD)", layout="wide")
st.title("📸 Aplikasi Pengolahan Citra Digital (PCD)")

# --- Upload Gambar ---
uploaded_file = st.file_uploader("Unggah Gambar", type=['jpg','jpeg','png','bmp'])
if uploaded_file:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img_cv2 = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    img_rgb = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2RGB)

    st.subheader("Gambar Asli")
    st.image(img_rgb, use_column_width=True)

    max_h, max_w = img_rgb.shape[:2]

    # --- TABEL PIXEL RGB 10x10 ---
    st.subheader("Data Piksel (Interval 10x10)")
    data_pixel = []
    step = 10
    for y in range(0, max_h, step):
        for x in range(0, max_w, step):
            r, g, b = img_rgb[y, x]
            data_pixel.append({"Y Index": y, "X Index": x, "RGB Value": f"({r},{g},{b})"})
    df_pixel = pd.DataFrame(data_pixel)
    st.dataframe(df_pixel, use_container_width=True)

    # --- Menu Operasi via Dropdown ---
    st.sidebar.subheader("Menu Operasi Citra")
    ops = st.sidebar.selectbox("Pilih Operasi:", [
        "Grayscale",
        "Citra Biner",
        "Atur Kecerahan",
        "Operasi Aritmetika",
        "Operasi Boolean",
        "Operasi Geometri"
    ])

    if st.sidebar.button("Proses"):
        if ops == "Citra Biner":
            threshold = st.sidebar.slider("Ambang Batas (0-255)", 0, 255, 128)
            gray = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2GRAY)
            _, bin_img = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
            st.subheader("Hasil Citra Biner")
            st.image(bin_img, use_column_width=True, clamp=True, channels="L")

        elif ops == "Grayscale":
            gray = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2GRAY)
            st.subheader("Hasil Grayscale")
            st.image(gray, use_column_width=True, clamp=True, channels="L")

        elif ops == "Atur Kecerahan":
            brightness = st.sidebar.slider("Nilai Kecerahan (-255 sampai 255)", -255, 255, 30)
            if brightness >= 0:
                bright_img = cv2.add(img_cv2, np.ones(img_cv2.shape, dtype=np.uint8) * brightness)
            else:
                bright_img = cv2.subtract(img_cv2, np.ones(img_cv2.shape, dtype=np.uint8) * abs(brightness))
            st.subheader("Hasil Kecerahan")
            st.image(cv2.cvtColor(bright_img, cv2.COLOR_BGR2RGB), use_column_width=True)

        elif ops == "Operasi Aritmetika":
            uploaded_file2 = st.file_uploader("Unggah Gambar Kedua (Ukuran sama atau akan di-resize)", type=['jpg','jpeg','png','bmp'], key="aritmetika")
            if uploaded_file2:
                file_bytes2 = np.asarray(bytearray(uploaded_file2.read()), dtype=np.uint8)
                img2 = cv2.imdecode(file_bytes2, cv2.IMREAD_COLOR)
                if img2.shape[:2] != img_cv2.shape[:2]:
                    img2 = cv2.resize(img2, (max_w, max_h))
                sum_img = cv2.add(img_cv2, img2)
                sub_img = cv2.subtract(img_cv2, img2)
                st.subheader("Hasil Penjumlahan & Pengurangan")
                fig, ax = plt.subplots(1,2, figsize=(10,5))
                ax[0].imshow(cv2.cvtColor(sum_img, cv2.COLOR_BGR2RGB))
                ax[0].set_title("Penjumlahan"); ax[0].axis("off")
                ax[1].imshow(cv2.cvtColor(sub_img, cv2.COLOR_BGR2RGB))
                ax[1].set_title("Pengurangan"); ax[1].axis("off")
                st.pyplot(fig)

        elif ops == "Operasi Boolean":
            uploaded_file2 = st.file_uploader("Unggah Gambar Kedua (Ukuran sama atau akan di-resize)", type=['jpg','jpeg','png','bmp'], key="boolean")
            if uploaded_file2:
                file_bytes2 = np.asarray(bytearray(uploaded_file2.read()), dtype=np.uint8)
                img2 = cv2.imdecode(file_bytes2, cv2.IMREAD_COLOR)
                if img2.shape[:2] != img_cv2.shape[:2]:
                    img2 = cv2.resize(img2, (max_w, max_h))
                gray1 = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2GRAY)
                gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
                _, bin1 = cv2.threshold(gray1, 128, 255, cv2.THRESH_BINARY)
                _, bin2 = cv2.threshold(gray2, 128, 255, cv2.THRESH_BINARY)
                and_img = cv2.bitwise_and(bin1, bin2)
                or_img = cv2.bitwise_or(bin1, bin2)
                xor_img = cv2.bitwise_xor(bin1, bin2)
                not_img = cv2.bitwise_not(bin1)
                st.subheader("Hasil Operasi Boolean")
                fig, ax = plt.subplots(3,2, figsize=(10,10))
                ax[0,0].imshow(bin1, cmap='gray'); ax[0,0].set_title("Citra 1"); ax[0,0].axis('off')
                ax[0,1].imshow(bin2, cmap='gray'); ax[0,1].set_title("Citra 2"); ax[0,1].axis('off')
                ax[1,0].imshow(and_img, cmap='gray'); ax[1,0].set_title("AND"); ax[1,0].axis('off')
                ax[1,1].imshow(or_img, cmap='gray'); ax[1,1].set_title("OR"); ax[1,1].axis('off')
                ax[2,0].imshow(xor_img, cmap='gray'); ax[2,0].set_title("XOR"); ax[2,0].axis('off')
                ax[2,1].imshow(not_img, cmap='gray'); ax[2,1].set_title("NOT"); ax[2,1].axis('off')
                st.pyplot(fig)

        elif ops == "Operasi Geometri":
            pil_img = Image.fromarray(img_rgb)
            flip_h = ImageOps.mirror(pil_img)
            flip_v = ImageOps.flip(pil_img)
            rot_90 = pil_img.rotate(90, expand=True)
            rot_45 = pil_img.rotate(45, expand=True)
            st.subheader("Hasil Operasi Geometri")
            fig, ax = plt.subplots(2,3, figsize=(12,8))
            ax[0,0].imshow(pil_img); ax[0,0].set_title("Asli"); ax[0,0].axis("off")
            ax[0,1].imshow(flip_h); ax[0,1].set_title("Flip H"); ax[0,1].axis("off")
            ax[0,2].imshow(flip_v); ax[0,2].set_title("Flip V"); ax[0,2].axis("off")
            ax[1,0].imshow(rot_90); ax[1,0].set_title("Rot 90°"); ax[1,0].axis("off")
            ax[1,1].imshow(rot_45); ax[1,1].set_title("Rot 45°"); ax[1,1].axis("off")
            ax[1,2].axis("off")
            st.pyplot(fig)

    # --- Cari Piksel ---
    st.subheader("Cari Piksel RGB")
    x = st.number_input("X (Kolom)", min_value=0, max_value=max_w-1, value=0)
    y = st.number_input("Y (Baris)", min_value=0, max_value=max_h-1, value=0)
    if st.button("Cari RGB"):
        r,g,b = img_rgb[y,x]
        st.success(f"Hasil Piksel ({x},{y}): R={r}, G={g}, B={b}")
