import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
from streamlit_image_coordinates import streamlit_image_coordinates

# ========== STYLE GLOBAL ==========
st.set_page_config(page_title="🎨 Pixel Viewer", layout="centered")
st.markdown("""
    <style>
    body { background-color: #f8f9fa; }
    .main > div { padding: 1.5rem 2rem; border-radius: 15px; background: white; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    h1, h2, h3, h4, h5 { color: #2C3E50; }
    .stDataFrame { border-radius: 10px !important; }
    .pixel-box {
        width: 60px; height: 60px; 
        border-radius: 10px; 
        border: 2px solid #ddd; 
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# ========== APP TITLE ==========
st.markdown("<h1 style='text-align:center;'>🎨 Pixel Viewer Interaktif</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:gray;'>Upload gambar lalu klik titik manapun untuk melihat nilai RGB dan area sekitarnya</p>", unsafe_allow_html=True)

# ========== UPLOADER ==========
uploaded_file = st.file_uploader("📤 Upload gambar", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    height, width = img_array.shape[:2]

    st.divider()
    st.markdown(f"<h4>📏 Ukuran gambar:</h4> <p><b>{width} × {height}</b> (width × height)</p>", unsafe_allow_html=True)

    # ========== TABEL PIXEL ==========
    pixels = [[f"({r},{g},{b})" for (r, g, b) in row] for row in img_array[:, :, :3]]
    df_full = pd.DataFrame(pixels)

    with st.expander("📊 Lihat seluruh tabel pixel (klik untuk membuka)", expanded=False):
        st.dataframe(df_full, use_container_width=True)

    # ========== GAMBAR INTERAKTIF ==========
    st.markdown("### 🖱️ Klik pada gambar untuk melihat detail pixel")
    coords = streamlit_image_coordinates(image)

    if coords is not None:
        x, y = coords["x"], coords["y"]
        st.success(f"📍 Koordinat yang diklik: (x={x}, y={y})")

        if y < img_array.shape[0] and x < img_array.shape[1]:
            r, g, b = img_array[y, x][:3]

            # Warna dan RGB side by side
            col1, col2 = st.columns([1, 3])
            with col1:
                st.markdown(f"<div class='pixel-box' style='background-color:rgb({r},{g},{b});'></div>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"<h4>🎨 Nilai RGB:</h4> <p style='font-size:18px'><b>({r}, {g}, {b})</b></p>", unsafe_allow_html=True)

            # Fokus pada baris
            st.divider()
            st.markdown(f"### 🔎 Pixel pada baris ke-{y}")
            row_focus = pd.DataFrame([df_full.iloc[y]], index=[f"Row {y}"])
            st.dataframe(row_focus, use_container_width=True)

            # Area sekitar (5x5)
            st.markdown("### 🟩 Area sekitar titik (5×5 pixel):")
            y_start, y_end = max(0, y-2), min(height, y+3)
            x_start, x_end = max(0, x-2), min(width, x+3)
            neighborhood = df_full.iloc[y_start:y_end, x_start:x_end]
            st.dataframe(neighborhood, use_container_width=True)

else:
    st.info("📁 Silakan upload gambar terlebih dahulu.")
