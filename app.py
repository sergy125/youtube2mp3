import streamlit as st
import yt_dlp
import os
import glob

st.set_page_config(
    page_title="Diva MP3",
    page_icon="🎧",
    layout="centered"
)

DIVA_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@600;700&family=Outfit:wght@400;500;600;700&display=swap');

:root {
    --diva-pink: #ff2d87;
    --diva-pink-soft: #ff8fc3;
    --diva-dark: #3a0d29;
    --diva-cream: #fff5f9;
}

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Outfit', sans-serif;
}

.stApp {
    background: radial-gradient(circle at 20% 0%, #ffb3d9 0%, transparent 45%),
                radial-gradient(circle at 100% 100%, #ff6fb8 0%, transparent 55%),
                linear-gradient(160deg, #2b0a20 0%, #5a1240 45%, #b3195e 100%);
    background-attachment: fixed;
    color: var(--diva-cream);
}

[data-testid="stHeader"] {
    background-color: rgba(0, 0, 0, 0);
}

[data-testid="stAppViewContainer"] > .main {
    padding-top: 2rem;
}

.block-container {
    max-width: 560px;
    padding-left: 1.2rem;
    padding-right: 1.2rem;
}

/* Tarjeta principal */
.diva-card {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 24px;
    padding: 40px 28px;
    border: 1px solid rgba(255, 255, 255, 0.18);
    box-shadow: 0 20px 45px rgba(0, 0, 0, 0.35);
    text-align: center;
    margin-bottom: 28px;
}

.diva-icon {
    font-size: 2.4rem;
    margin-bottom: 6px;
    filter: drop-shadow(0 4px 10px rgba(0,0,0,0.3));
}

.diva-title {
    font-family: 'Fraunces', serif;
    font-size: 2.5rem;
    font-weight: 700;
    letter-spacing: -0.5px;
    background: linear-gradient(90deg, #ffe0f0, #ff9fd0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 8px 0;
}

.diva-subtitle {
    font-size: 0.98rem;
    font-weight: 400;
    color: rgba(255, 245, 249, 0.75);
    margin-bottom: 18px;
    line-height: 1.4;
}

.diva-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(255, 255, 255, 0.12);
    border: 1px solid rgba(255, 255, 255, 0.25);
    color: var(--diva-cream);
    font-weight: 600;
    padding: 6px 16px;
    border-radius: 50px;
    font-size: 0.78rem;
    letter-spacing: 0.4px;
}

/* Inputs */
.stTextInput > div > div > input {
    border-radius: 16px !important;
    background-color: rgba(255, 255, 255, 0.95) !important;
    color: var(--diva-dark) !important;
    border: none !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
    padding: 14px 18px !important;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1) !important;
}

.stTextInput > div > div > input:focus {
    box-shadow: 0 0 0 3px rgba(255, 45, 135, 0.45) !important;
}

.stTextInput label {
    color: rgba(255, 245, 249, 0.9) !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
}

/* Botón principal */
.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #ff2d87, #ff6fb8) !important;
    color: #ffffff !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    padding: 14px 24px !important;
    border-radius: 16px !important;
    border: none !important;
    box-shadow: 0 12px 24px rgba(255, 45, 135, 0.35) !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    margin-top: 6px;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 16px 30px rgba(255, 45, 135, 0.45) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* Botón de descarga */
.stDownloadButton > button {
    width: 100%;
    background: rgba(255, 255, 255, 0.95) !important;
    color: var(--diva-dark) !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    padding: 14px 24px !important;
    border-radius: 16px !important;
    border: none !important;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.25) !important;
}

/* Alertas */
.stAlert {
    border-radius: 14px !important;
    font-weight: 500 !important;
}

.diva-footer {
    text-align: center;
    color: rgba(255, 245, 249, 0.45);
    font-weight: 400;
    font-size: 0.82rem;
    margin-top: 10px;
}

/* Responsive: móvil */
@media (max-width: 480px) {
    .block-container {
        padding-left: 0.8rem;
        padding-right: 0.8rem;
        padding-top: 1rem;
    }
    .diva-card {
        padding: 28px 18px;
        border-radius: 20px;
    }
    .diva-title {
        font-size: 1.9rem;
    }
    .diva-subtitle {
        font-size: 0.9rem;
    }
    .diva-icon {
        font-size: 2rem;
    }
    .stButton > button, .stDownloadButton > button {
        font-size: 0.95rem !important;
        padding: 13px 20px !important;
    }
}
</style>
"""

st.markdown(DIVA_CSS, unsafe_allow_html=True)

st.markdown("""
    <div class="diva-card">
        <div class="diva-icon">🎧</div>
        <div class="diva-title">Diva MP3</div>
        <div class="diva-subtitle">Convierte tus vídeos de YouTube en audio MP3 de máxima calidad.</div>
        <span class="diva-badge">✨ 320 kbps</span>
    </div>
""", unsafe_allow_html=True)

url = st.text_input("Enlace de YouTube", placeholder="https://www.youtube.com/watch?v=...")

st.write("")

if st.button("Convertir a MP3"):
    if not url:
        st.warning("Ingresa un enlace válido para continuar.")
    else:
        with st.spinner("Convirtiendo tu audio..."):
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
                    title = info.get('title', 'audio')

                list_of_files = glob.glob('downloads/*.mp3')
                latest_file = max(list_of_files, key=os.path.getctime)

                with open(latest_file, "rb") as file:
                    st.success("Tu MP3 está listo.")
                    st.download_button(
                        label="Descargar MP3",
                        data=file,
                        file_name=os.path.basename(latest_file),
                        mime="audio/mpeg"
                    )

            except Exception as e:
                st.error(f"Ocurrió un error al procesar el enlace: {str(e)}")

st.markdown("""
    <div class="diva-footer">Diva MP3</div>
""", unsafe_allow_html=True)
