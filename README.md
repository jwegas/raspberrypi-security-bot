# Your Security Telegram Bot for Raspberry Pi

Hey there. This is Telegram Bot which can help you to control your home or working space.
With Raspberry Pi microcomputer, PIR motion sensor and Camera it will inform you with telegram message if someone come to your room, office or another space.

This code was tested with:
* Raspberry Pi 3b+;
* Raspberry Camera v2.1;
* Infrared PIR Motion Sensor Module HC-SR501.

## Install

1. Create Telegram Bot. Please follow to this [official instructions](https://core.telegram.org/bots#6-botfather);
2. Be sure you have `git` installed. You can install it with `sudo apt install git` command;
3. Clone this repo on your device with command `git clone https://github.com/jwegas/raspberrypi-security-bot.git` and go this repo;
4. Be sure you camera is [connected to device and enabled](https://www.raspberrypi.org/documentation/configuration/camera.md);
5. Connect PIR sensor to device properly ([example](https://projects.raspberrypi.org/en/projects/parent-detector/1)):
    * Connect the PIR sensor’s pin labelled VCC to the 5V pin on the Raspberry Pi. This provides power to the PIR sensor;
    * Connect the one labelled GND to a ground pin on the Pi (also labelled GND). This completes the circuit;
    * Connect the one labelled OUT to any numbered GPIO pin on the Pi;
6. Create file `config.py` as copy of `config_template.py` and put there your settings:
    * `TOKEN` - token you got after creating telegram bot;
    * `RECIEVER_ID` - ID of chat to communicate with. Only you can communicate with this bot. E.g. you can get your `RECIEVER_ID` with help of another Telegram Bot called *@userinfobot*. It will send your id.
    * `REQUEST_KWARGS` - additional settings to connect to Telegram server, e.g. proxy settings;
    * `PIR_OUT` - Raspberry Pi pin number (according BCM mode) which signal pin of PIR sensor is connected to.
7. Create virtual environment (e.g. with `virtualenv`) and install all requirements:
    * `virtualenv venv -p python3`;
    * `source venv/bin/activate`;
    * `pip install -r requirements.txt`;
8. Run your Bot with one of two ways:
    * simply activate your `venv` environment (`source venv/bin/activate`) and run `python run_bot.py`;
    * create your own with your settings based on `start_tmux_session_template.sh` and run it to run bot inside TMUX session. You need to have TMUX installed (`sudo apt install tmux`). It's better way to manage your bot on device.

## Interactions:

* To show start menu simply type `/<command>` where \<command\> can be one of [menu, start, hi, hey, hello];
* Type `/start` (button *Start Detection*) or `/stop` (button *Stop Detection*) to start or stop movement detection process accordingly;
* Type `/photo` (button *Make Photo*) to force get photo from Camera.
