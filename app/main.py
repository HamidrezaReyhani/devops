from flask import Flask, jsonify
import os
import psycopg2
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import logging
import socket
import json
import time
import threading

app = Flask(__name__)

# تنظیمات دیتابیس
DB_HOST = os.getenv("DB_HOST", "postgres")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")

# تنظیمات Logstash
LOGSTASH_HOST = os.getenv("LOGSTASH_HOST", "logstash")
LOGSTASH_PORT = int(os.getenv("LOGSTASH_PORT", 4000))
RETRY_DELAY = 5  # ثانیه

# راه‌اندازی لاگر داخلی پایتون (برای نمایش کنسول)
logger = logging.getLogger("flask-app")
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger.addHandler(console_handler)

# اتصال و ارسال لاگ به Logstash با فرمت JSON خطی (در Thread جدا)
class LogstashJsonLogger:
    def __init__(self, host, port, retry_delay=5):
        self.host = host
        self.port = port
        self.retry_delay = retry_delay
        self.sock = None
        self.connected = False
        self.lock = threading.Lock()
        self.connect_thread = threading.Thread(target=self.connect_loop, daemon=True)
        self.connect_thread.start()

    def connect_loop(self):
        while not self.connected:
            try:
                self.sock = socket.create_connection((self.host, self.port))
                logger.info(f"Connected to Logstash at {self.host}:{self.port}")
                self.send_log({"message": "Connected to Logstash", "level": "INFO"})
                self.connected = True
            except Exception as e:
                logger.error(f"Failed to connect to Logstash: {e}. Retrying in {self.retry_delay} seconds...")
                time.sleep(self.retry_delay)

    def send_log(self, log_dict):
        if not self.connected:
            logger.info(f"Logstash not connected, skipping log: {log_dict}")
            return
        try:
            log_dict["@timestamp"] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            if "level" not in log_dict:
                log_dict["level"] = "INFO"
            line = json.dumps(log_dict) + "\n"
            with self.lock:  # جلوگیری از همزمانی در ارسال
                self.sock.sendall(line.encode("utf-8"))
        except Exception as e:
            logger.error(f"Error sending log to Logstash: {e}. Reconnecting...")
            self.connected = False
            self.connect_thread = threading.Thread(target=self.connect_loop, daemon=True)
            self.connect_thread.start()

# نمونه از لاگر JSON
logstash_logger = LogstashJsonLogger(LOGSTASH_HOST, LOGSTASH_PORT, RETRY_DELAY)

# Wrapper ساده برای ارسال لاگ‌ها
def log_info(message, **extra):
    logstash_logger.send_log({"message": message, "level": "INFO", **extra})

def log_error(message, **extra):
    logstash_logger.send_log({"message": message, "level": "ERROR", **extra})

# متریک‌ها
REQUEST_COUNT = Counter('app_requests_total', 'Total number of requests')
DB_QUERY_COUNT = Counter('db_queries_total', 'Total number of DB queries')

@app.route("/health")
def health():
    REQUEST_COUNT.inc()
    log_info("Health check endpoint called", endpoint="/health")
    return jsonify({"status": "healthy"})

@app.route("/data")
def data():
    REQUEST_COUNT.inc()
    log_info("Data endpoint called", endpoint="/data")
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cur = conn.cursor()
        cur.execute("SELECT NOW();")
        DB_QUERY_COUNT.inc()
        result = cur.fetchone()
        cur.close()
        conn.close()
        log_info("DB query executed successfully", db_time=str(result[0]))
        return jsonify({"db_time": str(result[0])})
    except Exception as e:
        log_error("DB query failed", error=str(e))
        return jsonify({"error": str(e)}), 500

@app.route("/metrics")
def metrics():
    log_info("Metrics endpoint called", endpoint="/metrics")
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    log_info("Starting Flask app...")
    app.run(host="0.0.0.0", port=5010)
