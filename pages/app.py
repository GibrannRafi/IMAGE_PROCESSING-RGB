import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
from streamlit_image_coordinates import streamlit_image_coordinates

st.title("Pixel Viewer")

uploaded_file = st.file_uploader("Upload gambar", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Buka gambar
    image = Image.open(uploaded_file)
    img_array = np.array(image)

    # Ukuran gambar
    height, width = img_array.shape[:2]
    st.write(f"Ukuran gambar: **{width} x {height}** (width x height)")

    # Buat tabel seluruh pixel (hati-hati kalau gambar besar bisa berat!)
    pixels = [[f"({r},{g},{b})" for (r,g,b) in row] for row in img_array[:,:,:3]]
    df_full = pd.DataFrame(pixels)
    st.write("📊 Tabel seluruh pixel (RGB):")
    st.dataframe(df_full, use_container_width=True)

    # Gambar interaktif
    st.write("Klik pada gambar untuk melihat pixel tertentu 👇")
    coords = streamlit_image_coordinates(image)

    if coords is not None:
        x, y = coords["x"], coords["y"]

        st.success(f"📍 Koordinat yang diklik: (x={x}, y={y})")

        if y < img_array.shape[0] and x < img_array.shape[1]:
            r, g, b = img_array[y, x][:3]
            st.write(f"🎨 Nilai RGB di titik tersebut: **({r}, {g}, {b})**")

            # Preview warna
            st.markdown(
                f"<div style='width:50px;height:50px;background-color:rgb({r},{g},{b});border:1px solid #000'></div>",
                unsafe_allow_html=True
            )

            # Fokus ke cell tabel tertentu (tampilkan row y saja)
            row_focus = pd.DataFrame([df_full.iloc[y]], index=[f"Row {y}"])
            st.write(f"🔎 Pixel pada baris ke-{y}:")
            st.dataframe(row_focus, use_container_width=True)

            # Atau tampilkan area sekitar (misalnya 5x5 pixel di sekitar titik)
            y_start, y_end = max(0, y-2), min(height, y+3)
            x_start, x_end = max(0, x-2), min(width, x+3)
            neighborhood = df_full.iloc[y_start:y_end, x_start:x_end]
            st.write("🟩 Area sekitar titik yang diklik (5x5):")
            st.dataframe(neighborhood, use_container_width=True)
