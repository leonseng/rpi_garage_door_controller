# RPi Garage Door Controller

## Setup

```
# Create a Python virtual environment
python -m venv .venv

# Activate the virtual environment
. .venv/bin/activate

# Install the required packages
pip install -r requirements.txt
```

---
## Run the application

Run `python waitress_serve.py` to start the application.

### Configuration

The application is configurable with the following environment variables

| Variable | Description | Mandatory | Example | Default |
| --- | --- | --- | --- | --- |
| RPI_GARAGE_DOOR_CONTROLLER_GPIO_OPEN | GPIO pin connected to the relay for opening the door | N | 10 | 17 |
| RPI_GARAGE_DOOR_CONTROLLER_GPIO_CLOSE | GPIO pin connected to the relay for closing the door | N | 10 | 27 |
| RPI_GARAGE_DOOR_CONTROLLER_GPIO_DOOR_STATE | GPIO pin connected to the door sensor | N | 10 | 22 |
| RPI_GARAGE_DOOR_CONTROLLER_HOST | Host IP to serve application on | N | 10.0.0.1 | 127.0.0.1 |
| RPI_GARAGE_DOOR_CONTROLLER_PORT | Host port to serve application on | N | 80 | 8080 |
| FLASK_DEBUG | Enables debug logs | N | true | false |

---
## API

Check door status, if it is opened or closed.
```
# Request
GET /garage_door

# Response
200
{
  "door_state": "opened"
}
```

Open door.
```
# Request
POST /garage_door
{
  "door_state": "opened"
}

# Response
201
{
  "door_state": "opened"
}
```

Close door.
```
# Request
POST /garage_door
{
  "door_state": "closed"
}

# Response
200
{
  "door_state": "closed"
}
```