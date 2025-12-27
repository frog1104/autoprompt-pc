import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- CONFIG ---
st.set_page_config(page_title="Auto Prompter - Final", page_icon="✨")
st.title("✨ Auto Prompter: Universal")
st.markdown("Upload gambar (Baju/Tudung/Kasut), dapatkan 8 Magic Prompt siap copy.")

# --- SIDEBAR: API KEY ---
with st.sidebar:
    st.header("🔐 Kunci")
    # Tuan masukkan Key yang 'BERJAYA' tadi di sini nanti
    api_key = st.text_input("Masukkan API Key", type="password")

# --- FUNGSI AI ---
def generate_prompts(image, api_key):
    # Setup
    genai.configure(api_key=api_key)
    
    # Kita guna model Flash (Laju)
    # Kalau flash tak jalan, kod ni automatik cari model lain (Safety net)
    target_model = 'gemini-1.5-flash'
    try:
        model = genai.GenerativeModel(target_model)
    except:
        model = genai.GenerativeModel('gemini-pro')

    # PROMPT "VISUAL DNA" (YANG TUAN BUAT)
    system_prompt = """
    Act as a professional fashion photographer and expert AI Prompt Engineer.
    Task: Perform a detailed visual analysis of the product in the uploaded image to extract its 'Visual DNA'. Focus ONLY on the item (Garment/Hijab/Shoes/Bag).
    
    Analyze: Type, Fabric & Texture, Color, Cut & Fit, Details.

    CRITICAL STEP:
    Based on the analysis, create 8 DISTINCT AI IMAGE PROMPTS for Midjourney/Flux.
    Styles:
    1. Lookbook Studio (Clean grey/white background, professional lighting)
    2. Cinematic Outdoor (Natural lighting, depth of field, realistic)
    3. Luxury Editorial (High fashion magazine style, dramatic)
    4. Traditional/Cultural Vibes (Kampung or heritage setting, warm tones)
    5. Close-Up Detail (Focus on fabric texture)
    6. Minimalist E-Commerce (Pure white background)
    7. Soft Pastel/Dreamy (Soft focus, airy)
    8. Street Style/Urban (Modern city background)

    OUTPUT FORMAT:
    Strictly output ONLY the list of 8 prompts. Do not write any intro.
    """
    
    response = model.generate_content([system_prompt, image])
    return response.text

# --- UI (PAPARAN) ---
uploaded_file = st.file_uploader("Upload Gambar Produk", type=["jpg", "png", "jpeg", "webp"])

if uploaded_file is not None:
    # 1. Tunjuk Gambar Dulu
    image = Image.open(uploaded_file)
    st.image(image, caption="Gambar Produk", width=300)
    
    # 2. Butang Jana
    if st.button("Jana Magic Prompt 🚀", type="primary"):
        if not api_key:
            st.error("Masukkan API Key kat tepi (Sidebar) dulu bos.")
        else:
            try:
                with st.spinner("Sedang analisis Visual DNA..."):
                    result_text = generate_prompts(image, api_key)
                    
                    st.success("Siap! Pilih style di bawah:")
                    st.markdown("---")
                    
                    # Bersihkan & Paparkan Output
                    lines = result_text.split('\n')
                    for line in lines:
                        if line.strip():
                            # Buang nombor (1. , 2.) supaya bersih
                            clean_line = line.lstrip('0123456789.-* ')
                            st.code(clean_line, language="text")
                            
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("Tips: Pastikan guna API Key yang 'BERJAYA' tadi.")
