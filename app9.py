# -*- coding: utf-8 -*-
"""Untitled19.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/11rKABDhI4ACmm76amjfgsOGH-2CU_crd
"""

import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# 임베딩 모델 로드
encoder = SentenceTransformer('jhgan/ko-sroberta-multitask')

# 식당 관련 질문과 답변 데이터
questions = [
    "전체 조원이 몇명인가요?",
    "조원들이 이름을 알려주세요?",
    "포트폴리오의 주제가 뭔가요?",
]

answers = [
    "4명입니다..",
    "서동현, 경진우, 노승욱, 이원석 입니다.",
    "운동을 하는 동작을 보고 바른 자세로 교정해주는 서비스 입니다.",
]

# 질문 임베딩과 답변 데이터프레임 생성
question_embeddings = encoder.encode(questions)
df = pd.DataFrame({'question': questions, '챗봇': answers, 'embedding': list(question_embeddings)})

# 대화 이력을 저장하기 위한 Streamlit 상태 설정
if 'history' not in st.session_state:
    st.session_state.history = []

# 챗봇 함수 정의
def get_response(user_input):
    # 사용자 입력 임베딩
    embedding = encoder.encode(user_input)

    # 유사도 계산하여 가장 유사한 응답 찾기
    df['distance'] = df['embedding'].map(lambda x: cosine_similarity([embedding], [x]).squeeze())
    answer = df.loc[df['distance'].idxmax()]

    # 대화 이력에 추가
    st.session_state.history.append({"user": user_input, "bot": answer['챗봇']})

# Streamlit 인터페이스
st.title("식당 챗봇")
st.write("한식당에 관한 질문을 입력해보세요. 예: 영업시간이 어떻게 되나요?")

user_input = st.text_input("user", "")

if st.button("Submit"):
    if user_input:
        get_response(user_input)
        user_input = ""  # 입력 초기화

# 대화 이력 표시
for message in st.session_state.history:
    st.write(f"**사용자**: {message['user']}")
    st.write(f"**챗봇**: {message['bot']}")

