FROM python:3.13.8-slim
WORKDIR /main
COPY . /main
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE $PORT
CMD ["sh", "-c", "streamlit run main.py --server.port=$PORT --server.address=0.0.0.0 --client.showErrorDetails=false"] 