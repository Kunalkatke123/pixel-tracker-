from flask import Flask, send_file, request
import logging
import datetime
import requests
import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# n8n webhook URL (from your info)
N8N_WEBHOOK_URL = "https://testn8n.doctorstech.in/webhook/pixel-open"

@app.route("/pixel/<email_id>.png")
def tracking_pixel(email_id):
    log_data = {
        "email_id": email_id,
        "ip": request.remote_addr,
        "user_agent": request.headers.get("User-Agent"),
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    app.logger.info(log_data)

    # Notify n8n workflow
    try:
        requests.post(N8N_WEBHOOK_URL, json=log_data, timeout=3)
    except Exception as e:
        app.logger.error(f"Failed to send data to n8n: {e}")

    # Return the transparent PNG
    return send_file("transperent.png", mimetype="image/png")

if __name__ == "__main__":
    # For local dev, but Render uses gunicorn
    app.run(host="0.0.0.0", port=8080)
