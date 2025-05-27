# OccupancyDetection

Overview

This project is a smart office occupancy detection system that uses PIR motion sensors and a temperature sensor to monitor room usage and automate environmental control (lights, fan). It leverages a Raspberry Pi and Python to create a responsive system, with a backend Flask dashboard for real-time monitoring.


Key Features:

Real-time room occupancy detection via PIR motion sensors,
Temperature and humidity monitoring using an AHT20 sensor,
Light and fan automation based on sensor data,
Data logging and live updates on a custom dashboard,
Backend built with Flask and data stored in SQLite


Technologies Used:

Python (Flask, GPIO, AHT20 libraries),
Raspberry Pi 400,
PIR Motion Sensors,
AHT20 Temperature & Humidity Sensor,
SQLite (for logging occupancy and environmental data),
HTML/CSS (for frontend interface)


How to Run:

Clone the repository:
git clone https://github.com/Suhanisharma04/OccupancyDetection.git
cd OccupancyDetection

Install dependencies:
pip install -r requirements.txt

Run the application:
python app.py

Open your browser and go to http://localhost:5000 to access the dashboard.



Project Status:
This is a completed university project demonstrating a real-world IoT application for energy-efficient office space management.
