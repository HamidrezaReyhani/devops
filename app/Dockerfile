FROM python:3.9-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

FROM python:3.9-slim
RUN useradd -m appuser
WORKDIR /home/appuser/app
COPY --from=builder /usr/local/lib/python3.9/site-packages /home/appuser/.local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /home/appuser/.local/bin
COPY --chown=appuser:appuser . .
ENV PATH="/home/appuser/.local/bin:${PATH}"
USER appuser
EXPOSE 5010
CMD ["python", "main.py"]