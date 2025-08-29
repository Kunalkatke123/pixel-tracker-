from flask import Flask, send_file, request
import logging
import datetime
import requests
import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# n8n webhook URL (from your info)
N8N_WEBHOOK_URL = "https://testn8n.doctorstech.in/webhook/Pixel-open"

# Track already-seen email_ids
seen_emails = set()

@app.route("/pixel/<email_id>.png")
def tracking_pixel(email_id):
    log_data = {
        "email_id": email_id,
        "ip": request.remote_addr,
        "user_agent": request.headers.get("User-Agent"),
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    app.logger.info(f"Pixel opened: {log_data}")

    # Only send webhook on first open
    if email_id not in seen_emails:
        seen_emails.add(email_id)
        try:
            requests.post(N8N_WEBHOOK_URL, json=log_data, timeout=3)
            app.logger.info(f"Webhook sent for {email_id}")
        except Exception as e:
            app.logger.error(f"Failed to send data to n8n: {e}")
    else:
        app.logger.info(f"Duplicate open ignored for {email_id}")

    # Return the transparent PNG
    return send_file("transperent.png", mimetype="image/png")

if __name__ == "__main__":
    # For local dev, but Render uses gunicorn
    app.run(host="0.0.0.0", port=8080)
