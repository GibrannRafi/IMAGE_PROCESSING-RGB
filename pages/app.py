import streamlit as st
from PIL import Image, ImageDraw
import numpy as np
import pandas as pd
from streamlit_image_coordinates import streamlit_image_coordinates

st.set_page_config(page_title="RGB Pixel Viewer", layout="wide")
st.title("🎯 Deteksi Warna & Koordinat dari Gambar")

# CSS biar responsive di mobile
st.markdown("""
    <style>
    [data-testid="stImage"] img {
        max-width: 100%;
        height: auto;
        border-radius: 10px;
    }
    @media (max-width: 768px) {
        .block-container {
            padding: 1rem;
        }
        h1 { font-size: 1.6rem !important; }
    }
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader("📸 Upload gambar", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        img_array = np.array(image)
        st.write(f"🖼️ Ukuran gambar: **{image.width} x {image.height}** px")

        # Resize otomatis biar nggak kegedean di mobile
        max_display_width = 400  # px
        if image.width > max_display_width:
            aspect_ratio = image.height / image.width
            new_height = int(max_display_width * aspect_ratio)
            image_display = image.resize((max_display_width, new_height))
        else:
            image_display = image

        st.write("🖱️ Klik pada gambar di bawah ini:")
        coords = streamlit_image_coordinates(image_display, key="pilih_pixel")

        if coords is not None:
            x_scaled = int(coords["x"] * (image.width / image_display.width))
            y_scaled = int(coords["y"] * (image.height / image_display.height))

            if 0 <= x_scaled < image.width and 0 <= y_scaled < image.height:
                r, g, b = img_array[y_scaled, x_scaled]
                st.session_state["last_coords"] = (x_scaled, y_scaled, (r, g, b))

with col2:
    st.subheader("📍 Info Koordinat & Warna")

    if "last_coords" in st.session_state:
        x, y, (r, g, b) = st.session_state["last_coords"]
        st.write(f"**Koordinat:** (x={x}, y={y})")
        st.write(f"**RGB:** ({r}, {g}, {b})")
        st.markdown(
            f"<div style='width:80px;height:80px;background-color:rgb({r},{g},{b});border:2px solid #fff;border-radius:10px'></div>",
            unsafe_allow_html=True,
        )

        # Crosshair marker di preview kecil
        img_preview = image.copy()
        draw = ImageDraw.Draw(img_preview)
        cross_size = 10
        draw.line((x - cross_size, y, x + cross_size, y), fill=(255, 0, 0), width=2)
        draw.line((x, y - cross_size, x, y + cross_size), fill=(255, 0, 0), width=2)

        st.image(img_preview.resize((200, int(200 * image.height / image.width))), caption="Titik yang dipilih")

    else:
        st.info("Klik gambar di kiri untuk melihat warna dan koordinat.")
