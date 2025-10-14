import streamlit as st
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
from image_processing_app import ImageProcessingApp  # file Tkinter kamu

# ===============================
# SETUP STREAMLIT
# ===============================
st.set_page_config(page_title="Aplikasi PCD Web", layout="centered")

st.title("🧠 Aplikasi Pengolahan Citra Digital (Versi Web)")
st.write("Gunakan fitur di bawah ini untuk melakukan operasi citra digital secara online.")

# ===============================
# UPLOAD GAMBAR
# ===============================
uploaded_file = st.file_uploader("📤 Upload gambar pertama", type=["jpg", "jpeg", "png", "bmp"])

if uploaded_file:
    image = Image.open(uploaded_file)
    img_np = np.array(image)
    st.image(image, caption="Gambar 1", use_container_width=True)

    # Simpan citra di format OpenCV (BGR)
    img_cv2 = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

    # ===============================
    # PILIH OPERASI
    # ===============================
    st.subheader("⚙️ Pilih Operasi")

    operasi = st.selectbox(
        "Pilih jenis operasi:",
        [
            "Citra Biner",
            "Grayscale",
            "Atur Kecerahan",
            "Operasi Aritmetika (2 Gambar)",
            "Operasi Boolean (2 Gambar)",
            "Operasi Geometri"
        ]
    )

    # ===============================
    # OPERASI CITRA
    # ===============================
    if operasi == "Citra Biner":
        ambang = st.slider("Nilai Ambang (0-255)", 0, 255, 128)
        citra_gray = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2GRAY)
        _, citra_biner = cv2.threshold(citra_gray, ambang, 255, cv2.THRESH_BINARY)
        st.image(citra_biner, caption=f"Citra Biner (Ambang={ambang})", use_container_width=True)

    elif operasi == "Grayscale":
        citra_gray = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2GRAY)
        st.image(citra_gray, caption="Citra Grayscale", use_container_width=True)

    elif operasi == "Atur Kecerahan":
        nilai = st.slider("Nilai Kecerahan (-100 sampai 100)", -100, 100, 30)
        matriks_kecerahan = np.ones(img_cv2.shape, dtype="uint8") * abs(nilai)
        if nilai > 0:
            citra = cv2.add(img_cv2, matriks_kecerahan)
        else:
            citra = cv2.subtract(img_cv2, matriks_kecerahan)
        st.image(cv2.cvtColor(citra, cv2.COLOR_BGR2RGB),
                 caption=f"Citra setelah kecerahan {nilai}",
                 use_container_width=True)

    elif operasi == "Operasi Aritmetika (2 Gambar)":
        uploaded_file2 = st.file_uploader("Upload gambar kedua", type=["jpg", "jpeg", "png", "bmp"])
        if uploaded_file2:
            img2 = np.array(Image.open(uploaded_file2))
            img2_bgr = cv2.cvtColor(img2, cv2.COLOR_RGB2BGR)
            img2_resized = cv2.resize(img2_bgr, (img_cv2.shape[1], img_cv2.shape[0]))

            sum_img = cv2.add(img_cv2, img2_resized)
            sub_img = cv2.subtract(img_cv2, img2_resized)

            st.image([cv2.cvtColor(sum_img, cv2.COLOR_BGR2RGB),
                      cv2.cvtColor(sub_img, cv2.COLOR_BGR2RGB)],
                     caption=["Penjumlahan", "Pengurangan"])

    elif operasi == "Operasi Boolean (2 Gambar)":
        uploaded_file2 = st.file_uploader("Upload gambar kedua", type=["jpg", "jpeg", "png", "bmp"])
        if uploaded_file2:
            img2 = np.array(Image.open(uploaded_file2))
            img2_bgr = cv2.cvtColor(img2, cv2.COLOR_RGB2BGR)
            img2_resized = cv2.resize(img2_bgr, (img_cv2.shape[1], img_cv2.shape[0]))

            g1 = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2GRAY)
            g2 = cv2.cvtColor(img2_resized, cv2.COLOR_BGR2GRAY)

            _, b1 = cv2.threshold(g1, 128, 255, cv2.THRESH_BINARY)
            _, b2 = cv2.threshold(g2, 128, 255, cv2.THRESH_BINARY)

            and_op = cv2.bitwise_and(b1, b2)
            or_op = cv2.bitwise_or(b1, b2)
            xor_op = cv2.bitwise_xor(b1, b2)
            not_op = cv2.bitwise_not(b1)

            st.image([and_op, or_op, xor_op, not_op],
                     caption=["AND", "OR", "XOR", "NOT Citra 1"])

    elif operasi == "Operasi Geometri":
        from PIL import ImageOps
        citra_pil = Image.fromarray(cv2.cvtColor(img_cv2, cv2.COLOR_BGR2RGB))

        flip_h = ImageOps.mirror(citra_pil)
        flip_v = ImageOps.flip(citra_pil)
        rot_90 = citra_pil.rotate(90, expand=True)
        rot_45 = citra_pil.rotate(45, expand=True)

        st.image([flip_h, flip_v, rot_90, rot_45],
                 caption=["Flip Horizontal", "Flip Vertikal", "Rotasi 90°", "Rotasi 45°"])
