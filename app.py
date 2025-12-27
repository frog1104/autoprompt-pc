import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Auto Prompter - Hybrid", page_icon="🛡️")
st.title("🛡️ Auto Prompter: Hybrid Mode")
st.markdown("Kod ini akan cari sendiri model yang 'hidup' dalam akaun anda.")

# --- SIDEBAR ---
with st.sidebar:
    st.header("🔐 Kunci")
    api_key = st.text_input("Masukkan API Key", type="password")

# --- FUNGSI PENTING: CARI MODEL YANG HIDUP ---
def find_valid_model():
    # Kita scan semua model dalam akaun
    for m in genai.list_models():
        # Kita nak model yang boleh 'generateContent' dan versi '1.5'
        if 'generateContent' in m.supported_generation_methods:
            if 'flash' in m.name or 'pro' in m.name:
                return m.name # Jumpa! Pulangkan nama dia (contoh: models/gemini-1.5-flash-001)
    return None

# --- FUNGSI GENERATE ---
def generate_prompts(image, api_key):
    genai.configure(api_key=api_key)
    
    # 1. Cari Model Dulu
    valid_model_name = find_valid_model()
    
    if not valid_model_name:
        return "ERROR: Tak jumpa model Gemini 1.5 dalam akaun ini."
    
    # 2. Guna Model Yang Dijumpai
    model = genai.GenerativeModel(valid_model_name)
    
    # 3. Prompt Visual DNA
    system_prompt = """
    Act as a fashion expert. Analyze the uploaded image (Garment/Hijab/Accessory).
    Create 8 DISTINCT AI PROMPTS for Midjourney/Flux based on the visual DNA.
    Styles: Lookbook, Cinematic, Luxury, Cultural, Detail, Minimalist, Dreamy, Urban.
    Output ONLY the list of 8 prompts.
    """
    
    response = model.generate_content([system_prompt, image])
    return response.text, valid_model_name

# --- UI ---
uploaded_file = st.file_uploader("Upload Gambar", type=["jpg", "png", "jpeg", "webp"])

if uploaded_file and st.button("Jana Prompt 🚀", type="primary"):
    if not api_key:
        st.error("Masukkan Key dulu.")
    else:
        try:
            image = Image.open(uploaded_file)
            st.image(image, width=250)
            
            with st.spinner("Sedang mencari model & analisis gambar..."):
                # Panggil fungsi generate
                result = generate_prompts(image, api_key)
                
                # Check kalau result tu Error
                if isinstance(result, str) and "ERROR" in result:
                     st.error(result)
                else:
                    text_output, model_used = result
                    st.success(f"Berjaya! (Guna model: {model_used})")
                    st.code(text_output)
                    
        except Exception as e:
            # INI AKAN BAGITAHU KITA APA ERROR SEBENAR
            st.error(f"Error Terperinci: {e}")
