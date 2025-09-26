# 🖨️ Telegram Pi Print Bot 🤖

A simple, elegant, and asynchronous Telegram bot that turns your Raspberry Pi and a USB printer into a network printer accessible from anywhere via Telegram. Just send a document to the bot, and it will be printed instantly\!

Built with ❤️ using **Python**, **Aiogram 3.x**, and **CUPS**.

[](https://www.python.org/downloads/)
[](https://github.com/aiogram/aiogram)
[](https://opensource.org/licenses/MIT)

-----

## ✨ Features

  * 📤 **Remote Printing**: Send documents from any device with Telegram installed.
  * 📄 **Wide Format Support**: Prints any file format that your printer and CUPS drivers support (PDF, TXT, DOCX, JPG, etc.).
  * 🔔 **Real-time Notifications**: Get instant feedback on whether your file has been received and sent to the printer.
  * 🔒 **Secure**: Your bot is private. The bot token is stored securely in an environment file.
  * ⚙️ **Easy Setup**: A step-by-step guide to get you up and running in minutes.
  * 🚀 **Asynchronous**: Built on `asyncio` and `aiogram` for high performance and responsiveness.

-----

## 🛠️ How It Works

The workflow is straightforward:

1.  **User**: You send a document file to the Telegram bot.
2.  **Telegram Bot (Aiogram)**: The bot, running on your Raspberry Pi, receives the file.
3.  **File Download**: The bot downloads the file to a temporary directory on the Pi.
4.  **CUPS Print Server**: The bot uses the `lp` command-line tool to send the downloaded file to the CUPS printing system.
5.  **Printer**: CUPS processes the job and sends it to your connected USB printer.
6.  **Confirmation**: The bot sends you a confirmation message in Telegram.

-----

## 📋 Prerequisites

### Hardware

  * 🍓 **Raspberry Pi 4** (or any other model with network access)
  * 🔌 **USB Printer** connected to the Raspberry Pi
  * 🌐 **Stable Internet Connection**

### Software

  * **Raspberry Pi OS** (or any other Debian-based Linux distro)
  * **Python 3.9+**
  * **CUPS** (Common Unix Printing System)
  * A **Telegram Bot Token**. Get one from [@BotFather](https://t.me/BotFather).

-----

## 🚀 Setup & Installation Guide

Follow these steps carefully to set up your print bot.

### Step 1: Configure the Printer on Raspberry Pi (CUPS)

1.  **Update Your System**:

    ```bash
    sudo apt update && sudo apt upgrade
    ```

2.  **Install CUPS**:

    ```bash
    sudo apt install cups -y
    ```

3.  **Configure CUPS**:

      * Add the `pi` user (or your current user) to the `lpadmin` group to manage printers.

    <!-- end list -->

    ```bash
    sudo usermod -a -G lpadmin pi
    ```

      * Allow remote administration of CUPS (so you can configure it from your main computer's browser).

    <!-- end list -->

    ```bash
    sudo cupsctl --remote-any
    sudo systemctl restart cups
    ```

4.  **Add Your Printer**:

      * Connect your printer to the Raspberry Pi via USB and turn it on.
      * Open a web browser on a computer on the same network and go to `https://<YOUR_PI_IP_ADDRESS>:631`.
      * Navigate to the **Administration** tab and click **Add Printer**.
      * Follow the on-screen instructions. CUPS should automatically detect your printer and suggest the correct drivers.

5.  **Test Printing from Command Line**:

      * Create a test file and send it to the printer using the `lp` command.

    <!-- end list -->

    ```bash
    echo "Hello, Printer!" > test.txt
    lp test.txt
    ```

    If it prints, your CUPS setup is successful\!

### Step 2: Set Up the Bot

1.  **Clone the Repository**:

    ```bash
    git clone https://your-repository-url/telegram-pi-print-bot.git
    cd telegram-pi-print-bot
    ```

2.  **Create a Virtual Environment**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

    *(Note: Create a `requirements.txt` file containing `aiogram` and `python-dotenv`)*

4.  **Configure Environment Variables**:

      * Create a `.env` file in the project root.
      * Add your Telegram Bot Token to it.

    <!-- end list -->

    ```env
    BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
    ```

### Step 3: Run the Bot

1.  **Start the Bot**:

    ```bash
    python main.py
    ```

2.  **Make it Run on Boot (Optional but Recommended)**:

      * To ensure your bot is always running, create a `systemd` service for it. This will automatically start the bot on boot and restart it if it crashes.
      * Create a service file:
        ```bash
        sudo nano /etc/systemd/system/printbot.service
        ```
      * Paste the following configuration, adjusting the paths to match your setup:
        ```ini
        [Unit]
        Description=Telegram Print Bot
        After=network.target

        [Service]
        User=pi
        Group=www-data
        WorkingDirectory=/home/pi/telegram-pi-print-bot
        ExecStart=/home/pi/telegram-pi-print-bot/venv/bin/python main.py
        Restart=always

        [Install]
        WantedBy=multi-user.target
        ```
      * Enable and start the service:
        ```bash
        sudo systemctl enable printbot.service
        sudo systemctl start printbot.service
        sudo systemctl status printbot.service
        ```

-----

## 💬 Usage

1.  Open Telegram and find the bot you created.
2.  Press `/start`.
3.  Send any document (e.g., a PDF file) to the chat.
4.  Wait a few seconds... and your document will start printing\! 📄🖨️

-----

## 🌱 Future Development Roadmap

This project is fully functional, but there's always room for improvement\! Here are some ideas for future development. Contributions are welcome\!

  * [ ] **User Authentication**: Restrict bot access to a list of authorized `user_ids` to prevent unauthorized printing.
  * [ ] **Print Queue System**: Implement a queue to handle multiple documents gracefully instead of printing them all at once.
  * [ ] **Advanced Print Options**: Add support for commands to specify print options, such as:
      * `/print -n 2` for two copies.
      * `/print --grayscale` for black and white printing.
      * `/print --duplex` for double-sided printing.
  * [ ] **Printer Status Command**: Create a `/status` command that checks if the printer is online, out of paper, or has low ink.
  * [ ] **Dockerization**: Package the entire application (bot + dependencies) into a Docker container for even easier deployment and portability.
  * [ ] **Confirmation via Inline Keyboard**: Ask for confirmation before printing using an inline keyboard (e.g., "Print this file? [Yes] [No]").
  * [ ] **Web Interface**: A simple web UI to view the print queue, job history, and manage authorized users.

-----

## 🤝 Contributing

Contributions, issues, and feature requests are welcome\! Feel free to check the [issues page](https://www.google.com/search?q=https://github.com/your-username/telegram-pi-print-bot/issues).

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

-----

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
