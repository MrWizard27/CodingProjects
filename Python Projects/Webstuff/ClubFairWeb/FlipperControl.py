import time
import serial

# Com 4 is the serial port your device is on, to find this go to device manager and look at the ports and look for a device with COM# in the name, put that where COM4 is
# 230400 is the baud rate, this is the speed at which the data is sent, you can lookup your device to find the baud rate it uses
ser = serial.Serial('COM4', 230400, timeout=1)

def readMessages():
    while(ser.in_waiting):
        print(ser.readline().decode('UTF-8'), end='')

if __name__ == '__main__':
    print(ser.readline())
    readMessages()
    while(True):
        message = input('')
        ser.write(bytes(message + '\r\n', 'UTF-8'))
        time.sleep(0.1)
        ser.readline()
        readMessages()
        

