import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("🖋️ GPT 약관해석기: 복잡한 계약도 쉽게")
st.write(
    "복잡한 계약서를 쉽게! GPT가 중요한 조항을 요약해드립니다."
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("🔑 OpenAI API Key를 입력하세요", type="password")

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Let the user upload a file via `st.file_uploader`.
    st.subheader("📄 계약서 내용 입력")
    uploaded_file = st.file_uploader(
        "📂 파일 업로드 (.txt or .md)", type=("txt", "md")
    )
    text_input = st.text_area("또는 직접 계약서 내용을 붙여넣기", height=300)

    # 텍스트 추출
    contract_text = ""
    if uploaded_file:
        contract_text = uploaded_file.read().decode("utf-8")
    elif text_input:
        contract_text = text_input

    # 분석 버튼
    # 분석 버튼
    if contract_text and st.button("🔍 계약서 분석하기"):
        with st.spinner("GPT가 계약서를 분석 중입니다..."):

            prompt = f"""
다음 계약서 조항을 이해하기 쉽게 요약하고, 일반인이 주의해야 할 위험 조항이 있으면 따로 알려줘.
- 각 조항을 짧게 요약
- 어려운 표현은 일상어로 바꾸기
- 법적 위험(일방 면책, 위약금, 자동 갱신 등)은 ⚠️로 강조

계약서 내용:
{contract_text}
"""

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o",  # 또는 "gpt-3.5-turbo"
                    messages=[
                        {"role": "system", "content": "당신은 계약서를 해석해주는 전문가 AI입니다."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=1500,
                )
                result = response.choices[0].message.content
                st.subheader("🧾 해석 결과")
                st.markdown(result)

            except Exception as e:
                st.error(f"GPT 호출 중 에러 발생: {e}")
