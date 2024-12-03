FROM python:3.9-slim  

# 컨테이너 내에서 /app 디렉토리를 기본 작업 디렉토리로 설정
WORKDIR /app

# 컨테이너의 pip을 최신 버전으로 업그레이드
RUN pip install --upgrade pip

# app/requirements.txt 파일을 컨테이너의 /app 디렉토리로 복사
COPY ./frontend-service/app/requirements.txt /app/frontend-service/app/requirements.txt

# 파일(in 컨테이너)에 명시된 모든 python 패키지 설치
RUN pip install -r /app/frontend-service/app/requirements.txt

# 로컬 디렉토리의 모든 파일과 폴더를 컨테이너의 /app 디렉토리에 복사
COPY ./frontend-service ./frontend-service

# frontend-service 디렉터리로 이동하여 작업들 실행하기
WORKDIR /app/frontend-service/app

# 컨테이너의 8501 포트를 외부에 노출
EXPOSE 8501

# 컨테이너가 실행될 때 기본적으로 실행할 명령을 설정
ENTRYPOINT ["streamlit", "run"]

CMD ["app.py", "--server.port=8501", "--server.address=0.0.0.0"]
