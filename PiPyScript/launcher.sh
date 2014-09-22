#!bin/sh
# launcher.sh


#Turn on the virtual environment
source sensors/virtualenvs/sensorEnv/bin/activate

#Turn on the script
python sensors/BundledWeatherSensor/PiPyScript/PythonListener

