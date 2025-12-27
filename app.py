import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. SETUP HALAMAN ---
st.set_page_config(page_title="Auto Prompter Pro", page_icon="🎨")
st.title("🎨 Auto Prompter: PC Version")
st.markdown("Upload gambar produk, AI akan buatkan 8 Prompt Power untuk anda.")

# --- 2. INPUT KUNCI ---
with st.sidebar:
    st.header("Kunci Rahsia")
    api_key = st.text_input("Masukkan Google API Key", type="password")
    st.info("Gunakan Key dari 'Default Gemini Project' supaya tak error.")

# --- 3. FUNGSI AI (ANTI-GAGAL) ---
def get_gemini_model():
    # Ini teknik 'Fallback'. Dia cuba Flash, kalau tak ada, dia cuba Pro.
    # Supaya tak keluar error 404 lagi.
    supported_models = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]
    for model_name in supported_models:
        try:
            model = genai.GenerativeModel(model_name)
            return model, model_name
        except:
            continue
    return genai.GenerativeModel("gemini-1.5-flash-latest"), "flash-latest"

def analyze_image(image, api_key):
    genai.configure(api_key=api_key)
    model, model_name = get_gemini_model()
    
    # Prompt "Visual DNA" yang kita dah tune
    prompt = """
    Act as an Expert AI Prompt Engineer.
    Task: Analyze the uploaded fashion/product image deeply (Visual DNA).
    Focus on: Item Type, Fabric/Material, Color Palette, Cut/Shape, and Details.

    Based on this, create 8 DISTINCT AI ART PROMPTS for Midjourney/Flux.
    Styles to generate:
    1. Lookbook Studio (Clean, professional)
    2. Cinematic Outdoor (Golden hour, depth of field)
    3. Luxury Editorial (Vogue style, dramatic lighting)
    4. Cultural/Heritage (Kampung/Traditional vibe if applicable)
    5. Macro Detail (Focus on fabric texture)
    6. Minimalist E-Commerce (White background)
    7. Soft Pastel/Dreamy (Airy, gentle)
    8. Urban/Street Style (Modern background)

    OUTPUT FORMAT:
    Strictly output ONLY the list of 8 prompts. No intro text.
    """
    
    response = model.generate_content([prompt, image])
    return response.text, model_name

# --- 4. RUANG UPLOAD & BUTANG ---
uploaded_file = st.file_uploader("Pilih Gambar (JPG/PNG)", type=["jpg", "png", "jpeg", "webp"])

if uploaded_file is not None:
    # Papar gambar terus supaya user nampak
    image = Image.open(uploaded_file)
    st.image(image, caption="Gambar Preview", width=300)
    
    # Butang Jana
    if st.button("Jana Magic Prompt 🚀", type="primary"):
        if not api_key:
            st.error("⚠️ Sila masukkan API Key di sebelah kiri (Sidebar) dulu!")
        else:
            try:
                with st.spinner("Sedang memerah otak AI... Tunggu kejap..."):
                    result_text, used_model = analyze_image(image, api_key)
                    
                    st.success(f"Siap! (Dijana menggunakan model: {used_model})")
                    st.markdown("---")
                    
                    # Pecahkan result kepada kotak-kotak
                    prompts = result_text.split('\n')
                    for p in prompts:
                        if p.strip(): # Kalau baris tak kosong
                            # Bersihkan nombor (1. , 2. )
                            clean_p = p.lstrip('0123456789.-* ')
                            st.code(clean_p, language="text")
                            
            except Exception as e:
                st.error(f"Ada error sikit: {e}")
                st.warning("Tips: Pastikan API Key betul dan Internet PC stabil.")
