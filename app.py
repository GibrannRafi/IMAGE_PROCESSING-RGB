import streamlit as st
from PIL import Image
import numpy as np
import io
import base64

st.set_page_config(page_title="RGB Color Picker", layout="wide")
st.title("🎨 RGB Color Picker dari Gambar")

# Layout dua kolom
col1, col2 = st.columns([3, 2])

with col1:
    uploaded_file = st.file_uploader("Upload gambar", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")

        # Konversi gambar jadi base64 agar bisa di-embed di HTML
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        byte_im = buf.getvalue()
        b64 = base64.b64encode(byte_im).decode()

        # HTML untuk gambar yang bisa diklik
        st.markdown(
            f"""
            <div style="position:relative;">
                <img id="img" src="data:image/png;base64,{b64}" style="max-width:100%;" />
                <script>
                    const img = document.getElementById('img');
                    img.addEventListener('click', function(e) {{
                        const rect = img.getBoundingClientRect();
                        const x = Math.round(e.clientX - rect.left);
                        const y = Math.round(e.clientY - rect.top);
                        window.parent.postMessage({{type: 'click', x, y}}, '*');
                    }});
                </script>
            </div>
            """,
            unsafe_allow_html=True
        )

with col2:
    st.subheader("📍 Koordinat & RGB")

# Tangkap koordinat dari event JavaScript
click = st.experimental_get_query_params()

# Streamlit tidak bisa langsung tangkap JS event, jadi kita buat handler sederhana
st.markdown("""
<script>
window.addEventListener('message', (e) => {
    if (e.data.type === 'click') {
        const url = new URL(window.location);
        url.searchParams.set('x', e.data.x);
        url.searchParams.set('y', e.data.y);
        window.location = url;
    }
});
</script>
""", unsafe_allow_html=True)

if uploaded_file and "x" in click and "y" in click:
    x, y = int(click["x"][0]), int(click["y"][0])
    rgb = np.array(image)[y, x].tolist()
    st.write(f"**Koordinat:** ({x}, {y})")
    st.write(f"**RGB:** {rgb}")
    st.markdown(
        f'<div style="width:100px;height:100px;background-color:rgb{tuple(rgb)};border-radius:10px;border:1px solid #ccc;"></div>',
        unsafe_allow_html=True,
    )
