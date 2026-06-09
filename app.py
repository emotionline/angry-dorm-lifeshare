import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import gspread

# 1. 페이지 레이아웃을 wide(전체 화면)로 변경하여 영상과 화면을 시원하게 키웁니다!
st.set_page_config(
    page_title="📦 공주대 기숙사 반띵(Ban-Thing)", 
    page_icon="📦", 
    layout="wide"
)

# 구글 시트 원본 주소 및 정보 정의
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1opCa9vpXP5N-FC1r6_IQe7zgUaT8U1OyGko9C4IkttA/edit"
WORKSHEET_NAME = "Sheet1"
DEFAULT_COLUMNS = ["id", "reg_time", "title", "quantity", "price", "place", "contact", "password", "status"]

# 2. 구글 시트 데이터베이스 연결 및 에러 안전장치 (데이터 읽기)
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_raw = conn.read(spreadsheet=SPREADSHEET_URL, worksheet=WORKSHEET_NAME, ttl=0)
    
    # 시트가 완전히 비어있거나 데이터가 없으면 기본 구조로 강제 초기화
    if df_raw is None or df_raw.empty:
        df_raw = pd.DataFrame(columns=DEFAULT_COLUMNS)
except Exception as e:
    st.error("구글 시트 연결에 실패했습니다. 공유 권한 및 URL을 확인해주세요!")
    df_raw = pd.DataFrame(columns=DEFAULT_COLUMNS)

# 혹시 특정 컬럼이 누락되었다면 자동 채워주기
for col in DEFAULT_COLUMNS:
    if col not in df_raw.columns:
        df_raw[col] = "모집중" if col == "status" else ""

# id 컬럼 숫자형으로 안전하게 변환
if not df_raw.empty:
    df_raw['id'] = pd.to_numeric(df_raw['id'], errors='coerce').fillna(0).astype(int)

# 3. 힙한 상단 배너 & 스토리텔링
st.title("🎤 쇼미더 반띵 : N분의 1 (Ban-Thing)")
st.markdown("### `\"우린 N분의 1, 생필품 짜치게 안 나눠~ 🍚\"`")
st.markdown("#### 🎧 배경음악 켜고 힙하게 반띵하기")

# 유튜브 배경음악 임베드
st.markdown(
    '<iframe width="100%" height="500" src="https://www.youtube.com/embed/jCHriYAr6Qw" '
    'frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" '
    'allowfullscreen style="border-radius:12px; box-shadow: 0px 4px 15px rgba(0,0,0,0.3);"></iframe>', 
    unsafe_allow_html=True
)

st.info("""
🤝 **공주대 학우들을 위한 무수수료 순수 복지 웹입니다.** 내가 직접 방장이 되어 모집 글을 올리고, 오픈채팅을 통해 기숙사 로비에서 만나 스웩 넘치게 반띵해보세요! 🚀
""")

# 🚨 안전 가이드
with st.expander("🚨 안전한 반띵을 위한 필독 가이드 (사기 예방)", expanded=True):
    st.warning(
        "**[외부인 및 사기 방지 필수 룰]**\n\n"
        "1. 오픈채팅방에 입장하면 서로 **공주대학교 학생 인증(에브리타임 합격/재학 인증 캡처 또는 모바일 학생증)**을 가장 먼저 확인하시는 것을 강력히 권장합니다!\n"
        "2. 물품을 실제로 전달받기 전 과도한 선입금은 지양해 주시고, 기숙사 로비 등 안전한 공공장소에서 대면 거래를 권장합니다.\n"
        "3. 본 플랫폼은 학우 간 연결만을 돕는 복지 서비스로, 거래 과정에서 발생하는 분쟁이나 사기 피해에 대해 어떠한 법적 책임도 지지 않습니다."
    )

st.markdown("---")

# 4. 실시간 매칭 현황판
st.subheader("🔥 지금 올라온 실시간 반띵 모집")

# 모집중인 데이터만 필터링
display_df_raw = df_raw[df_raw['status'] == "모집중"]

if not display_df_raw.empty and len(display_df_raw) > 0:
    # 사용자에게 보여줄 데이터 정제
    display_df = display_df_raw.drop(columns=["password", "id", "status"], errors='ignore')
    display_df = display_df.rename(columns={
        "reg_time": "등록시간", 
        "title": "물품", 
        "quantity": "방 인원 수", 
        "price": "인당 예상 금액", 
        "place": "픽업 장소", 
        "contact": "🔗 참여하기"
    })
    # 최신 글이 맨 위로 오도록 정렬
    display_df = display_df.iloc[::-1]
    
    st.dataframe(
        display_df, 
        use_container_width=True, 
        hide_index=True, 
        column_config={
            "🔗 참여하기": st.column_config.LinkColumn("🔗 참여하기", display_text="오픈톡 입장 ↗")
        }
    )
else:
    st.info("현재 모집 중인 글이 없습니다. 아래 폼에서 첫 번째 글의 주인공이 되어보세요! 😎")

st.markdown("---")

# 5. 방장 전용: 모집 마감하기 기능
st.subheader("🔒 내가 올린 모집 마감하기 (닫기)")

with st.form("close_form", clear_on_submit=True):
    col1, col2 = st.columns([2, 1])
    with col1:
        if not display_df_raw.empty and len(display_df_raw) > 0:
            post_options = {f"[{row['reg_time']}] {row['title']}": row['id'] for _, row in display_df_raw.iterrows()}
            selected_post_label = st.selectbox("마감할 방을 선택하세요", options=list(post_options.keys()))
        else:
            selected_post_label = None
            st.selectbox("마감할 방을 선택하세요", options=["모집중인 방이 없습니다"], disabled=True)
            
    with col2:
        input_password = st.text_input("글 작성 시 비밀번호", type="password", placeholder="4자리 숫자")
        
    close_submit = st.form_submit_button("🏁 해당 모집 완료(마감) 처리하기")
    
    if close_submit:
        if not selected_post_label:
            st.warning("마감할 방이 없습니다.")
        elif not input_password:
            st.warning("비밀번호를 입력해주세요.")
        else:
            target_id = post_options[selected_post_label]
            target_idx = df_raw[df_raw['id'] == target_id].index
            
            if not target_idx.empty and str(df_raw.loc[target_idx[0], 'password']) == str(input_password):
                df_raw.loc[target_idx[0], 'status'] = "마감"
                
                # 링크 편집자 권한을 활용한 직접 우회 업데이트 (st-gsheets 제약 우회)
                try:
                    # gspread의 기본 클라이언트를 활용해 공개 링크용으로 강제 접근 처리
                    gc = gspread.client.Client(auth=None)
                    sh = gc.open_by_url(SPREADSHEET_URL)
                    worksheet = sh.worksheet(WORKSHEET_NAME)
                    
                    # 데이터 프레임을 리스트 형태로 변환하여 시트 덮어쓰기
                    df_as_list = [df_raw.columns.values.tolist()] + df_raw.fillna("").values.tolist()
                    worksheet.update('A1', df_as_list)
                    
                    st.success("🎉 모집이 완료되었습니다! 목록이 실시간으로 업데이트됩니다.")
                    st.rerun()
                except Exception as update_err:
                    st.error(f"마감 처리 중 구글 시트 반영에 실패했습니다. (원인: {update_err})")
            else:
                st.error("❌ 비밀번호가 일치하지 않습니다! 방장이 맞으신지 확인해주세요. 😭")

st.markdown("---")

# 6. 새로운 모집 글 쓰기
st.subheader("➕ 나도 같이 살 사람 모집하기")

with st.form("match_form", clear_on_submit=True):
    title = st.text_input("1번 : 물품", placeholder="예: 크리넥스 휴지 30롤, 햇반 24개입")
    quantity = st.text_input("2번 : 방 인원 수", placeholder="예: 총 3명 (나 포함), 반띵(2명)")
    price = st.text_input("3번 : 인당 예상 금액", placeholder="예: 3,500원")
    place = st.text_input("4번 : 픽업 장소", placeholder="예: 비전하우스 로비, 드림하우스 앞 벤치")
    contact = st.text_input("5번 : 오픈채팅방 링크", placeholder="https://open.kakao.com/...")
    password = st.text_input("6번 : 비밀번호 4자리 (방 마감할 때 방장에게 필요합니다.)", type="password", max_chars=4, placeholder="숫자 4자리")
    
    submit = st.form_submit_button("🚀 모집 시작하기")
    
    if submit:
        if title and quantity and price and place and contact and password:
            if not contact.startswith("http"):
                st.error("오픈채팅방 링크는 http:// 또는 https:// 로 시작해야 합니다!")
            else:
                # 안전하게 새 ID 생성
                next_id = int(df_raw['id'].max() + 1) if not df_raw.empty and df_raw['id'].notna().any() else 1
                
                new_row = [
                    next_id, 
                    datetime.now().strftime("%Y-%m-%d %H:%M"), 
                    title, 
                    quantity, 
                    price, 
                    place, 
                    contact, 
                    password, 
                    "모집중"
                ]
                
                # 링크 편집자 권한을 활용한 직접 우회 데이터 추가 (st-gsheets 제약 우회)
                try:
                    gc = gspread.client.Client(auth=None)
                    sh = gc.open_by_url(SPREADSHEET_URL)
                    worksheet = sh.worksheet(WORKSHEET_NAME)
                    
                    # 맨 아래 행에 데이터 꽂아넣기
                    worksheet.append_row(new_row)
                    
                    st.success("🎤 반띵 모집 스웩 넘치게 등록 완료! 현황판을 확인하세요!")
                    st.balloons()
                    st.rerun()
                except Exception as append_err:
                    st.error(f"데이터 등록 중 구글 시트 반영에 실패했습니다. (원인: {append_err})")
        else:
            st.warning("모든 칸을 채워주세요! 학우들이 기다립니다. 🥺")

st.markdown("---")
st.caption("<p style='text-align: center; color: gray;'>© 2026 공주대학교 프로젝트 - Ban-Thing (Data History Enabled)</p>", unsafe_allow_html=True)
