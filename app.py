import streamlit as st
import pandas as pd
from datetime import datetime

# 1. 페이지 레이아웃 및 테마 세팅
st.set_page_config(
    page_title="📦 공주대 기숙사 반띵(Ban-Thing)", 
    page_icon="📦", 
    layout="centered"
)

# 2. 로컬 서버 세션에 실제 데이터 저장소 만들기 (새로고침 방지)
if "posts" not in st.session_state:
    st.session_state.posts = [
        {
            "등록시간": "2026-06-08 11:00",
            "모집품목": "쿠팡 우삼겹 1kg (두 팩 묶음)",
            "분할 방식": "각 500g씩 반띵!",
            "인당 금액": "6,500원",
            "픽업 장소": "은행사 상가 앞 벤치",
            "오픈채팅 주소": "https://open.kakao.com/o/demo1"
        },
        {
            "등록시간": "2026-06-08 09:30",
            "모집품목": "햇반 발아현미밥 24개입",
            "분할 방식": "6개씩 4명 구함",
            "인당 금액": "1,800원",
            "픽업 장소": "기숙사 비전관 로비",
            "오픈채팅 주소": "https://open.kakao.com/o/demo2"
        }
    ]

# 3. 힙한 상단 배너 & 스토리텔링
st.title("🎤 쇼미더 반띵 : N분의 1 (Ban-Thing)")
st.markdown("### `\"우린 N분의 1, 생필품 짜치게 안 나눠~ 🍚\"`")

st.info("""
🤝 **공주대 학우들을 위한 무수수료 순수 복지 웹입니다.**  
매번 생필품 대용량으로 시키면 돈도 부담되고 방에 쌓아둘 공간도 없으셨죠?  
가까운 사람들끼리 쪼개 쓰던 경험을 확장해서, 우리 학교 동기들 다 같이 지갑 지키자고 빌드했습니다.  
편하게 모집 글을 올리고, 오픈채팅을 통해 만나서 반띵해보세요! 🚀
""")

st.markdown("---")

# 4. 실시간 매칭 현황판
st.subheader("🔥 지금 올라온 실시간 반띵 모집")

if st.session_state.posts:
    df = pd.DataFrame(st.session_state.posts)
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.write("아직 올라온 소분 글이 없습니다. 첫 번째 글의 주인공이 되어보세요! 😎")

st.markdown("---")

# 5. 새로운 소분 모집 글 쓰기 폼
st.subheader("➕ 나도 같이 살 사람 모집하기")

with st.form("match_form", clear_on_submit=True):
    title = st.text_input("1. 어떤 물품을 나누실 건가요?", placeholder="예: 크리넥스 휴지 30롤, 세제 대용량 등")
    quantity = st.text_input("2. 어떻게 나누실 건가요?", placeholder="예: 3명이서 10롤씩 / 반띵!")
    price = st.text_input("3. 인당 예상 금액은 얼마인가요?", placeholder="예: 인당 3,500원")
    place = st.selectbox("4. 선호하는 픽업 장소는?", ["기숙사 로비/벤치", "학교 정문 앞", "공주대 후문/대학가", "자취방 근처 (상세 기재)"])
    contact = st.text_input("5. 카카오톡 오픈채팅방 링크 (필수)", placeholder="학우들이 타고 들어올 링크를 넣어주세요!")
    
    submit = st.form_submit_button("🚀 반띵 모집 글 올리기")

if submit:
    if title and quantity and price and contact:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        new_post = {
            "등록시간": current_time,
            "모집품목": title,
            "분할 방식": quantity,
            "인당 금액": price,
            "픽업 장소": place,
            "오픈채팅 주소": contact
        }
        st.session_state.posts.insert(0, new_post)
        st.success("🎉 모집 글이 성공적으로 등록되었습니다! 에타 동기들이 곧 오픈카톡으로 달려옵니다!")
        st.balloons() 
        st.rerun() 
    else:
        st.warning("학우들이 정확히 보고 참여할 수 있도록 모든 칸을 채워주세요! 🥺")

st.markdown("---")
st.caption("© 2026 공주대학교 능력자 학우가 만든 순수 복지 프로젝트 - Ban-Thing")
