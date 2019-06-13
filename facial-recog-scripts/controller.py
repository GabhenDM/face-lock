
from flask import Flask
from flask import request,render_template
from flask_json import FlaskJSON, JsonError, json_response, as_json
import serial 
import time


app = Flask(__name__)
FlaskJSON(app)

arduino = serial.Serial('/dev/cu.usbmodem14201', 9600)


def onOffFunction(command):
	if command =="on":
		print("Abrindo a Porta...")
		time.sleep(1) 
		arduino.write(b'H') 
	elif command =="off":
		print("Fechando a Porta...")
		time.sleep(1) 
		arduino.write(b'L')
	elif command =="bye":
		print("Adeus!...")
		time.sleep(1) 
		arduino.close()


@app.route("/controller", methods=['GET'])
def onOffArduino():
    if(request.args.get('command') == "on"):
        onOffFunction("on")
        return json_response(status=200)
    elif(request.args.get('command') == "off"):
        onOffFunction("off")
        return json_response(status=200)
    else:
        return json_response(status=404)

@app.route("/", methods=['GET'])
def home():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()