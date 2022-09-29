from utils.project_imports import *

def connect(port, baudrate=9600, debug=False):
    "Connect to a serial port over a number of attempts"
    error = None
    attempts = 3
    for i in range(attempts):
        try:
            if debug:
                print("Connecting to {} - {}/{}".format(port, i, attempts))
            serial_ = serial.Serial(port, baudrate=baudrate, timeout=1)
            serial_.reset_input_buffer()
            serial_.reset_output_buffer()
            return serial_
        except Exception as e:
            time.sleep(1)
            error = e
            if debug:
                print(e)
            continue
    raise RuntimeError(error)

def write_read(ser,x):
    ser.write(x.encode());
    time.sleep(0.05)
    data = ser.readline()
    return data

def wait_for_response(ser,finish_cmd):
    timeout = 60*10
    timestart = time.time()
   # cmd_finishX = f"INFO:move:x_stage move complete\r\n"
   # cmd_finishY = f"INFO:move:y_stage move complete\r\n"
    while time.time() - timestart < timeout:
        completion_check = ser.readline()
        #print(completion_check)
        if completion_check[0:5] == bytes("ERROR", encoding="ascii"):
            print(completion_check.decode("ascii"))
            return
        elif completion_check == bytes(finish_cmd, encoding="ascii") :
            return
                
    print("Failed to complete action")
    return

def write_wait_for_response(ser,x,response):
    ser.write(x.encode());
    time.sleep(0.05)
    data = ser.readline();
    wait_for_response(ser,finish_cmd);
    return data
