# ESP32 MicroPython Projects & Experiments

This is home to my collection of various experiments, prototypes and maybe projects taking advantage of modern [ESP32 SoC microcontrollers](https://en.wikipedia.org/wiki/ESP32) and the [MicroPython](https://micropython.org/) development environment.

## Development Setup

My development setup consists of:

* ESP32 (Wrover) Development Starter Kit [(Link)](https://www.amazon.co.uk/gp/product/B09BC1N9LL/)
* [RShell](https://github.com/dhylands/rshell) (to transfer code to/from the ESP32)
* Raspberry Pi 4
* Visual Studio Code
  * [SSH Remote extension](https://code.visualstudio.com/docs/remote/ssh) connected to Raspberry Pi

The ESP32 development board is connected to the Raspberry Pi using the standard USB port. This provides the ESP with sufficient power (5v) to perform most operations and also doubles as a USB serial port used for flashing and communicating with the board.

### Setup

After connecting the ESP32 to the Raspberry Pi (or another device) via USB:

Create a workspace for your project files:

    mkdir -p ~/projects/esp32
    cd ~/projects/esp32

Create and activate a Python virtual environment:

    python3 -m venv ./venv
    source ./venv/bin/activate

Install the `rshell` tool:

    pip install rshell

Add your current user to the serial port (`dialout`) user group, remembering to fully logout and back in again to ensure the group membership has updated:

    sudo usermod -a -G dialout ${USER}

Try and locate the USB device created for your ESP32

    ls /dev/ttyUSB*

Connect `rshell` to your ESP32 using the found USB device name:

    rshell -p /dev/ttyUSB0 repl

To syncronise files to and from your ESP32:

    # Sync content in current directory to ESP32 /flash directory
    rshell -p /dev/ttyUSB rsync . /flash
    
    # Sync content on ESP32 to current directory
    rshell -p /dev/ttyUSB rsync /flash .
