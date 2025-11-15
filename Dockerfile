FROM python:3.13.8-slim
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*
WORKDIR /main
COPY . /main
COPY nginx.conf /etc/nginx/nginx.conf
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE ${PORT}
CMD ["sh", "-c", "streamlit run main.py --server.port=8501 --server.address=0.0.0.0 & nginx -g 'daemon off;'"]