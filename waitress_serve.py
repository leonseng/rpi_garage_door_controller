import os

from waitress import serve

import app


SERVE_HOST = os.environ.get("RPI_GARAGE_DOOR_CONTROLLER_HOST", "127.0.0.1")
SERVE_PORT = os.environ.get("RPI_GARAGE_DOOR_CONTROLLER_PORT", "8080")

serve(app.app, host=SERVE_HOST, port=SERVE_PORT)
