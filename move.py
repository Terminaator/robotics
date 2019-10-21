import serial
import time
import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
device = list(map(lambda port: port.device, ports))[0]

ser = serial.Serial(device, 115200, timeout=0.01)

while True:
    print(ser.read())
    time.sleep(0.1)
    #ser.write("gs\n".encode())
    #ser.write("sd:10:10:10\n".encode())
