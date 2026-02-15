from flask import Blueprint, Response
from src.obd.obd_reader import get_latest_telemetry
import json
import time

api = Blueprint("api", __name__)

@api.route("/stream")
def stream():
    def event_stream():
        while True:
            data = get_latest_telemetry()
            yield f"data: {json.dumps(data)}\n\n"
            time.sleep(0.3)
    return Response(event_stream(), mimetype="text/event-stream")
