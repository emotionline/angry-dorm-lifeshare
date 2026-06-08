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
            "id": 1,
            "등록시간": "2026-06-08 11:00",
            "모집품목": "쿠팡 우삼겹 1kg (두 팩 묶음)",
            "분할 방식": "각 500g씩 반띵!",
            "인당 금액": "6,500원",
            "픽업 장소": "은행사 상가 앞 벤치",
            "오픈채팅 주소": "https://open.kakao.com/o/demo1",
            "비밀번호": "1234"
        }
    ]
if "post_id_counter" not in st.session_state:
    st.session_state.post_id_counter = 2

# 3. 힙한 상단 배너 & 스토리텔링
st.title("🎤 쇼미더 반띵 : N분의 1 (Ban-Thing)")
st.markdown("### `\"우린 N분의 1, 생필품 나눠~ 🍚\"`")

# 🎵 쇼미더머니 N분의 1 BGM 에디션 (유튜브 오디오 임베드)
st.markdown("#### 🎧 배경음악 켜고 힙하게 반띵하기")
st.video("https://www.youtube.com/watch?v=jCHriYAr6Qw", loop=True)

st.info("""
🤝 **공주대 학우들을 위한 무수수료 순수 복지 웹입니다.**
매번 생필품 대용량으로 시키면 돈도 부담되고 방에 쌓아둘 공간도 없으셨죠? 가까운 사람들끼리 쪼개 쓰던 경험을 확장해서, 우리 학교 동기들 다 같이 지갑 지키자고 빌드했습니다. 편하게 모집 글을 올리고, 오픈채팅을 통해 만나서 반띵해보세요! 🚀
""")

# ⚠️ 사기 방지 가이드 및 경고 문구 (2번 요청사항)
with st.expander("🚨 안전한 반띵을 위한 필독 가이드 (사기 예방 안내)", expanded=False):
    st.warning("""
    **비해당/외부인 사기 및 먹튀 주의보**
    1. **에브리타임/학생증 인증 필수:** 오픈채팅방에 입장하면 서로 **공주대학교 학생 인증(합격증, 에타 캡처 등)**을 먼저 교환하시는 것을 강력히 권장합니다.
    2. **선입금 주의:** 물건을 직접 전달받거나 눈앞에서 확인할 때 정산하는 것이 가장 안전합니다. 거액일 경우 선입금을 지양해 주세요.
    3. **외부인 발견 시:** 우리 학교 학생이 아니거나 사기 정황이 의심될 경우 즉시 거래를 중단하고 에브리타임 핫게시판이나 경찰(112)에 신고하시기 바랍니다.
    
    *본 서비스는 오픈 플랫폼으로, 거래 과정에서 발생하는 학우 간의 분쟁이나 사기 피해에 대해 어떠한 법적 책임도 지지 않습니다. 서로 매너 있는 반띵 문화를 만들어가요!*
    """)

st.markdown("---")

# 4. 실시간 매칭 현황판 (1번 요청사항: 바로가기 링크 반영)
st.subheader("🔥 지금 올라온 실시간 반띵 모집")

if st.session_state.posts:
    df = pd.DataFrame(st.session_state.posts)
    
    # 데이터프레임에서 비밀번호와 ID, 원본 주소 숨기기
    display_df = df.drop(columns=["비밀번호", "id"])
    
    # 오픈채팅 주소 컬럼명을 '🔗 참여하기'로 변경하고 클릭 가능한 링크로 설정
    display_df = display_df.rename(columns={"오픈채팅 주소": "🔗 참여하기"})
    
    # st.dataframe의 column_config를 활용해 링크를 버튼/클릭 형태로 제공
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "🔗 참여하기": st.column_config.LinkColumn(
                "🔗 참여하기",
                help="클릭하면 오픈채팅방으로 바로 이동합니다!",
                display_text="오픈톡 입장 ↗"
            )
        }
    )
else:
    st.write("아직 올라온 소분 글이 없습니다. 첫 번째 글의 주인공이 되어보세요! 😎")

st.markdown("---")

# 5. 방장 전용: 모집 마감하기 기능 (1번 요청사항)
st.subheader("🔒 내가 올린 모집 마감하기 (닫기)")
with st.form("delete_form", clear_on_submit=True):
    col1, col2 = st.columns([2, 1])
    with col1:
        # 현재 활성화된 글 목록을 선택박스로 보여줌
        post_options = {f"[{p['등록시간']}] {p['모집품목']}": p['id'] for p in st.session_state.posts}
        selected_post_label = st.selectbox("마감할 방을 선택하세요", options=list(post_options.keys()))
    with col2:
        input_password = st.text_input("글 작설 시 비밀번호", type="password", placeholder="4자리 숫자")
        
    delete_submit = st.form_submit_button("🗑️ 해당 모집 마감 및 삭제하기")
    
    if delete_submit:
        if selected_post_label and input_password:
            target_id = post_options[selected_post_label]
            # 해당 ID의 게시글 찾기
            target_post = next((p for p in st.session_state.posts if p['id'] == target_id), None)
            
            if target_post and target_post['비밀번호'] == input_password:
                st.session_state.posts = [p for p in st.session_state.posts if p['id'] != target_id]
                st.success("🎉 성공적으로 모집이 마감되어 리스트에서 내렸습니다!")
                st.rerun()
            else:
                st.error("❌ 비밀번호가 일치하지 않거나 이미 삭제된 방입니다.")
        else:
            st.warning("방을 선택하고 비밀번호를 입력해 주세요.")

st.markdown("---")

# 6. 새로운 소분 모집 글 쓰기 폼 (비밀번호 입력 추가)
st.subheader("➕ 나도 같이 살 사람 모집하기")
with st.form("match_form", clear_on_submit=True):
    title = st.text_input("1. 어떤 물품을 나누실 건가요?", placeholder="예: 크리넥스 휴지 30롤, 세제 대용량 등")
    quantity = st.text_input("2. 어떻게 나누실 건가요?", placeholder="예: 3명이서 10롤씩 / 반띵!")
    price = st.text_input("3. 인당 예상 금액은 얼마인가요?", placeholder="예: 인당 3,500원")
    place = st.selectbox("4. 선호하는 픽업 장소는?", ["기숙사 로비/벤치", "학교 정문 앞", "공주대 후문/대학가", "자취방 근처 (상세 기재)"])
    contact = st.text_input("5. 카카오톡 오픈채팅방 링크 (필수)", placeholder="https://open.kakao.com/...")
    
    # 닫기 기능을 위한 비밀번호 설정 추가
    password = st.text_input("6. 방장 비밀번호 설정 (나중에 방을 닫을 때 사용합니다)", type="password", max_chars=4, placeholder="숫자 4자리")
    
    submit = st.form_submit_button("🚀 반띵 모집 글 올리기")
    
    if submit:
        if title and quantity and price and contact and password:
            # 주소 유효성 간단 체크
            if not contact.startswith("http"):
                st.error("링크는 http:// 또는 https:// 로 시작해야 합니다!")
            else:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
                new_post = {
                    "id": st.session_state.post_id_counter,
                    "등록시간": current_time,
                    "모집품목": title,
                    "분할 방식": quantity,
                    "인당 금액": price,
                    "픽업 장소": place,
                    "오픈채팅 주소": contact,
                    "비밀번호": password
                }
                st.session_state.posts.insert(0, new_post)
                st.session_state.post_id_counter += 1
                st.success("🎉 모집 글이 성공적으로 등록되었습니다! 에타 동기들이 곧 오픈카톡으로 달려옵니다!")
                st.balloons()
                st.rerun()
        else:
            st.warning("학우들이 정확히 보고 참여할 수 있도록 비밀번호를 포함한 모든 칸을 채워주세요! 🥺")

st.markdown("---")
st.caption("© 2026 공주대학교 학우가 만든 순수 복지 프로젝트 - Ban-Thing")
