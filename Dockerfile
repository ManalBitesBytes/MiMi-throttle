FROM python:3.9-slim

RUN apt-get update -y && \
    apt install default-jdk libmagic-dev gcc curl -y

ENV AI_AUTH_DB_HOST ai_auth_db_host
ENV AI_AUTH_DB_NAME ai_auth_db_name
ENV AI_AUTH_DB_PASSWORD ai_auth_db_password
ENV AI_AUTH_DB_PORT ai_auth_db_port
ENV AI_AUTH_DB_USERNAME ai_auth_db_username
ENV ALLOWED_HOST allowed_host
ENV CSRF_TRUSTED_ORIGINS csrf_trusted_origins
ENV NOTIFICATION_SLACK_WEB_HOOK notification_slack_web_hook
ENV TIKA_SERVER_ENDPOINT tika_server_endpoint

COPY . /app
WORKDIR /app


RUN pip3 install -r requirements.txt

# CV Parser
# Install ffmpeg, a tool for handling multimedia files. -> we use it to convert any voice to .wav to make speech recognition deal with it
# Install Tesseract OCR, an optical character recognition tool -> we use it to extract text from images
RUN apt-get update && apt-get install -y poppler-utils
RUN apt-get update && apt-get install -y tesseract-ocr
RUN apt-get install -y tesseract-ocr-ara
RUN apt-get install -y tesseract-ocr-eng

# CV Parser: Install spaCy model, pdfplumber, and LibreOffice Writer
RUN python -m spacy download en_core_web_sm && \
    python -m pip install pdfplumber==0.11.2 && \
    apt-get install -y libreoffice-writer

# Download Tika Requirements
# Download Tika Server manually
RUN curl -L -o /tmp/tika-server.jar https://archive.apache.org/dist/tika/tika-server-2.9.0.jar

#RUN python3 manage.py makemigrations && python3 manage.py migrate

#EXPOSE 8001

CMD ["gunicorn", "-w", "6", "-b", ":8000", "-t", "360", "--log-level", "DEBUG", "ai_services_apis.wsgi:application"]