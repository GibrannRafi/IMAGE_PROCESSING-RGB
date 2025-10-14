
import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="Aplikasi Pengolahan Citra Digital (PCD)", layout="wide")
st.title("📸 Aplikasi Pengolahan Citra Digital (PCD)")

# --- Upload Gambar ---
uploaded_file = st.file_uploader("Unggah Gambar", type=['jpg','jpeg','png','bmp'])
if uploaded_file:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img_cv2 = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    img_rgb = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2RGB)
    
    max_h, max_w = img_rgb.shape[:2]

    st.subheader("Gambar Asli")
    st.image(img_rgb, use_column_width=True)

    # --- Operasi Citra ---
    ops = st.selectbox("Pilih Operasi Citra:", [
        "Citra Biner",
        "Grayscale",
        "Atur Kecerahan",
        "Operasi Aritmetika",
        "Operasi Boolean",
        "Operasi Geometri"
    ])

    # --- Input untuk setiap operasi ---
    if ops == "Citra Biner":
        threshold = st.slider("Ambang Batas (0-255)", 0, 255, 128, key="thresh")
        if st.button("Proses Citra Biner"):
            gray = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2GRAY)
            _, bin_img = cv2.threshold(gray, st.session_state.thresh, 255, cv2.THRESH_BINARY)
            st.subheader("Hasil Citra Biner")
            st.image(bin_img, use_column_width=True, clamp=True, channels="L")

    elif ops == "Grayscale":
        if st.button("Proses Grayscale"):
            gray = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2GRAY)
            st.subheader("Hasil Grayscale")
            st.image(gray, use_column_width=True, clamp=True, channels="L")

    elif ops == "Atur Kecerahan":
        brightness = st.slider("Nilai Kecerahan (-255 sampai 255)", -255, 255, 30, key="bright")
        if st.button("Proses Kecerahan"):
            val = st.session_state.bright
            if val >= 0:
                bright_img = cv2.add(img_cv2, np.ones(img_cv2.shape, dtype=np.uint8) * val)
            else:
                bright_img = cv2.subtract(img_cv2, np.ones(img_cv2.shape, dtype=np.uint8) * abs(val))
            st.subheader("Hasil Kecerahan")
            st.image(cv2.cvtColor(bright_img, cv2.COLOR_BGR2RGB), use_column_width=True)

    elif ops == "Operasi Aritmetika":
        uploaded_file2 = st.file_uploader("Unggah Gambar Kedua (Ukuran sama atau akan di-resize)", type=['jpg','jpeg','png','bmp'], key="aritmetika")
        if uploaded_file2:
            file_bytes2 = np.asarray(bytearray(uploaded_file2.read()), dtype=np.uint8)
            img2 = cv2.imdecode(file_bytes2, cv2.IMREAD_COLOR)
            if img2.shape[:2] != img_cv2.shape[:2]:
                img2 = cv2.resize(img2, (max_w, max_h))
            
            operator = st.selectbox("Pilih Operator:", ["+", "-", "*", "/"], key="operator_arit")
            if st.button("Proses Aritmetika"):
                if operator == "+":
                    result_img = cv2.add(img_cv2, img2)
                elif operator == "-":
                    result_img = cv2.subtract(img_cv2, img2)
                elif operator == "*":
                    result_img = cv2.multiply(img_cv2.astype(np.float32)/255.0, img2.astype(np.float32)/255.0)
                    result_img = np.clip(result_img*255, 0, 255).astype(np.uint8)
                elif operator == "/":
                    img2_safe = img2.copy()
                    img2_safe[img2_safe==0] = 1
                    result_img = cv2.divide(img_cv2.astype(np.float32), img2_safe.astype(np.float32))
                    result_img = np.clip(result_img*255/np.max(result_img), 0, 255).astype(np.uint8)

                st.subheader(f"Hasil Operasi Aritmetika ({operator})")
                st.image(cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB), use_column_width=True)

    elif ops == "Operasi Boolean":
        uploaded_file2 = st.file_uploader("Unggah Gambar Kedua (Ukuran sama atau akan di-resize)", type=['jpg','jpeg','png','bmp'], key="boolean")
        if uploaded_file2 and st.button("Proses Boolean"):
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
        if st.button("Proses Geometri"):
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

    # --- Tabel Pixel RGB (10x10 interval) ---
    st.subheader("Tabel Data Pixel (Interval 10x10)")
    data = []
    step = 10
    for y in range(0, max_h, step):
        for x in range(0, max_w, step):
            r,g,b = img_rgb[y,x]
            data.append([y, x, f"({r},{g},{b})"])
    df_pixels = pd.DataFrame(data, columns=["Y Index (Baris)", "X Index (Kolom)", "Nilai RGB (R,G,B)"])
    st.dataframe(df_pixels)

    # --- Cari Pixel ---
    st.subheader("Cari Piksel RGB")
    x_coord = st.number_input("X (Kolom)", min_value=0, max_value=max_w-1, value=0)
    y_coord = st.number_input("Y (Baris)", min_value=0, max_value=max_h-1, value=0)
    if st.button("Cari RGB"):
        r,g,b = img_rgb[y_coord,x_coord]
        st.success(f"Hasil Piksel ({x_coord},{y_coord}): R={r}, G={g}, B={b}")
