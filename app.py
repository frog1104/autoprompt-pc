import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Auto Prompter - Easy Copy", page_icon="✂️")
st.title("✂️ Auto Prompter: Easy Copy Mode")
st.markdown("Setiap prompt kini ada butang copy sendiri.")

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
        return ["ERROR: Tak jumpa model."], "None"
    
    model = genai.GenerativeModel(valid_model_name)
    
    # Kita minta AI bagi output yang bersih
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
    Just list the prompts. One prompt per line. 
    Do not put empty lines between prompts.
    Do not write intro text like "Here are the prompts".
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
            
            with st.spinner("Sedang memproses..."):
                text_output, model_used = generate_prompts(image, api_key)
                
                # Check error
                if "ERROR" in text_output[0]:
                    st.error("Ada masalah model.")
                else:
                    st.success(f"Siap! (Model: {model_used})")
                    st.write("Tekan ikon 📄 kecil di bucu kanan kotak untuk copy.")
                    st.markdown("---")
                    
                    # --- INI BAHAGIAN PECAHKAN PROMPT ---
                    # Kita pisahkan ayat berdasarkan baris baru (Enter)
                    prompts = text_output.split('\n')
                    
                    count = 1
                    for p in prompts:
                        # Abaikan baris kosong
                        if p.strip():
                            # Buang nombor (1. , 2.) di depan ayat supaya bersih
                            clean_p = p.lstrip("0123456789.-* ")
                            
                            # Buat Label Cantik
                            st.caption(f"🎨 Style {count}")
                            
                            # KOTAK KHAS DENGAN BUTANG COPY
                            st.code(clean_p, language="text")
                            
                            count += 1
                            
        except Exception as e:
            st.error(f"Error: {e}")
