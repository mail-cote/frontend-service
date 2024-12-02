import streamlit as st
import sys
import os

# Python 검색 경로에 gRPC 파일 경로 추가
sys.path.append(os.path.abspath("../../member-service/member"))

import grpc
import member_pb2
import member_pb2_grpc

# Streamlit form
with st.form("user_input_form"):
    email = st.text_input("이메일 주소 입력")
    difficulty = st.selectbox("백준 티어 선택", ["Bronze5", "Bronze4", "Bronze3", "Bronze2", "Bronze1", 
                                           "Silver5", "Silver4", "Silver3", "Silver2", "Silver1", 
                                           "Gold5", "Gold4", "Gold3", "Gold2", "Gold1", 
                                           "Platinum5", "Platinum4", "Platinum3", "Platinum2", "Platinum1", 
                                           "Diamond5", "Diamond4", "Diamond3", "Diamond2", "Diamond1", 
                                           "Ruby5", "Ruby4", "Ruby3", "Ruby2", "Ruby1"
                                           ])
    submitted = st.form_submit_button("Submit")

if submitted:
    # gRPC communication
    try:
        channel = grpc.insecure_channel("member-service:50052")  # member-service 서버의 DNS 이름과 포트
        stub = member_pb2_grpc.MemberServiceStub(channel)
        request = member_pb2.MemberRequest(email=email, difficulty=difficulty)
        response = stub.SubmitMember(request)
        st.success(f"Response from server: {response.message}")
    except Exception as e:
        st.error(f"Failed to connect to gRPC server: {e}")
