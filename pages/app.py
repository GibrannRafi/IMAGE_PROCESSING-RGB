import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
from streamlit_image_coordinates import streamlit_image_coordinates

st.set_page_config(page_title="RGB Pixel Viewer", layout="wide")
st.title("🎯 Deteksi Warna & Koordinat dari Gambar")

col1, col2 = st.columns([3, 2])

with col1:
    uploaded_file = st.file_uploader("Upload gambar", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        img_array = np.array(image)
        st.write(f"Ukuran gambar: **{image.width} x {image.height}** (width x height)")

        # --- Gambar interaktif
        st.write("🖱️ Klik pada gambar di bawah ini:")
        coords = streamlit_image_coordinates(image, key="pilih_pixel")

        if coords is not None:
            x, y = coords["x"], coords["y"]

            # Ambil warna RGB
            if 0 <= x < image.width and 0 <= y < image.height:
                r, g, b = img_array[y, x]
                st.session_state["last_coords"] = (x, y, (r, g, b))

with col2:
    st.subheader("📍 Informasi Koordinat & Warna")

    if "last_coords" in st.session_state:
        x, y, (r, g, b) = st.session_state["last_coords"]

        st.write(f"**Koordinat:** (x={x}, y={y})")
        st.write(f"**RGB:** ({r}, {g}, {b})")
        st.markdown(
            f"<div style='width:100px;height:100px;background-color:rgb({r},{g},{b});border:2px solid #fff;border-radius:10px'></div>",
            unsafe_allow_html=True,
        )

        # 🎯 Tambahkan preview titik di gambar (crosshair)
        from PIL import ImageDraw
        img_preview = image.copy()
        draw = ImageDraw.Draw(img_preview)
        cross_size = 10
        draw.line((x - cross_size, y, x + cross_size, y), fill=(255, 0, 0), width=2)
        draw.line((x, y - cross_size, x, y + cross_size), fill=(255, 0, 0), width=2)

        st.write("🔍 Titik yang dipilih:")
        st.image(img_preview, use_container_width=True)

    else:
        st.info("Klik gambar di kiri untuk melihat warna dan koordinat.")
