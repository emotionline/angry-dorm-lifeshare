import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. 페이지 레이아웃 및 테마 세팅
st.set_page_config(
    page_title="📦 공주대 기숙사 반띵(Ban-Thing)",
    page_icon="📦",
    layout="centered"
)

# 2. 구글 시트 데이터베이스 연결
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # 데이터 실시간 동기화를 위해 ttl=0 설정
    df_raw = conn.read(ttl=0)
except Exception as e:
    st.error("구글 시트 연결에 실패했습니다. Secrets 설정을 확인해주세요!")
    df_raw = pd.DataFrame(columns=["id", "reg_time", "title", "quantity", "price", "place", "contact", "password", "status"])

# 데이터가 비어있거나 status 열이 없는 경우를 대비한 방어 코드
if df_raw.empty:
    df_raw = pd.DataFrame(columns=["id", "reg_time", "title", "quantity", "price", "place", "contact", "password", "status"])
if "status" not in df_raw.columns:
    df_raw["status"] = "모집중"

# 3. 힙한 상단 배너 & 스토리텔링
st.title("🎤 쇼미더 반띵 : N분의 1 (Ban-Thing)")
st.markdown("### `\"우린 N분의 1, 생필품 짜치게 안 나눠~ 🍚\"`")

# 🎵 쇼미더머니 N분의 1 BGM 에디션 (유튜브 오디오 임베드)
st.markdown("#### 🎧 배경음악 켜고 힙하게 반띵하기")
st.markdown(
    '<iframe width="100%" height="120" src="https://www.youtube.com/embed/jCHriYAr6Qw" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
    unsafe_allow_html=True
)

st.info("""
🤝 **공주대 학우들을 위한 무수수료 순수 복지 웹입니다.**
모집 글을 올리고, 오픈채팅을 통해 만나서 반띵해보세요! 🚀
""")

# 🚨 안전 가이드
with st.expander("🚨 안전한 반띵을 위한 필독 가이드 (사기 예방)", expanded=False):
    st.warning("오픈채팅방에 입장하면 서로 **공주대학교 학생 인증(에타 캡처 등)**을 먼저 하시는 것을 강력히 권장합니다. 선입금은 가급적 지양하세요!")

st.markdown("---")

# 4. 실시간 매칭 현황판 (필터링 적용: '모집중'인 데이터만 표시)
st.subheader("🔥 지금 올라온 실시간 반띵 모집")

# 전체 데이터 중 status가 '모집중'인 것만 골라냅니다.
display_df_raw = df_raw[df_raw['status'] == "모집중"]

if not display_df_raw.empty and len(display_df_raw) > 0:
    # 사용자 화면에서는 관리용 데이터(id, password, status)를 숨깁니다.
    display_df = display_df_raw.drop(columns=["password", "id", "status"])
    
    display_df = display_df.rename(columns={
        "reg_time": "등록시간", "title": "모집품목", "quantity": "분할 방식",
        "price": "인당 금액", "place": "픽업 장소", "contact": "🔗 참여하기"
    })
    
    # 최신글 순으로 정렬
    display_df = display_df.iloc[::-1]
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "🔗 참여하기": st.column_config.LinkColumn(
                "🔗 참여하기", display_text="오픈톡 입장 ↗"
            )
        }
    )
else:
    st.write("현재 모집 중인 글이 없습니다. 첫 번째 글의 주인공이 되어보세요! 😎")

st.markdown("---")

# 5. 방장 전용: 모집 마감하기 기능 (삭제가 아닌 '상태 변경' 방식)
st.subheader("🔒 내가 올린 모집 마감하기 (닫기)")
with st.form("close_form", clear_on_submit=True):
    col1, col2 = st.columns([2, 1])
    with col1:
        # 모집중인 글만 선택지에 노출
        if not display_df_raw.empty:
            post_options = {f"[{row['reg_time']}] {row['title']}": row['id'] for _, row in display_df_raw.iterrows()}
            selected_post_label = st.selectbox("마감할 방을 선택하세요", options=list(post_options.keys()))
        else:
            selected_post_label = None
            st.selectbox("마감할 방을 선택하세요", options=["모집중인 방이 없습니다"], disabled=True)
            
    with col2:
        input_password = st.text_input("글 작성 시 비밀번호", type="password", placeholder="4자리 숫자")
        
    close_submit = st.form_submit_button("🏁 해당 모집 완료(마감) 처리하기")
    
    if close_submit and selected_post_label:
        target_id = post_options[selected_post_label]
        # 해당 행 찾기
        target_idx = df_raw[df_raw['id'] == target_id].index
        
        if not target_idx.empty and str(df_raw.loc[target_idx[0], 'password']) == str(input_password):
            # 💡 핵심: 행을 삭제하지 않고 status만 '마감'으로 바꿉니다.
            df_raw.loc[target_idx[0], 'status'] = "마감"
            conn.update(data=df_raw)
            st.success("🎉 모집이 완료되었습니다! 기록은 데이터베이스에 안전하게 보관됩니다.")
            st.rerun()
        else:
            st.error("❌ 비밀번호가 일치하지 않거나 이미 마감된 방입니다.")

st.markdown("---")

# 6. 새로운 모집 글 쓰기 (status='모집중'으로 시작)
st.subheader("➕ 나도 같이 살 사람 모집하기")
with st.form("match_form", clear_on_submit=True):
    title = st.text_input("1. 어떤 물품을 나누실 건가요?", placeholder="예: 크리넥스 휴지 30롤")
    quantity = st.text_input("2. 어떻게 나누실 건가요?", placeholder="예: 3명이서 10롤씩")
    price = st.text_input("3. 인당 예상 금액은?", placeholder="예: 3,500원")
    place = st.selectbox("4. 픽업 장소", ["기숙사 로비/벤치", "학교 정문 앞", "공주대 후문/대학가", "자취방 근처"])
    contact = st.text_input("5. 오픈채팅방 링크 (필수)", placeholder="https://open.kakao.com/...")
    password = st.text_input("6. 비밀번호 (4자리)", type="password", max_chars=4)
    
    submit = st.form_submit_button("🚀 모집 시작하기")
    
    if submit:
        if title and quantity and price and contact and password:
            if not contact.startswith("http"):
                st.error("링크는 http:// 로 시작해야 합니다!")
            else:
                next_id = int(df_raw['id'].max()) + 1 if not df_raw.empty and df_raw['id'].notna().any() else 1
                new_data = pd.DataFrame([{
                    "id": next_id,
                    "reg_time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "title": title, "quantity": quantity, "price": price, 
                    "place": place, "contact": contact, "password": password,
                    "status": "모집중" # 기본값은 모집중
                }])
                updated_df = pd.concat([df_raw, new_data], ignore_index=True)
                conn.update(data=updated_df)
                st.success("🎉 성공적으로 등록되었습니다!")
                st.balloons()
                st.rerun()
        else:
            st.warning("모든 칸을 채워주세요! 🥺")

st.markdown("---")
st.caption("© 2026 공주대학교 프로젝트 - Ban-Thing (Data History Enabled)")
