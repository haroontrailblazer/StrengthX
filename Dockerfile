FROM python:3.13.8-slim
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL https://ollama.com/install.sh | sh
WORKDIR /main
COPY . /main
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8501
EXPOSE 11434
CMD ollama serve & \
    streamlit run main.py --server.port=8501 --server.address=0.0.0.0
