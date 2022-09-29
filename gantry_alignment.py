from utils.project_imports import *
from utils.serial_toolbox import *
MOVE_COMPLETE = f"INFO:move:x_stage move complete\r\n"; # to update for the move complete move:OUTPUT()?
KIT_READY = f"INIT:COMPLETE\r\n";

#%% Connect to the light and microscope gantries and set calibration values to default

light_gantry_serialport = "COM18"
microscope_gantry_serialport = "COM20"

positions_to_check = np.array([
                      [470,330],
                      [20,330],
                      [470,40],
                      [20,40]
                     ], dtype=float);

_z                 = 3; # default microscope gantry Z position
step_size          = 0.1; # Movement step size

#%% Check we are connecting to the correct gantries and they are using the default values
lightGantry = connect(light_gantry_serialport)
wait_for_response(lightGantry,f"NAME:LightGantry\r\n")
wait_for_response(lightGantry,KIT_READY)
write_read(lightGantry,f"setXoffsets(0,1,0,0)\r\n")
write_read(lightGantry,f"setYoffsets(1,0,0,0)\r\n")

microscopeGantry =  connect(microscope_gantry_serialport)
wait_for_response(microscopeGantry,f"NAME:MicroscopeGantry\r\n")
wait_for_response(microscopeGantry,KIT_READY )
write_read(microscopeGantry,f"setXoffsets(0,1,0,0)\r\n")
write_read(microscopeGantry,f"setYoffsets(1,0,0,0)\r\n")

#%% Loop through each capture position and wait for alignment to complete
calibrated_positions = positions_to_check;
i = 0;

write_read(lightGantry,f"light(100)\r\n"); # turn light on
print("Starting calibration at nominal positions")
print("Use arrow keys to adjust position of light gantry, + or - to change the step size and n to confirm alignment and move onto the next position")
for i in range(len(positions_to_check)):
    # store nominal position
    _x = positions_to_check[i][0]
    _y = positions_to_check[i][1]
    
    print("Calibrating for position x = " +str(_x) + ", y= " + str(_y))
    write_wait_for_response(lightGantry,f"move({_x},{_y})\r\n",MOVE_COMPLETE)
    write_wait_for_response(microscopeGantry,f"move({_x},{_y},{_z})\r\n", MOVE_COMPLETE)


    # Nominal position reached: now wait for keyboard input to align by moving the light gantry, press n to complete
    while True:
        if keyboard.is_pressed("left arrow"):  
            _x = _x + step_size;
        if keyboard.is_pressed("right arrow"):  
            _x = _x - step_size;
        if keyboard.is_pressed("up arrow"):  
            _y = _y  + step_size;
        if keyboard.is_pressed("down arrow"):  
            _y = _y - step_size;
        if keyboard.is_pressed("+"):  
            step_size = step_size*2;
            print("Step size set to " + str(step_size))
            time.sleep(1)
        if keyboard.is_pressed("-"):  
            step_size = step_size/2;
            print("Step size set to " + str(step_size))    
            time.sleep(1)
        if keyboard.is_pressed("n"):
            calibrated_positions[i][0] = _x;
            calibrated_positions[i][1] = _y;
            print("Calibrated position x = " +str(_x) + ", y= " + str(_y))
            break;
        
        time.sleep(0.25)
        write_wait_for_response(lightGantry,f"move({_x},{_y})\r\n",MOVE_COMPLETE)
            
#%% Run least squares fitting:



#%% Write new values to device and confirm calibration
