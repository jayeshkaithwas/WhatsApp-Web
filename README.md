# WhatsApp Web Automation

This repository contains a Python script to automate sending messages and media through WhatsApp Web using Selenium. The script includes a GUI built with Tkinter for ease of use.

## Features

- Generate QR Code for WhatsApp Web login.
- Send text messages.
- Send media files.
- Queue messages for sequential sending.
- Display message status in a GUI.

## Prerequisites

- Python 3.x
- Google Chrome
- ChromeDriver
- Required Python packages: `selenium`, `pillow`, `qrcode`, `tkinter`

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/jayeshkaithwas/WhatsAppWebAutomation.git
    cd WhatsAppWebAutomation
    ```

2. **Install the required packages:**
    ```bash
    pip install selenium pillow qrcode
    ```

3. **Download ChromeDriver:**
    - Download the ChromeDriver from [here](https://sites.google.com/chromium.org/driver/downloads).
    - Ensure that ChromeDriver is in your PATH or in the same directory as the script.

## Configuration

1. **Profile Directory:**
   Update the `PROFILE_DIR` variable in the script with the correct path to your Chrome profile directory.

2. **Running Chrome with the Profile Path:**
   If the profile does not exist, the script will prompt you to create and set up a new profile manually.

## Usage

1. **Run the script:**
    ```bash
    python your_script_name.py
    ```

2. **GUI Interface:**
   - Click "Generate QR Code" to generate a QR code for WhatsApp Web login.
   - Enter the phone number, message text, and optionally, select a document to send.
   - Click "Submit" to queue the message for sending.

## Code Explanation

The script uses the following libraries:
- **`selenium`**: For automating browser interactions.
- **`tkinter`**: For creating the graphical user interface.
- **`pillow`**: For image processing.
- **`qrcode`**: For generating QR codes.

The main functionalities include:
- **QR Code Generation**: Generates a QR code for WhatsApp Web login.
- **Message Sending**: Sends text messages and media files.
- **Queue Management**: Manages a queue of messages to be sent sequentially.

## Screenshot

![Screenshot 2024-08-01 171656](https://github.com/user-attachments/assets/b5f75d5b-ab51-45c6-b725-428efd11746e)

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License.

## Contact

For any queries or issues, please contact Jayesh Kaithwas.
