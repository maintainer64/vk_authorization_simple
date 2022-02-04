FROM python:3.8
WORKDIR /opt/app
COPY requirements.txt .
RUN apt-get update && apt-get install python3-dev \
                        gcc \
                        libc-dev -y
RUN pip install --upgrade pip -r requirements.txt
RUN python3 -m dostoevsky download fasttext-social-network-model
COPY . .
RUN chmod a+x *.sh
RUN find . -name __pycache__ -type d -exec rm -rv {} +
