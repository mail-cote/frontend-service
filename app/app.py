import streamlit as st
import sys
import os

# Python 검색 경로에 gRPC 파일 경로 추가
sys.path.append(os.path.abspath("../../member-service/member"))

import grpc
import member_pb2
import member_pb2_grpc


def send_request(email, level):
    # gRPC 서버 연결
    channel = grpc.insecure_channel("localhost:50052")  # 서버 포트 확인
    stub = member_pb2_grpc.MemberServiceStub(channel)

    # CreateMemberRequest 메시지 생성
    request = member_pb2.CreateMemberRequest(
        member=member_pb2.Member(
            email=email,
            level=level,
            password="default_password"  # 비밀번호는 예제로 고정값
        )
    )

    # gRPC 요청 보내기
    response = stub.CreateMember(request)
    return response.message


st.title("Mail-Cote")

# 클라이언트 입력 폼
with st.form("user_input_form"):
    email = st.text_input("이메일 주소 입력")
    level = st.selectbox("백준 티어 선택", ["Bronze5", "Bronze4", "Bronze3", "Bronze2", "Bronze1", 
                                           "Silver5", "Silver4", "Silver3", "Silver2", "Silver1", 
                                           "Gold5", "Gold4", "Gold3", "Gold2", "Gold1", 
                                           "Platinum5", "Platinum4", "Platinum3", "Platinum2", "Platinum1", 
                                           "Diamond5", "Diamond4", "Diamond3", "Diamond2", "Diamond1", 
                                           "Ruby5", "Ruby4", "Ruby3", "Ruby2", "Ruby1"
                                           ])
    submitted = st.form_submit_button("Submit")

if submitted:
    try:
        # gRPC 서버로 데이터 전송
        response = send_request(email, level)
        st.success(f"Server Response: {response}")
    except Exception as e:
        st.error(f"Failed to connect to gRPC server: {e}")
