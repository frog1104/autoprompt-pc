import streamlit as st
import google.generativeai as genai

st.title("🕵️ Penyiasat Model")

# Masukkan Key Baru Tuan Di Sini
api_key = st.text_input("Masukkan Key BARU tadi", type="password")

if st.button("Check Suis"):
    if not api_key:
        st.error("Mana kuncinya?")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # Kita senaraikan apa model yang hidup
            models = []
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    models.append(m.name)
            
            if len(models) > 0:
                st.success(f"✅ BERJAYA! Suis Hidup! Ada {len(models)} model.")
                st.write(models)
                st.info("Sekarang baru kita boleh pasang kod apps sebenar!")
            else:
                st.error("❌ Alamak, senarai model KOSONG. Project ni pun tak ada suis.")
                
        except Exception as e:
            st.error(f"Error Key: {e}")
