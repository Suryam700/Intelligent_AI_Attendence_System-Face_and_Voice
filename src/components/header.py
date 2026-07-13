import streamlit as st

def header_home():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    st.markdown(f"""
                <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; margin: 30px 0;">
                    <img src={logo_url} alt="App logo" style='height: 100px;'/>
                    <h1 style='text-align: center; color: #E0E3FF'>SNAP<br/>CLASS</h1>
                </div>
                """, unsafe_allow_html=True)