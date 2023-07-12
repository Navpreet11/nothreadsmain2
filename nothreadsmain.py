import streamlit as st
import sqlite3
from PIL import Image
from streamlit_option_menu import option_menu

img=Image.open("logo4.png")
st.set_page_config(page_title="noThreads",page_icon=img)

db=sqlite3.connect("nothreads.db")
c=db.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY,password TEXT)''')

c.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender TEXT NOT NULL,
        recipient TEXT NOT NULL,
        message TEXT NOT NULL,
        picture BLOB,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")
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

def main():
   
    if not is_user_logged_in():
        login()
    else:
        app()

def is_user_logged_in():
    return st.session_state.get('username') is not None
        
#main page
def login():
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
    st.subheader("Sign in :-")
    username=st.text_input("",placeholder="Username")
    password=st.text_input("",placeholder="Password",type="password")

    signin=st.button("Sign in")
    if signin:
        if not username  or not password :
            st.error("Please enter your full credentials")
        else:
            c.execute("SELECT *FROM users WHERE username=? AND password=?" ,(username,password))
            resu=c.fetchone()
            if resu:
                 set_user_logged_in(username)
                
            else:
                st.error("Invalid username or password !")
    st.markdown(f"___")


    st.markdown(f"Don't have an account yet ?[create one now](https://nothreadsup.streamlit.app)")

  
def set_user_logged_in(username):
    st.session_state.username = username
def app():
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
    nav = option_menu(menu_title=None,   options=["", " ","  ", "   ","    "],icons=["house-fill","search","person-fill", "gear-fill","chat-fill"],menu_icon="cast",default_index=0,orientation="horizontal",styles={
        "container": {"padding": "0!important", "background":"linear-gradient(90deg, #1A6DFF,#C822FF,#6DC7FF,#E6ABFF)"},
        "icon": {"color": "black", "font-size": "20px"}, 
        "nav-link": {"text-align":"left", "margin":"1px", "--hover-color": "#1c1c1c"},
        "nav-link-selected": {"background-color": "darkblue","color":"#1c1c1c"},})
            
    if nav =="":
        st.success("hello")

    elif nav==" ":
        st.success("search is here")
    else:
        chat_app()
def chat_app():
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
    
    st.markdown('<p class="gradient-text">Chat</p>', unsafe_allow_html=True)
   
    st.write("___")
    st.subheader("Choose a user to send message or see message")

   
    c.execute("SELECT username FROM users WHERE username != ?", (st.session_state.username,))
    recipients = [row[0] for row in c.fetchall()]

    recipient = st.selectbox("", recipients, key="recipient")
    st.write("____")
   
    message = st.text_input("",placeholder="Enter the Message you want to send to"+" "  +str(recipient), key="message")

    if st.button("Send message ➡️"):#and picture
         if message:
            insert_query = "INSERT INTO messages (sender, recipient, message) VALUES (?, ?, ?)"
            c.execute(insert_query, (st.session_state.username, recipient, message ))
            db.commit()
            st.success("Message sent successfully")
            
    st.write("___")
    
    if recipient:
        st.subheader(f" Your Chat History with {recipient} :-")
        query = "SELECT sender, message , timestamp FROM messages WHERE (sender = ? AND recipient = ?) OR (sender = ? AND recipient = ?) ORDER BY timestamp"
        c.execute(query, (st.session_state.username, recipient,recipient, st.session_state.username))
        chat_history = c.fetchall()
        for chat in chat_history:
             sender= chat[0]
             message = chat[1]
             timestamp = chat[2]
            
             
             if sender == st.session_state.username:
                 st.write("___")
                 displaychat(f"You: {message}")
                 st.success(f"sended on : {timestamp}")
            
             else:
                 st.write("___")
                 displayright(f"{sender}: {message} ")
                 st.info(f"received on : {timestamp}")
           
   



def send_message(sender, receiver, message,picture):
    query = "INSERT INTO messages (sender, receiver, message,picture) VALUES (?, ?, ?, ?)"#picture
    c.execute(query, (sender, receiver, message,picture.read() if picture else None ))
    db.commit()

def get_chat_history(username):
    query = "SELECT id, sender, receiver, message , picture FROM messages WHERE sender = ? OR receiver = ? ORDER BY timestamp"
    
    c.execute(query, (username, username))
    chat_history = c.fetchall()
    
    return chat_history

    
    
if __name__ == "__main__":
    
    main()
    c.close()
    db.close()

