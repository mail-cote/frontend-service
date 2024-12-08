import streamlit as st
import grpc
import member_pb2
import member_pb2_grpc
from PIL import Image


# gRPC 서버 연결 함수
def get_grpc_stub():
    # 변경된 gRPC 서버 주소: GKE에 맞게 수정
    channel = grpc.insecure_channel("member-service:50052")  # member 서버 포트
    return member_pb2_grpc.MemberServiceStub(channel)

# GetMemberByEmail - 이메일로 회원 ID 조회
def get_member_id(email):
    stub = get_grpc_stub()
    request = member_pb2.GetMemberByEmailRequest(email=email)
    response = stub.GetMemberByEmail(request)
    return response.member_id

# 1. CreateMemberRequest - 회원 등록
def create_member(email, level):
    stub = get_grpc_stub()
    request = member_pb2.CreateMemberRequest(
        member=member_pb2.Member(
            email=email,
            level=level,
            password=password  
        )
    )
    response = stub.CreateMember(request)
    return response.message


# 2. UpdateMemberRequest - 회원 정보 수정
def update_member(email, old_password, new_level, new_password):
    try:
        # 이메일로 회원 ID 조회
        member_id = get_member_id(email)
        stub = get_grpc_stub()
    
        request = member_pb2.UpdateMemberRequest(
            member_id=member_id,
            level=new_level,
            password=new_password,
            old_password=old_password  # 기존 비밀번호 추가(대조 위함!)
        )
        response = stub.UpdateMember(request)
        return response.message
    except Exception as e:
        raise RuntimeError(f"🚨 이메일 또는 비밀번호가 맞지 않아요.")


# 3. DeleteMemberRequest - 회원 삭제
def delete_member(email, password):
    try:
        # 이메일로 회원 ID 조회
        member_id = get_member_id(email)
        stub = get_grpc_stub()
        request = member_pb2.DeleteMemberRequest(
            member_id=member_id,
            old_password=old_password  # 기존 비밀번호 추가(대조 위함!)
        )
        response = stub.DeleteMember(request)
        return response.message
    except Exception as e:
        raise RuntimeError(f"🚨 이메일 또는 비밀번호가 맞지 않아요.")



######################    UI     ###########################

# 이미지 불러오기
pageIcon = Image.open("logo.png")
man = Image.open("man.png")
mail = Image.open("mail.png")
jandi = Image.open("jandi.png")

#Layout
st.set_page_config(
    page_title="매일코테 : 코딩테스트 문제 구독 서비스",
    layout="wide",
    page_icon=pageIcon,
    initial_sidebar_state="expanded")


#Data Pull and Functions
st.markdown("""
<style>
.big-font {
    font-size:80px !important;
}
</style>
""", unsafe_allow_html=True)

st.title("Mail-Cote")


st.title('🔔 매일코테, 코딩테스트 문제 구독 서비스 🔔')
st.divider()


# 1번째 
with st.container():
    col1,col2=st.columns(2)
    with col1:
        st.markdown('<h5>하루 한 문제로 꾸준히 성장하는 습관을 만들어보세요.</h5>', unsafe_allow_html=True)
    with col2:
        st.image(man)


st.divider()


with st.container():
    col1,col2=st.columns(2)
    with col1:
        st.image(mail)
    with col2:
        st.markdown('<h5>여러분의 실력에 맞는 백준 문제를 매일 7시에 보내드려요.</h5>', unsafe_allow_html=True)


st.divider()

st.title('🌱 매일코테로 깃허브 잔디를 빼곡히 채워봐요! 🌱') 




# 탭 UI
tabs = st.tabs(["구독하기", "마이페이지", "구독 해지"])


# 회원 등록
with tabs[0]:
    with st.form("create_member_form"):
        email = st.text_input("📍 Email")
        password = st.text_input("📍 Password")
        level = st.selectbox("📍 구독할 백준 티어", ["Bronze5", "Bronze4", "Bronze3", "Bronze2", "Bronze1", 
                                            "Silver5", "Silver4", "Silver3", "Silver2", "Silver1", 
                                            "Gold5", "Gold4", "Gold3", "Gold2", "Gold1", 
                                            "Platinum5", "Platinum4", "Platinum3", "Platinum2", "Platinum1", 
                                            "Diamond5", "Diamond4", "Diamond3", "Diamond2", "Diamond1", 
                                            "Ruby5", "Ruby4", "Ruby3", "Ruby2", "Ruby1"
                                            ])
        submitted = st.form_submit_button("구독하기")

    if submitted:
        try:
            # gRPC 서버로 데이터 전송
            response = create_member(email, level)
            st.success(f"{response}")  # Create 성공
        except Exception as e:
            st.error(f"🚨 Failed to connect to gRPC server: {e}")


# 회원 정보 수정
with tabs[1]:
    with st.form("update_member_form"):
        email = st.text_input("📍 Email")
        old_password = st.text_input("📍 이전 비밀번호", type="password")
        new_level = st.selectbox("📍 구독할 백준 티어", ["Bronze5", "Bronze4", "Bronze3", "Bronze2", "Bronze1", 
                                            "Silver5", "Silver4", "Silver3", "Silver2", "Silver1", 
                                            "Gold5", "Gold4", "Gold3", "Gold2", "Gold1", 
                                            "Platinum5", "Platinum4", "Platinum3", "Platinum2", "Platinum1", 
                                            "Diamond5", "Diamond4", "Diamond3", "Diamond2", "Diamond1", 
                                            "Ruby5", "Ruby4", "Ruby3", "Ruby2", "Ruby1"
                                            ])
        new_password = st.text_input("📍 새 비밀번호", type="password")
        submitted = st.form_submit_button("수정")
        if submitted:
            try:
                response = update_member(email, old_password, new_level, new_password)
                st.success(f"{response}")
            except Exception as e:
                st.error(f"{e}")


# 회원 삭제
with tabs[2]:
    with st.form("delete_member_form"):
        email = st.text_input("📍 Email")
        old_password = st.text_input("📍 Password", type="password")
        submitted = st.form_submit_button("해지")
        if submitted:
            try:
                response = delete_member(email, old_password)
                st.success(f"{response}")
            except Exception as e:
                st.error(f"{e}")



# 깃허브 버튼 추가
st.divider()
st.markdown(
    """
    <a href="https://github.com/mail-cote" target="_blank">
        <button style="padding:10px 20px; font-size:16px; cursor:pointer;">Mail-Cote Github</button>
    </a>
    """,
    unsafe_allow_html=True
)


# 작은 글씨 추가
st.markdown("""
---
<small>
Copyright © 2024, 매일코테. All rights reserved.<br>
이메일 myeunee@khu.ac.kr, plmko0914@gmail.com<br>
GDGoC KHU 1기 Backend - 송성훈, 허윤지
</small>
""", unsafe_allow_html=True)