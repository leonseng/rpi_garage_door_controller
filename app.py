from enum import Enum
import json
import logging
import os

from flask import Flask
from flask.globals import request
from flask.wrappers import Response
from gpiozero import Button, DigitalOutputDevice

class DoorState(Enum):
  OPEN = "open"
  CLOSED = "closed"

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG if app.debug else logging.INFO)

# Raspberry Pi GPIO mapping
app.config['GPIO_OPEN'] = os.environ.get("RPI_GARAGE_DOOR_CONTROLLER_GPIO_OPEN", default=str(17))
app.config['GPIO_CLOSE'] = os.environ.get("RPI_GARAGE_DOOR_CONTROLLER_GPIO_CLOSE", default=str(27))
app.config['GPIO_DOOR_STATE'] = os.environ.get("RPI_GARAGE_DOOR_CONTROLLER_GPIO_DOOR_STATE", default=str(22))

# Initialize GPIO variables
rpi_button_door_state = Button(app.config['GPIO_DOOR_STATE'], pull_up=False)
rpi_output_open = DigitalOutputDevice(app.config['GPIO_OPEN'], active_high=False)
rpi_output_close = DigitalOutputDevice(app.config['GPIO_CLOSE'], active_high=False)

@app.route("/garage_door", methods=['GET', 'POST'])
def garage_door_endpoint():
  if request.method == "GET":
    return Response(
      json.dumps(
        {
          "door_state": DoorState.OPEN.value if rpi_button_door_state.is_pressed else DoorState.CLOSED.value
        }
      ),
      status=200,
      mimetype='application/json'
    )
  elif request.method == "POST":
    req_data = request.get_json()

    if "door_state" not in req_data:
      app.logger.info("'door_state' not found in request")
      return Response(
        json.dumps(
          {
            "message": "'door_state' attribute not found in request data",
          }
        ),
        status=400,
        mimetype='application/json'
      )

    if req_data["door_state"] == DoorState.OPEN.value:
      app.logger.info("Opening door")
      app.logger.debug("Blinking GPIO " + app.config['GPIO_OPEN'])
      rpi_output_open.blink(n=1)

      return Response(
        json.dumps(
          {
            "door_state": DoorState.OPEN.value
          }
        ),
        status=201,
        mimetype='application/json'
      )
    elif req_data["door_state"] == DoorState.CLOSED.value:
      app.logger.info("Closing door")
      app.logger.debug("Blinking GPIO " + app.config['GPIO_CLOSE'])
      rpi_output_close.blink(n=1)

      return Response(
        json.dumps(
          {
            "door_state": DoorState.CLOSED.value
          }
        ),
        status=201,
        mimetype='application/json'
      )
    else:
      try:
        DoorState(req_data["door_state"])
      except ValueError:
        app.logger.info("Invalid 'door_state': " + req_data["door_state"])
        return Response(
          json.dumps(
            {
              "message": "Invalid value for 'door_state': " + req_data["door_state"]
            }
          ),
        status=400,
        mimetype='application/json'
      )
