import requests
import os
import streamlit as st
import streamlit.components.v1 as components
import base64
import responce

  
api_key = 'sk-lp7vvr1mgDrGHaSF4wk9vtC6jQc_OpzVsRwAYNhB5O4'
url = 'http://localhost:7860/api/v1/run/1a6ef041-e006-41ac-8cff-3784d693c11b'
user_input = ''
resp = ''
st.sidebar.markdown("## YADRO")
menu = st.sidebar.radio("Меню", ["Главная", "наши продукты", "Контакты"])
if menu == "Главная":
    st.markdown("""
<div style="display: flex; align-items: center; gap: 10px;">
    <h1 style="margin: 0;">Hi, I'm FAQ_YADRO!</h1>
</div>
""", unsafe_allow_html=True)
    st.write("Задай любой вопрос:")

    # Инициализация
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "suggested_input" not in st.session_state:
        st.session_state.suggested_input = ""
    if "input_submitted" not in st.session_state:
        st.session_state.input_submitted = False

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
            margin-bottom: 10px;
            word-wrap: break-word;
        }
        .message-bot {
            background-color: #ED2939;
            color: white;
            padding: 10px 15px;
            border-radius: 10px;
            max-width: 400px;
            margin-right: auto;
            margin-bottom: 5px;
            word-wrap: break-word;
        }
                
</style>
    """, unsafe_allow_html=True)

    # Отображение сообщений и кнопок
    for idx, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            st.markdown(f"<div class='message-user'><b>Вы:</b><br>{msg['content']}</div>", unsafe_allow_html=True)

        elif msg["role"] == "bot":
            st.markdown(f"<div class='message-bot'><b>AI Constellation:</b><br>{msg['content']}</div>", unsafe_allow_html=True)

            # Кнопки-подсказки под ответом ИИ
            if idx >= 1 and st.session_state.messages[idx - 1]["role"] == "user":
                last_user_msg = st.session_state.messages[idx - 1][resp[2]]        #cюда api
                cols = st.columns(1)
                for i in range(1): 
                    with cols[i]:
                        if st.button(last_user_msg, key=f"suggest-{idx}-{i}"):
                            st.session_state.suggested_input = last_user_msg
                            st.session_state.input_submitted = False
                            st.rerun()

    # Прокрутка вниз
    components.html("""
        <div id="scroll-target"></div>
        <script>
        const element = document.getElementById("scroll-target");
        if (element) {
            element.scrollIntoView({behavior: "smooth", block: "center"});
        }
        </script>
    """, height=0)

    # Форма ввода
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("Ваш вопрос (до 300 символов):", max_chars=300, value=st.session_state.suggested_input)
        resp = responce.api_response(user_input,api_key,url)
        col2, col1 = st.columns([12, 1])
        with col1:
            clear = st.form_submit_button("🗑")
        with col2:
            submitted = st.form_submit_button("Отправить")

    if clear:
        st.session_state.messages = []
        st.session_state.suggested_input = ""
        st.session_state.input_submitted = False
        st.rerun()

    # Если форма отправлена — добавляем сообщение пользователя и ставим флаг ожидания
    if submitted and user_input and not st.session_state.input_submitted:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.waiting_for_response = True
        st.session_state.input_submitted = True
        st.session_state.suggested_input = ""
        st.rerun()

# Если флаг ожидания — показываем спиннер и добавляем ответ
    if st.session_state.get("waiting_for_response", False):
        with st.spinner("AI Constellation думает..."):
            import time
            time.sleep(1.5)  # можно убрать или заменить вызовом к ИИ
            ai_response = f"Ответ на: {st.session_state.messages[-1][resp[0]]}"  # тут подключай ИИ
            st.session_state.messages.append({"role": "bot", "content": ai_response})
            st.session_state.waiting_for_response = False
            st.session_state.input_submitted = False  # <--- добавлено
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








