# AI-Smart-Blindman-Stick

This repository contains the source code and instructions for a multi-device project integrating Arduino, Raspberry Pi, and ESP32 for various functionalities like sensor integration, voice recognition, and Bluetooth communication.

## **Table of Contents**
- [Project Overview](#project-overview)
- [Hardware Components](#hardware-components)
- [Software Requirements](#software-requirements)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [Code Breakdown](#code-breakdown)
- [License](#license)
- [Contributing](#contributing)

## **Project Overview**

This project demonstrates the integration of Arduino, Raspberry Pi, and ESP32 for a variety of tasks including:
- Ultrasonic sensor-based distance measurement and alert system using Arduino.
- Voice recognition and GPS-based navigation using Raspberry Pi.
- Object detection and Bluetooth communication using ESP32.

The system is designed for applications like obstacle detection, navigation assistance, and IoT-based remote monitoring.

## **Hardware Components**

- **Arduino Uno**
- **Ultrasonic Sensor (HC-SR04)**
- **Buzzer**
- **Touch Sensor**
- **Transistor**
- **ESP32-CAM**
- **Raspberry Pi Zero 2 W**
- **GPS Module (IDUINO M8N)**
- **Bluetooth Earphones (for voice input)**

## **Software Requirements**

- **Arduino IDE** for programming the Arduino and ESP32.
- **Raspberry Pi OS** (Debian-based) for the Raspberry Pi.
- **Python 3.7 or higher** for running the Python scripts on the Raspberry Pi.
- **Edge Impulse SDK** for running inferencing on the ESP32.
- **SoundDevice**, **SoundFile**, **Pydub**, **SpeechRecognition**, **gTTS**, **Requests**, **Pynmea2**, **Geopy** Python libraries for Raspberry Pi.

## **Installation and Setup**

### **Arduino Setup**

1. Connect the Arduino to your computer via USB.
2. Open the Arduino IDE.
3. Install the required libraries (`SoftwareSerial`).
4. Upload the Arduino code from `arduino_code.ino` to the Arduino board.

### **Raspberry Pi Setup**

1. Install required Python packages:
    ```bash
    sudo apt-get update
    sudo apt-get install python3-pip
    pip3 install sounddevice soundfile pydub SpeechRecognition gTTS requests pynmea2 geopy
    ```
2. Place the Raspberry Pi code (`raspberry_pi_code.py`) in your working directory.
3. Run the Python script:
    ```bash
    python3 raspberry_pi_code.py
    ```

### **ESP32 Setup**

1. Open the Arduino IDE.
2. Install the ESP32 board support from the Board Manager.
3. Upload the ESP32 code from `esp32_code.ino` to the ESP32-CAM.
4. Ensure the ESP32 is connected to the same network as the Raspberry Pi.

## **Usage**

1. **Arduino**: The Arduino continuously measures the distance using the ultrasonic sensor and activates the buzzer and vibrator if the distance falls below a threshold.
2. **Raspberry Pi**: It records audio, converts it to text, and uses it to fetch GPS coordinates for navigation. The system continuously reads GPS data and gives directions.
3. **ESP32**: The ESP32 captures images, processes them using Edge Impulse, and sends results over Bluetooth.

## **Code Breakdown**

### **Arduino Code (`arduino_code.ino`)**

- Initializes the ultrasonic sensor and buzzer.
- Measures distance and triggers alerts if an object is detected within a certain range.
- Communicates with the ESP32 over a software serial interface.

### **Raspberry Pi Code (`raspberry_pi_code.py`)**

- Records audio using a Bluetooth earphone.
- Converts the recorded audio to text and processes it to fetch GPS coordinates.
- Provides navigation instructions based on the GPS data.

### **ESP32 Code (`esp32_code.ino`)**

- Captures images using the ESP32-CAM module.
- Processes images using an Edge Impulse model to detect objects.
- Sends the results over Bluetooth.

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## **Contributing**

Contributions are welcome! Please fork the repository and submit a pull request with your changes. For major changes, please open an issue first to discuss what you would like to change.

---

Feel free to use, modify, and share this project. Happy coding!
