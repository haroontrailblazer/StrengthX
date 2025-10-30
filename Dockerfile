FROM python:3.13.8-slim

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL https://ollama.com/install.sh | sh

WORKDIR /main
COPY . /main
RUN pip install --no-cache-dir -r requirements.txt

# Start Ollama temporarily to allow pulling model
RUN ollama serve & sleep 5 && ollama pull haroontrailblazer/StrengthX-Dildo:V1

EXPOSE 8501
EXPOSE 11434

CMD ollama serve & \
    streamlit run main.py --server.port=8501 --server.address=0.0.0.0