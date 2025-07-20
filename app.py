import requests
import os
import streamlit as st
import streamlit.components.v1 as components
import base64



def back_start(user_promt):
    # API Configuration
    try:
        api_key = "sk-lp7vvr1mgDrGHaSF4wk9vtC6jQc_OpzVsRwAYNhB5O4" #os.environ["LANGFLOW_API_KEY"]
    except: #KeyError:
        pass #raise ValueError("LANGFLOW_API_KEY environment variable not found. Please set your API key in the environment variables.")

    url = "http://localhost:7860/api/v1/run/1a6ef041-e006-41ac-8cff-3784d693c11b"  # The complete API endpoint URL for this flow
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
    
    





logo_path = os.path.abspath("logo.png")  # путь к логотипу (PNG, SVG и т.п.)
try:
    st.sidebar.image(logo_path, use_container_width=True)
except Exception as e:
    st.sidebar.error(f"Ошибка загрузки логотипа: {str(e)}")
st.set_page_config(page_title="AI Constellation", layout="centered")

menu = st.sidebar.radio("Меню", ["Главная", "наши продукты", "Контакты"])

if menu == "Главная":
    st.title("Hi, I'm AI Constellation!")
    st.write("Задай любой вопрос:")

    # Инициализируем историю сообщений
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Стили
    st.markdown("""
        <style>
        .message-user {
            background-color: #3F3F3F;
            color: white;
            padding: 10px 15px;
            border-radius: 10px;
            max-width: 400px;
            margin-left: auto;
            margin-bottom: 40px;
            word-wrap: break-word;
        }
        .message-bot {
            background-color: #ED2939;
            color: white;
            padding: 10px 15px;
            border-radius: 10px;
            max-width: 400px;
            margin-right: auto;
            margin-bottom: 40px;
            word-wrap: break-word;
        }
                
      <style>
    /* Увеличиваем ширину сайдбара */
    [data-testid="stSidebar"] {
        width: 300px !important;
        min-width: 300px !important;
    }

    /* Чтобы основной блок не сжимался */
    .main .block-container {
        padding-left: 3rem;
        padding-right: 3rem;
    }
    </style>
                
    """, unsafe_allow_html=True)

    # Чат
    

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
        col2, col1= st.columns([12, 1])  # 12 к 1 по ширине
    with col1:
        clear = st.form_submit_button("🗑")
    if clear:
        st.session_state.messages = []
        st.rerun()
    with col2:
        submitted = st.form_submit_button("Отправить")
    

    if submitted and user_input:
        
        st.session_state.messages.append({"role": "user", "content": user_input})
        ai_response = f" {back_start(user_input)}"  # подключение модели здесь
        st.session_state.messages.append({"role": "bot", "content": ai_response})
        st.rerun()


elif menu == "наши продукты":
    st.markdown("""
        <style>
        .product-wrapper {
            background-color: #e0e0e0;
            border-radius: 12px;
            padding: 30px;
            margin: 20px 0;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        .product-wrapper:hover {
            background-color: #f0f0f0;
            transform: scale(1.03);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }
        .product-img {
            width: 1800px;
            border-radius: 12px;
            margin-bottom: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("Наши продукты")

    for i in range(1, 6):
        # Пробуем .jpg, .jpeg, .png — по очереди
        for ext in ["jpg", "jpeg", "png"]:
            image_path = f"product{i}.{ext}"
            if os.path.exists(image_path):
                with open(image_path, "rb") as img_file:
                    img_base64 = base64.b64encode(img_file.read()).decode()
                mime = "jpeg" if ext in ["jpg", "jpeg"] else "png"
                st.markdown(f"""
                    <div class='product-wrapper'>
                        <img src='data:image/{mime};base64,{img_base64}' class='product-img' />
                        Продукт {i}
                    </div>
                """, unsafe_allow_html=True)
                break
        else:
            st.markdown(f"""
                <div class='product-wrapper'>
                    <div style='color: red;'>Изображение product{i}.jpg/jpeg/png не найдено</div>
                    Продукт {i}
                </div>
            """, unsafe_allow_html=True)

elif menu == "Контакты":
    st.title("Контакты")
    st.write("Напишите нам на почту: example@example.com")








