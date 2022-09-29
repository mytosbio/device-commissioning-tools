# Device Commissioning Tools

## Setup 
check python version is > 3.6
`python --version`
create venv in a folder named env
`python -m venv env`
install dependencies
`python -m pip install -r requirements.txt`
run the script you are interested in, i.e.
'python .\gantry_alignment.py'
## Gantry Alignment
This python script helps to automate the gantry alignment procedure by providing a python script that:
- Checks the gantries have the default calibrations (if not then reprogramming is required before starting - experimental -> tries to set default values on initialisation)
- Moves the microscope and light gantry to each nominal position
- The user can then move the light gantry using the keyboard arrow keys while watching the arducam image
- Cheat sheet:
    - arrow keys -> move light gantry
    - "+" or "-" change move step size (default is 0.1mm)
    - "n" moves onto the next position

