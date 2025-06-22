import streamlit as st
from openai import OpenAI
import re

# Show title and description.
st.title("🖋️ GPT 약관해석기: 복잡한 계약도 쉽게")
st.write(
    "복잡한 계약서를 쉽게! GPT가 중요한 조항을 요약해드립니다."
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
# 🔑 OpenAI API 키 입력받기
openai_api_key = st.text_input("🔑 OpenAI API Key를 입력하세요", type="password")

# 📄 계약서 입력 UI는 항상 보이게
st.subheader("📄 계약서 내용 입력")
uploaded_file = st.file_uploader("📂 파일 업로드 (.txt 권장)", type=["txt"])
text_input = st.text_area("또는 직접 계약서 내용을 붙여넣기", height=300)

# 📥 텍스트 추출
contract_text = ""
if uploaded_file:
    contract_text = uploaded_file.read().decode("utf-8")
elif text_input:
    contract_text = text_input

# 📤 분석 버튼
if st.button("🔍 계약서 분석하기"):
    if not openai_api_key:
        st.error("❗ OpenAI API 키를 입력해주세요.")
    elif not contract_text.strip():
        st.warning("계약서 내용을 입력하거나 파일을 업로드해주세요.")
    else:
        with st.spinner("GPT가 계약서를 분석 중입니다..."):
            import openai
            openai.api_key = openai_api_key

            prompt = f"""
다음 계약서를 조항 단위로 나누어 이해하기 쉽게 설명해줘.
- 각 조항은 '제1조', '제2조' 단위로 구분
- 각 조항 밑에 한 줄 요약 + 중요한 내용 요약
- 어려운 표현은 일상어로 바꾸기
- 법적 위험(일방 면책, 위약금, 자동 갱신 등)은 ⚠️로 강조. 일반인이 주의해야 할 위험 조항이 있으면 알려줘.

계약서 내용:
{contract_text}
"""
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "당신은 계약서를 해석해주는 전문가 AI입니다."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=1500,
                )

                DANGER_KEYWORDS = ["면책", "위약금", "일방적", "해지", "자동 갱신", "손해배상", "책임 없음"]

                def highlight_danger_keywords(text):
                    for keyword in DANGER_KEYWORDS:
                        text = re.sub(f"({keyword})", r"<span style='color:red; font-weight:bold;'>⚠️ \1</span>", text)
                    return text
    
                result = response.choices[0].message.content
                highlighted_result = highlight_danger_keywords(result)
                st.subheader("🧾 해석 결과")
                st.markdown(highlighted_result, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"GPT 호출 중 에러 발생: {e}")
