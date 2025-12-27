import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Auto Prompter Final", page_icon="🚀")
st.title("🚀 Auto Prompter: Final Version")

# Input Key
api_key = st.text_input("Masukkan API Key BARU (Dari Project Baru)", type="password")

uploaded_file = st.file_uploader("Upload Gambar", type=["jpg", "png", "jpeg"])

if uploaded_file and st.button("Jana Prompt"):
    if not api_key:
        st.error("Masukkan Key dulu.")
    else:
        try:
            st.info("Menghubungi AI...")
            genai.configure(api_key=api_key)
            
            # KITA GUNA MODEL 'GEMINI-PRO' BIASA (Paling Stabil)
            # Kalau Flash tak jalan, model ni selalunya jalan.
            model = genai.GenerativeModel("gemini-1.5-flash") 
            
            prompt = "Analyze this image and generate 8 AI Art prompts (Studio, Outdoor, Luxury, etc). List only."
            
            image = Image.open(uploaded_file)
            st.image(image, width=200)
            
            response = model.generate_content([prompt, image])
            st.success("Berjaya!")
            st.code(response.text)
            
        except Exception as e:
            st.error(f"Error: {e}")
            st.warning("Kalau error 404: Maknanya Key tu dari Project yang salah. Sila Create New Project di aistudio.google.com")
