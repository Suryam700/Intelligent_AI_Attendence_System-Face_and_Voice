import streamlit as st

def footer(color):
    st.markdown(f"""
                <div style="margin-top:2rem; display:flex; gap:6px; justify-content:center; items-align:center">
                    <p style="font-weight:bold; color:{color};"> Created with ❤️ by <a href="https://github.com/Suryam700" style="color: {color}; text-decoration: none;">Suryam Gahoi</a></p>  
                </div>
                """, unsafe_allow_html=True)
