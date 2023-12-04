# from dotenv import load_dotenv
import os
from openai import OpenAI
import streamlit as st
import time

# load_dotenv()
API_KEY = os.environ['OPENAI_API_KEY']

client = OpenAI(api_key=API_KEY)

#thread id를 하나로 관리하기 위함
if 'thread_id' not in st.session_state:
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id

#thread_id, assistant_id 설정
thread_id = st.session_state.thread_id
#미리 만들어 둔 Assistant
assistant_id = "asst_8jhwuoPJibwLhyBApNgHYyvf"

# Streamlit 페이지 제목
st.title("💬 Kcosw.com Chatbot")
st.caption("🚀 A AI chatbot powered by CROBO Corp.")

# 초기 메시지 설정
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Do you want to buy Korean cosmetics wholesale?"}]

# 메시지를 화면에 표시
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 사용자 입력 받기
prompt = st.chat_input("Enter what you want to ask!")
if prompt:
    # 사용자의 메시지를 session_state에 추가
    st.session_state["messages"].append({"role": "user", "content": prompt})

    # OpenAI API를 통해 메시지 생성
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=prompt
    )

    # RUN을 돌리는 과정
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )

    with st.spinner('Waiting for response...'):
        # RUN이 completed 되었나 체크
        while run.status != "completed":
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )

    # 완료되었으니 메시지 불러오기
    messages = client.beta.threads.messages.list(
        thread_id=thread_id
    )
    # 마지막 메시지 UI에 추가
    response_content = messages.data[0].content[0].text.value
    st.session_state["messages"].append({"role": "assistant", "content": response_content})
