import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Auto Prompter - Pro", page_icon="✨")
st.title("✨ Auto Prompter: Pro Version")
st.markdown("Setiap prompt dilabel ikut Style masing-masing.")

# --- SIDEBAR ---
with st.sidebar:
    st.header("🔐 Kunci")
    api_key = st.text_input("Masukkan API Key", type="password")

# --- FUNGSI CARI MODEL ---
def find_valid_model():
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            if 'flash' in m.name or 'pro' in m.name:
                return m.name
    return None

# --- FUNGSI GENERATE ---
def generate_prompts(image, api_key):
    genai.configure(api_key=api_key)
    valid_model_name = find_valid_model()
    
    if not valid_model_name:
        return "ERROR_MODEL", "None"
    
    model = genai.GenerativeModel(valid_model_name)
    
    # KITA PAKSA AI GUNA FORMAT "STYLE: PROMPT"
    system_prompt = """
    Act as a fashion expert. Analyze the uploaded image.
    Create 8 DISTINCT AI PROMPTS for Midjourney/Flux.
    
    Styles: 
    1. Lookbook Studio
    2. Cinematic Outdoor
    3. Luxury Editorial
    4. Traditional/Cultural
    5. Close-Up Detail
    6. Minimalist E-Commerce
    7. Soft Pastel/Dreamy
    8. Street Style/Urban

    IMPORTANT OUTPUT FORMAT:
    You must use this exact format for every line:
    Style Name: The prompt text here.

    Example:
    Lookbook Studio: A professional studio shot of a red dress...
    Cinematic Outdoor: A realistic outdoor photo of...
    """
    
    response = model.generate_content([system_prompt, image])
    return response.text, valid_model_name

# --- UI (PAPARAN) ---
uploaded_file = st.file_uploader("Upload Gambar", type=["jpg", "png", "jpeg", "webp"])

if uploaded_file and st.button("Jana Prompt 🚀", type="primary"):
    if not api_key:
        st.error("Masukkan Key dulu.")
    else:
        try:
            image = Image.open(uploaded_file)
            st.image(image, width=200)
            
            with st.spinner("Sedang menulis prompt..."):
                text_output, model_used = generate_prompts(image, api_key)
                
                if text_output == "ERROR_MODEL":
                    st.error("Tak jumpa model AI yang sesuai.")
                else:
                    st.success(f"Siap! (Model: {model_used})")
                    st.markdown("---")
                    
                    # LOGIK PISAHKAN STYLE & PROMPT
                    prompts = text_output.split('\n')
                    
                    for p in prompts:
                        if p.strip():
                            # Kita cari simbol ":" untuk pisahkan Tajuk dan Isi
                            if ":" in p:
                                parts = p.split(":", 1) # Pisah dua
                                style_name = parts[0].strip().lstrip("0123456789.-* ") # Bersihkan nombor
                                prompt_content = parts[1].strip()
                                
                                # Paparkan Tajuk (Style)
                                st.subheader(f"🎨 {style_name}")
                                # Paparkan Kotak Copy (Isi sahaja)
                                st.code(prompt_content, language="text")
                            
                            else:
                                # Kalau AI tak letak ":", kita paparkan je semua
                                st.code(p, language="text")
                            
        except Exception as e:
            st.error(f"Error: {e}")
