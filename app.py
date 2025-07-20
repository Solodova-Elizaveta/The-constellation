import requests
import os
import streamlit as st
import streamlit.components.v1 as components



def back_start(user_promt):
    # API Configuration
    try:
        api_key = "sk-JmKQK2C3e4rqht2EftXXnKGXTtmZErOYubFLbPzfSLQ" #os.environ["LANGFLOW_API_KEY"]
    except: #KeyError:
        pass #raise ValueError("LANGFLOW_API_KEY environment variable not found. Please set your API key in the environment variables.")

    url = "http://localhost:7860/api/v1/run/8ffbd316-4b8d-4ff2-a36c-24a854503c7b"  # The complete API endpoint URL for this flow
    # Request payload configuration
    payload = {
        "output_type": "chat",
        "input_type": "chat",
        "input_value": user_promt
    }

    # Request headers
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key  # Authentication key from environment variable
    }

    try:
        # Send API request
        response = requests.request("POST", url, json=payload, headers=headers)
        response.raise_for_status()  # Raise exception for bad status codes
        ai_message = response.json()['outputs'][0]['outputs'][0]['results']['message']['data']['text']
        print(ai_message)
        return ai_message

        # Print response

    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}")
    except ValueError as e:
        print(f"Error parsing response: {e}")
    
    





st.set_page_config(page_title="AI Constellation", layout="centered")
menu = st.sidebar.radio("Меню", ["Главная", "О нас", "Контакты"])

if menu == "Главная":
    st.title("Hi, I'm AI Constellation!")
    st.write("Задай любой вопрос:")

    # Инициализируем историю сообщений
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Стили
    st.markdown("""
        <style>
        .chat-box {
            max-height: 500px;
            overflow-y: auto;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 10px;
            background-color: #f9f9f9;
            margin-bottom: 20px;
        }
        .message-user {
            background-color: #3F3F3F;
            color: white;
            padding: 10px 15px;
            border-radius: 10px;
            max-width: 90%;
            margin-left: auto;
            margin-bottom: 10px;
            word-wrap: break-word;
        }
        .message-bot {
            background-color: #ED2939;
            color: white;
            padding: 10px 15px;
            border-radius: 10px;
            max-width: 90%;
            margin-right: auto;
            margin-bottom: 10px;
            word-wrap: break-word;
        }
        </style>
    """, unsafe_allow_html=True)

    # Чат
    st.markdown('<div class="chat-box">', unsafe_allow_html=True)

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"<div class='message-user'><b>Вы:</b><br>{msg['content']}</div>", unsafe_allow_html=True)
        elif msg["role"] == "bot":
            st.markdown(f"<div class='message-bot'><b>AI Constellation:</b><br>{msg['content']}</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Якорь для прокрутки
    scroll_html = """
    <div id="scroll-target"></div>
    <script>
    const element = document.getElementById("scroll-target");
    if (element) {
        element.scrollIntoView({behavior: "smooth", block: "center"});
    }
    </script>
    """
    components.html(scroll_html, height=0)

    # Форма ввода
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("Ваш вопрос (до 300 символов):", max_chars=300)
        col2, col1= st.columns([5, 1])  # 4 к 1 по ширине
    with col1:
        submitted = st.form_submit_button("Отправить")
    with col2:
        clear = st.form_submit_button("🗑")
    if clear:
        st.session_state.messages = []
        st.rerun()
    

    if submitted and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        ai_response = f" {back_start(user_input)}"  # подключение модели здесь
        st.session_state.messages.append({"role": "bot", "content": ai_response})
        st.rerun()

elif menu == "О нас":
    st.title("О нас")
    st.write("Мы создаём сайты на Streamlit")

elif menu == "Контакты":
    st.title("Контакты")
    st.write("Напишите нам на почту: example@example.com")








