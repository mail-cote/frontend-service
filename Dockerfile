FROM python:3.9-slim

# 의존성 설치
RUN pip install --upgrade pip
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Streamlit 앱 복사
COPY . /app

# 워킹디렉토리 설정
WORKDIR /app

# 포트 설정
EXPOSE 8501

# Streamlit 실행
ENTRYPOINT ["streamlit", "run"]
CMD ["app.py", "--server.port=8501", "--server.address=0.0.0.0"]
