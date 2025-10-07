


import streamlit as st
from PIL import Image
import numpy as np

st.set_page_config(page_title="RGB Color Picker", layout="wide")

st.title("🎨 RGB Color Picker dari Gambar")

# Layout dua kolom
col1, col2 = st.columns([3, 2])

with col1:
    uploaded_file = st.file_uploader("Upload gambar", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Klik pada area gambar untuk ambil RGB", use_container_width=True)

        # Gunakan Streamlit image click
        click = st.image(image, use_container_width=True, output_format="PNG")

with col2:
    if uploaded_file:
        st.subheader("📍 Koordinat dan RGB")

        # Simpan klik dengan st.session_state
        if "click_x" not in st.session_state:
            st.session_state.click_x = None
            st.session_state.click_y = None

        # Catatan: Streamlit default belum punya click event di st.image
        # Jadi kita gunakan cara alternatif dengan st_canvas (library streamlit-drawable-canvas)
        from streamlit_drawable_canvas import st_canvas

        st.write("Klik di gambar di kiri untuk ambil warna:")

        canvas_result = st_canvas(
            fill_color="rgba(255, 165, 0, 0.3)",
            stroke_width=0,
            stroke_color="#000000",
            background_image=image,
            update_streamlit=True,
            height=400,
            drawing_mode="point",
            key="canvas",
        )

        if canvas_result.json_data is not None:
            if len(canvas_result.json_data["objects"]) > 0:
                point = canvas_result.json_data["objects"][-1]
                x = int(point["left"])
                y = int(point["top"])
                rgb = np.array(image)[y, x].tolist()

                st.write(f"**Koordinat:** ({x}, {y})")
                st.write(f"**RGB:** {rgb}")
                st.markdown(
                    f'<div style="width:100px;height:100px;background-color:rgb{tuple(rgb)};border-radius:10px;"></div>',
                    unsafe_allow_html=True,
                )
