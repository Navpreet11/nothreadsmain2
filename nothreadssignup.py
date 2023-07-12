import streamlit as st
import sqlite3
from PIL import Image


img=Image.open("logo4.png")
st.set_page_config(page_title="noThreads",page_icon=img)

db=sqlite3.connect("nothreads.db")
c=db.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY,password TEXT)''')

#theme
custom_css = """
<style>
body {
    color: white;
    background-color: black;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

#hide 
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


#logo
st.markdown("<center><img src=https://img.icons8.com/nolan/6000/email-sign.png; alt=centered image; height=200; width=200> </center>",unsafe_allow_html=True)


st.session_state.show_signup_form = True
textcolor= """
    <style>
    .gradient-text{
        background: linear-gradient(90deg, #1A6DFF,#C822FF,#6DC7FF,#E6ABFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family:cursive;color:#1A6DFF;text-align:center;font-size:32px;
    }
    </style>
    """
st.markdown(textcolor,unsafe_allow_html=True)
    
st.markdown('<p class="gradient-text">noThreads</p>', unsafe_allow_html=True)
st.subheader("Sign up :-")

username=st.text_input("",placeholder="Enter your Username")
password=st.text_input("",placeholder="Enter your Password",type="password")
   
signup=st.button("Sign up")
if signup:
    if not username  or not password :
        st.error("Please enter your full credentials")
    else:
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username,password))

        exiuser= c.fetchone()

        if exiuser:
              st.error("Username already taken !")

        else :
            query = "INSERT INTO users (username, password) VALUES (?, ?)"
     
            c.execute(query, (username, password))
            db.commit()
            st.success("Account created you may sign in now")
      
          
    
            
    

st.markdown(f"___")

st.markdown(f"Have an account ?[sign in now](https://nothreads.streamlit.app)")

    


