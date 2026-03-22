from flask import Flask, request, send_file
from io import BytesIO
import base64
from datetime import datetime

app = Flask(__name__)

# Transparent 1x1 GIF
PIXEL = base64.b64decode("R0lGODlhAQABAIABAP///wAAACwAAAAAAQABAAACAkQBADs=")

@app.route("/tracker/pixel.gif")
def pixel():
    campaign = request.args.get("campaign", "unknown")
    user_id = request.args.get("user_id", "unknown")

    print("=== Tracking Pixel Request ===")
    print("Time:", datetime.utcnow().isoformat() + "Z")
    print("Campaign:", campaign)
    print("User ID:", user_id)
    print("IP Address:", request.remote_addr)
    print("User-Agent:", request.headers.get("User-Agent"))
    print("Referer:", request.headers.get("Referer"))
    print("=============================")

    return send_file(BytesIO(PIXEL), mimetype="image/gif")

if __name__ == "__main__":
    app.run(debug=True)