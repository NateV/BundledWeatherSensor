#!bin/sh
# launcher.sh

echo "Launching script."
echo "1) Starting virtual environment."

#Turn on the virtual environment
source sensors/BundledWeatherSensor/virtualenvs/sensorEnv/bin/activate

echo "2) running python script."

#Turn on the script
python sensors/BundledWeatherSensor/PiPyScript/PythonListener.py

