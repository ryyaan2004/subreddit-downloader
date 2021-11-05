FROM python:3.8-slim
RUN useradd --create-home --shell /bin/bash app_user
WORKDIR /home/app_user
RUN pip install pipenv && \
    mkdir -p /out && \
    chown app_user:app_user /out

COPY Pipfile ./
RUN pipenv lock --requirements > requirements.txt && \
    pip install --no-cache-dir -r requirements.txt

USER app_user
COPY downloader/* ./

ENTRYPOINT ["python", "downloader.py"]