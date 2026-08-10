import streamlit as st
import yt_dlp
import os
import glob

# Configuración inicial de página
st.set_page_config(
    page_title="Diva MP3 Converter 💖✨",
    page_icon="💅",
    layout="centered"
)

# Estilos CSS Custom - Estilo Rosa Pop Diva 💖✨💅
DIVA_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600;700&family=Outfit:wght@400;600;800&display=swap');

/* Fondo principal Rosa Pop */
.stApp {
    background: linear-gradient(135deg, #ff758c 0%, #ff7eb3 40%, #ff1493 100%);
    font-family: 'Outfit', sans-serif;
    color: #ffffff;
}

/* Ocultar barra superior por defecto de Streamlit */
[data-testid="stHeader"] {
    background-color: rgba(0, 0, 0, 0);
}

/* Tarjeta Principal Glassmorphic */
.diva-card {
    background: rgba(255, 255, 255, 0.25);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-radius: 28px;
    padding: 35px 25px;
    border: 2px solid rgba(255, 255, 255, 0.4);
    box-shadow: 0 15px 35px rgba(255, 20, 147, 0.35), 0 5px 15px rgba(0, 0, 0, 0.1);
    text-align: center;
    margin-bottom: 25px;
}

/* Título Pop Diva */
.diva-title {
    font-family: 'Fredoka', cursive;
    font-size: 3rem !important;
    font-weight: 700;
    color: #ffffff;
    text-shadow: 0px 4px 12px rgba(219, 0, 110, 0.6), 0px 0px 20px #fff;
    margin-bottom: 5px;
}

.diva-subtitle {
    font-size: 1.15rem;
    font-weight: 600;
    color: #fff0f6;
    letter-spacing: 0.5px;
    margin-bottom: 20px;
    text-shadow: 0px 2px 4px rgba(0, 0, 0, 0.15);
}

.diva-badge {
    display: inline-block;
    background: #fff;
    color: #ff007f;
    font-weight: 800;
    padding: 6px 16px;
    border-radius: 50px;
    font-size: 0.85rem;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
    margin-bottom: 15px;
}

/* Inputs bonitos */
.stTextInput > div > div > input {
    border-radius: 20px !important;
    background-color: rgba(255, 255, 255, 0.9) !important;
    color: #880044 !important;
    border: 3px solid #ff66b2 !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    padding: 12px 20px !important;
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05) !important;
}

.stTextInput > div > div > input:focus {
    border-color: #ff007f !important;
    box-shadow: 0 0 15px rgba(255, 0, 127, 0.5) !important;
}

.stTextInput label {
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    text-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);
}

/* Botón Convertir Diva */
.stButton > button {
    width: 100%;
    background: linear-gradient(45deg, #ff007f, #ff52a2, #ff007f) !important;
    background-size: 200% auto !important;
    color: #ffffff !important;
    font-family: 'Fredoka', cursive !important;
    font-size: 1.4rem !important;
    font-weight: 700 !important;
    padding: 12px 24px !important;
    border-radius: 25px !important;
    border: 2px solid #ffffff !important;
    box-shadow: 0 10px 25px rgba(255, 0, 127, 0.5), 0 0 15px rgba(255, 255, 255, 0.4) !important;
    transition: all 0.3s ease-in-out !important;
    cursor: pointer !important;
}

.stButton > button:hover {
    transform: translateY(-3px) scale(1.02) !important;
    box-shadow: 0 15px 30px rgba(255, 0, 127, 0.7), 0 0 25px rgba(255, 255, 255, 0.8) !important;
    background-position: right center !important;
}

/* Botón Descargar (Streamlit native download button) */
.stDownloadButton > button {
    width: 100%;
    background: linear-gradient(45deg, #00f2fe, #4facfe) !important;
    color: #ffffff !important;
    font-family: 'Fredoka', cursive !important;
    font-size: 1.3rem !important;
    font-weight: 700 !important;
    padding: 12px 24px !important;
    border-radius: 25px !important;
    border: 2px solid #ffffff !important;
    box-shadow: 0 10px 20px rgba(79, 172, 254, 0.4) !important;
}

/* Alertas estilizadas */
.stAlert {
    border-radius: 18px !important;
    font-weight: 600 !important;
}

/* Footer Diva */
.diva-footer {
    text-align: center;
    color: rgba(255, 255, 255, 0.85);
    font-weight: 600;
    margin-top: 30px;
    font-size: 0.9rem;
}
</style>
"""

st.markdown(DIVA_CSS, unsafe_allow_html=True)

# Encabezado principal
st.markdown("""
    <div class="diva-card">
        <span class="diva-badge">✨ 320 KBPS ULTRA QUALITY ✨</span>
        <div class="diva-title">Diva MP3 Converter 💅🎶</div>
        <div class="diva-subtitle">Descarga tus canciones favoritas con el máximo estilo y calidad glam.</div>
    </div>
""", unsafe_allow_html=True)

# Campo para la URL
url = st.text_input("💖 Pega aquí el enlace de YouTube:", placeholder="https://www.youtube.com/watch?v=...")

# Espacio entre inputs
st.write("")

# Lógica de conversión
if st.button("✨ CONVERTIR A MP3 DIVA ✨"):
    if not url:
        st.warning("⚠️ Por favor, ingresa un enlace válido, reina.")
    else:
        with st.spinner("✨ Procesando tu temazo... Dame un segundo, reina ✨"):
            try:
                os.makedirs('downloads', exist_ok=True)
                
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '320',
                    }],
                    'outtmpl': 'downloads/%(title)s.%(ext)s',
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    title = info.get('title', 'audio_diva')

                list_of_files = glob.glob('downloads/*.mp3')
                latest_file = max(list_of_files, key=os.path.getctime)

                with open(latest_file, "rb") as file:
                    st.success("🎉 ¡Listo diva! Tu MP3 está preparado en máxima calidad.")
                    st.download_button(
                        label="📥 DESCARGAR MI MP3 DIVA 👑",
                        data=file,
                        file_name=os.path.basename(latest_file),
                        mime="audio/mpeg"
                    )

            except Exception as e:
                st.error(f"❌ Ocurrió un error al procesar el enlace: {str(e)}")

# Pie de página
st.markdown("""
    <div class="diva-footer">
        Hecho con 💖 para escuchar temazos desde tu teléfono ✨
    </div>
""", unsafe_allow_html=True)
