from flask import Flask, request
from markupsafe import escape
from datetime import datetime
import time
import serial

app = Flask(__name__)

global ser
try:
    # Com 4 is the serial port your device is on, to find this go to device manager and look at the ports and look for a device with COM# in the name, put that where COM4 is
    # 230400 is the baud rate, this is the speed at which the data is sent, you can lookup your device to find the baud rate it uses
    ser = serial.Serial('COM4', 230400, timeout=1)
    ser.readline()
    print("successfully opened serial port")
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    ser = None

# List to store log entries
log_entries = []

def readMessages():
    if ser and ser.is_open:
        while ser.in_waiting:
            ser.readline().decode('UTF-8')
readMessages()

def action_method():
    readMessages()
    print("run Actions")
    ser.write(b'led b 255\r\n')
    ser.write(b'led r 255\r\n')
    ser.write(b'vibro 1\r\n')
    ser.write(b'ir tx NEC 0x80 0x12\r\n')
    ser.write(b'ir tx NEC 0x80 0x1A\r\n')
    ser.write(b'ir tx NEC 0x80 0x12\r\n')
    ser.write(b'ir tx NEC 0x80 0x1A\r\n')
    ser.write(b'ir tx NEC 0x80 0x12\r\n')
    ser.write(b'ir tx NEC 0x80 0x1A\r\n')
    time.sleep(0.5)
    ser.write(b'vibro 0\r\n')
    ser.write(b'led b 0\r\n')
    ser.write(b'led r 0\r\n')
    ser.write(b'ir tx NEC 0x80 0x1A\r\n')
    readMessages()

@app.before_request
def log_request():
    # Log every incoming request before handling it
    timestamp = datetime.now().strftime("%d/%b/%Y %H:%M:%S")
    # Escape user input to prevent XSS
    sanitized_path = escape(request.path)
    log_entry = f'{request.remote_addr} - - [{timestamp}] "{request.method} {sanitized_path} HTTP/1.1"'
    
    # Store the log entry with a placeholder for the status code
    log_entries.append(log_entry)

    # Keep the log entries within the limit
    if len(log_entries) > 30:
        log_entries.pop(0)


@app.after_request
def log_response(response):
    # Update the last log entry with the actual response status code
    log_entries[-1] += f" {response.status_code} -"
    print(ser)
    print(ser.is_open)
    readMessages()
    action_method()
    readMessages()
    return response

@app.route('/')
def home():
    # Display all the logged requests
    return "<br>".join(log_entries)

if __name__ == '__main__':
    app.run(host='your ip here', port=80, debug=False, threaded=False)
