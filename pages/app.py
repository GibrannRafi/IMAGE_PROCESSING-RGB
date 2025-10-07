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
        .stDataFrame { font-size: 0.75rem; }
    }
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader("📸 Upload gambar", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        img_array = np.array(image)
        height, width = img_array.shape[:2]
        st.write(f"🖼️ Ukuran gambar: **{width} x {height} px**")

        # Buat tabel semua pixel (hati-hati gambar besar bisa berat!)
        df_all = pd.DataFrame(
            [[f"({r},{g},{b})" for (r,g,b) in row] for row in img_array],
            index=[y for y in range(height)],
            columns=[x for x in range(width)]
        )
        st.write("📊 **Tabel Seluruh Pixel (RGB):**")
        st.dataframe(df_all.head(20), use_container_width=True)  # tampilkan sebagian biar ringan

        # Resize otomatis biar gak kegedean di mobile
        max_display_width = 400
        if width > max_display_width:
            aspect_ratio = height / width
            new_height = int(max_display_width * aspect_ratio)
            image_display = image.resize((max_display_width, new_height))
        else:
            image_display = image

        st.write("🖱️ Klik pada gambar di bawah ini:")
        coords = streamlit_image_coordinates(image_display, key="pilih_pixel")

        if coords is not None:
            x_scaled = int(coords["x"] * (width / image_display.width))
            y_scaled = int(coords["y"] * (height / image_display.height))

            if 0 <= x_scaled < width and 0 <= y_scaled < height:
                r, g, b = img_array[y_scaled, x_scaled]
                st.session_state["last_coords"] = (x_scaled, y_scaled, (r, g, b))

                # Ambil area sekitar titik (5x5)
                half = 2
                y_min, y_max = max(0, y_scaled - half), min(height, y_scaled + half + 1)
                x_min, x_max = max(0, x_scaled - half), min(width, x_scaled + half + 1)
                region = img_array[y_min:y_max, x_min:x_max]
                df_region = pd.DataFrame(
                    [[f"({r},{g},{b})" for (r,g,b) in row] for row in region],
                    index=[y for y in range(y_min, y_max)],
                    columns=[x for x in range(x_min, x_max)]
                )
                st.session_state["pixel_table"] = df_region

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

        # Crosshair di preview
        img_preview = image.copy()
        draw = ImageDraw.Draw(img_preview)
        cross_size = 10
        draw.line((x - cross_size, y, x + cross_size, y), fill=(255, 0, 0), width=2)
        draw.line((x, y - cross_size, x, y + cross_size), fill=(255, 0, 0), width=2)
        st.image(img_preview.resize((200, int(200 * image.height / image.width))), caption="Titik yang dipilih")

        # Tabel pixel sekitar titik
        st.write("### 🧾 Tabel Pixel Sekitar Titik (5x5)")
        st.dataframe(st.session_state["pixel_table"], use_container_width=True)

    else:
        st.info("Klik gambar di kiri untuk melihat warna dan koordinat.")
        st.write("### 🧾 Tabel Pixel Sekitar Titik (5x5)")
        st.write("Belum ada titik yang dipilih.")
