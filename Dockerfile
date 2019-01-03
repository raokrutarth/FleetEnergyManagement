FROM python:3.5-slim
ADD ./app /app
ADD ./tests /tests
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
ENV FLASK_APP=app.py
# serve Flask app with gunicorn to spawn
# 5 web workers instead of sequential request processing
# use --reload to serve latest source code
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000", "--workers", "5", "--reload"]