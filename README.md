# Mutracker Testing

Software development for testing Mutracker is broken into three stages:

- **Mutracker Radiation Test**: All software required for testing the [OV2311](https://www.uctronics.com/2mp-global-shutter-ov2311-mono-camera-modules-pivariety.html) chip on the Arducam module, along with scripts required for post-test analysis, comparative radiation recognition, and pixel anomaly sdetection.

- **Mutracker Star Field Simulator Test**: Most of the code for this stage exists on the `mutracker_proto` [repository](https://github.com/Muon-Space/mutracker_proto/tree/master). An updated version of `mutracker_proto` may be copied over in the future. The main part is to get Mutracker to reproduce what is displayed on a screen while looking through a [collimating lens](https://www.edmundoptics.com/knowledge-center/application-notes/optics/considerations-in-collimation/). The procedure for the optical setup can be found in the [Optics101 test report](https://docs.google.com/document/d/1qmIDggesDDpajqvfpwtfHPBFSn1zCFabPXSUIwwS-dc/edit).
 
- **Mutracker Validation Test**: This stage goes beyond what exists for testing Mutracker's quaternion algorithm by implementing open source star field generators, astrometric plate solvers, [lens distortion calibration](https://www.geeksforgeeks.org/camera-calibration-with-python-opencv/), [point spread function](https://svi.nl/Point-Spread-Function-(PSF)) characterization, and thermal testing. This is the final stage of the Star Field Simulator development.

:camera:

# RPi How-Tos

**_DRIVE DEPRACATION NOTICE_** 

The installations that are used for the Mutracker code are not compatible with the most recent MIPI_Camera drivers and the OpenCV drivers. To get the most out of one Raspberry Pi, please follow this tutorial so all the `mutracker_proto` code and the `mutracker_test` code will functional correctly.

IMPORTANT NOTE ----> NEVER run `sudo apt-get upgrade` on your RPi! It will update all your drivers and prevent the Mutracker code from working. Since we're using older driver versions, it's okay to run `sudo apt-get update`, but never `upgrade` anything on your RPi.

## General Setup

1. [Download Putty](https://putty.org/) with all the default settings.
2. [Download Raspberry Pi Imager](https://www.raspberrypi.com/software/) to your PC and insert the SD card you'll use into your PC.
3. Open the imager and select `Buster OS`.
4. Be sure to select your SD card and not your PC.
5. Hit the settings button and setup all local host, SSH, and Wi-Fi details.

    - For hostname, I'd recommend using `mutracker` or something adjacent.
    - For SSH, choose `pi` as the username and a quick-to-type password. Write all of these down!
    - For WiFi, I suggest using your hotspot so you can connect and test from anywhere.
6. Load the OS onto the SD card.
7. When that finishes, remove the SD card from your machine and insert the card into your RPi.
8. Turn on the RPi and turn on your hotspot. Ensure your PC is also connected to the hotspot.
9. Enter the hostname into Putty.
10. Login using SSH username and password.
11. After you're logged in, run the command `sudo raspi-config`
12. You can customize your pi how you'd like, but make sure to go to the `Interface Options` and enable `Camera` and `VNC`. (You will have this easy access with a remote view of the RPi Desktop, but these are the two important ones to do now)
13. Run `sudo reboot`
14. Repeat steps 7-9.
15. [Download RealVNCViewer](https://www.realvnc.com/en/connect/download/viewer/) with the default settings and log into your RealVNC account.
16. Run `vncserver` in your Putty terminal. The terminal will give you a VNC desktop to log into in the format `hostname.local:1`
17. Add a new connection in the RealVNCViewer and enter `hostname.local:1` or whatever the terminal gave you.
18. Start the connection and log into the desktop with your SSH information. 
19. If you see the RPi Desktop, you're in!

## Ethernet Setup

1. If your PC runs Windows, [download Bonjour](https://support.apple.com/kb/DL999?locale=en_US) onto your PC and configure with all the default settings: This application will help interpret the Ethernet connection and find IP addresses for you. 
2. Go to the `Network Connections` control panel on your PC.
3. Right click on the Wi-Fi that you're connected to and select `Properties`
4. In the `Sharing` folder, check both of the boxes and enter `Ethernet` under `Home networking connection:`
5. Click ok to save these settings.
6. In a terminal accessing your RPi, run `ifconfig`
7. Under the `wlan0` submenu, take note of the RPi's `inet address` of the form `XXX.XXX.XX.X` or `XXX.XX.XX.X`
8. Go to the Wi-Fi icon in the top right of the RPi Desktop and right click it.
9. Click `Wireless & Wired Network Settings`
10. In the right drop-down menu, select `eth0`
11. In both the `Router` and  `DNS Servers` boxes, input your RPi's `inet address`
12. In the `IPv4 Address` box, input a new `static IP address` which can just be your current inet address with the last digit or two replaced with a much higher number.

    - For example, my RPi has an `inet address` of 172.20.10.1, and the `static IP address` I made up is 172.20.10.42
13. Click `Apply` and close the menu.
14. Turn off your RPi.
15. Connect an Ethernet cable between your PC and your RPi.
16. Turn off your hot spot to not confuse the RPi as it will establish a connection with your PC using the `static IP address` instead of the `inet address`
17. Turn on your RPi.
18. Using Putty, enter the RPi's hostname and login using SSH username and password.
19. Run `vncserver` in your Putty terminal. The terminal will give you a VNC desktop to log into in the format `hostname.local:1`
20. Add a new connection in the RealVNCViewer and enter `hostname.local:1` or whatever the terminal gave you.
21. Start the connection and log into the desktop with your SSH information. 
22. If you see the RPi Desktop, you're in!

## Mutracker Code

To get the `mutracker_proto` code onto your PC and your RPi to run the Mutracker's quaternion algorithm:

1. Clone the [Mutracker repository](https://github.com/Muon-Space/mutracker_proto/tree/master) to your PC.

    a. If you don't have access to the repository, follow the instructions in the [ECAD Setup Instructions](https://muonspace.atlassian.net/wiki/spaces/CR/pages/449413121/ECAD+Setup+Instructions)
2. Download [WinSCP](https://winscp.net/eng/download.php), which will help you SSH into your RPi and transfer files remotely.
3. With your RPi on and connected to your PC through hot spot or direct Ethernet, use WinSCP to SSH into your RPi.
4. With a workspace setup, copy the `mutracker_proto` folder into the /home/*your_username* directory on your RPi.
5. After the file transfers, close WinSCP and open RealVNCViewer to double check the file transferred correctly.

## MIPI Drivers

These intallation instructions follow the [Arducam MIPI_Camera driver](https://github.com/ArduCAM/MIPI_Camera/tree/master/RPI) installation process.

To install the MIPI drivers correctly to run `mutracker_proto` files, you'll need to follow these steps carefully:

1. On your RPi under `Preferences`->`Raspberry Pi Configuration`->`Interfaces`, enable the Camera interface.
2. Run `sudo reboot` to make sure the change holds.
3. Open a terminal on your RPi and install the support packages by running these commands (you may need to connect your RPi to Wi-Fi for this step):

    `sudo apt-get update`

    `sudo apt-get install libzbar-dev libopencv-dev`

4. DO NOT RUN `sudo apt-get install python-opencv` YET!!! Instead, choose from these two options:

- If you'd like the Mutracker quaternion algorithm to work on your RPi, go ahead and run `sudo apt-get install python-opencv` and continue following this tutorial.
- If you'd like all of the MIPI_Camera/RPI driver features to operate correctly on your RPI, such as live capture, follow [this tutorial](https://pyimagesearch.com/2019/09/16/install-opencv-4-on-raspberry-pi-4-and-raspbian-buster/) using the pip-install method to be able to install all depedencies of OpenCV without compiling from source.

5. Download and install the SDK library:

    `git clone https://github.com/ArduCAM/MIPI_Camera.git`

    `cd MIPI_Camera/RPI`

    `make install`

    `sudo install -m 644 lib/libarducam_mipicamera.so /usr/lib/`

    `cd /tmp`

    `wget https://project-downloads.drogon.net/wiringpi-latest.deb`

    `sudo dpkg -i wiringpi-latest.deb`

    `cd`

    `cd MIPI_Camera/RPI`

    `chmod +x enable_i2c_vc.sh`

    `./enable_i2c_vc.sh`

    Then click Y to reboot
6. Open a terminal on your RPi again and compile the Arducam examples.

    `cd MIPI_Camera/RPI`

    `make clean && make`
7. To begin using the Arducam commands and OpenCV Gui, please refer to the [Arducam MIPI_Camera driver](https://github.com/ArduCAM/MIPI_Camera/tree/master/RPI) Github under "How to use release demos?"


# Mutracker Radiation Test

## Goals:

- While setting up for a test, use autoexposure settings with the lights off to help the sensor focus on incident radiation.
- During a test, capture and save images every 10 seconds while the beam is on.
- Produce png and raw images to analyze after testing.
- Identify dead and hot pixels after testing.

## Setup How-Tos:

### How to start Mutracker Rad Test:

- Establish connection with RPi over Ethernet using Putty.
- Run vncserver in a terminal on your PC.
- Go to RealVNCViewer and open a terminal.
- Enter these commands:

    `cd mutracker_proto/radtest/systemd`

    `sudo su`

    `bash mutracker-radtest-enable.sh`
- Check that photos are being generated correctly in the `radtest_data` folder located in directory `/home/pi/mutracker_proto`

### How to stop Mutracker Rad Test:

- While still in the systemd directory as the root user, enter the command:
    
    `bash mutracker-radtest-disable.sh`
- All done!

### August 11th, 2023 Radiation Test Results: 

MuTracker image sensor: Tested to 11krad, and recoverable (after power cycle) functional upsets seen at ~5krad and ~9krad. Image analysis underway to detect hot/dead pixels and characterize the radiation induced noise (beam set to 10pA, 100pA, and 1nA).

- [Test log](https://github.com/Muon-Space/radtest/tree/main/results/ucd_20230811/ov2311)
- [Test result video!](https://drive.google.com/file/d/11sDO0cBbXf5ZDy7LDanfG3Vu3N43jvEA/view?usp=drive_link)
- [Identified hot pixels](https://drive.google.com/file/d/1xoKgKy0rL_X_Shs2fnMt-HV9935ZENY5/view?usp=drive_link)
- Identified dead pixels


# Mutracker Star Field Simulator Test

## Goals:

- Make sure that a single lit pixel, or a gropu of pixels, will correspond to a certain number of lit pixels on the star tracker focal plane.
- Mounting for Mutracker needs to be aligned to .1 degrees or less if wanting .1 degrees or less error.


# Mutracker Validation Test

## Goals: 

- Might need to know where Mutracker is facing to get true solutions.
- Get an image that tells you global position based on an image, or get "what star field do I see" so we can compare ground truth to what the algorithm is saying.
- Can find the total system error and check against the spec sheet to decide on the capability of Mutracker.
- Be able to download/generate any part of the sky and check Mutracker's accuracy, precision, and repeatability.


# RPi SD Card Log

## Mutracker.local

- Buster OS
- Has simple MIPI functions, but not the live GUI. (TO change in near future)
- Putty info: mutracker.local, port 22
- SSH username: muon
- SSH password: starfield
- Inet IP: 10.2.2.20
- Static IP: 10.2.2.40
- RealVNC: mutracker.local
- Mutracker Code Status: (TO change in near future)
    - Online Code using `python`: `"NULL pointer access" in arducam_mipicamera.py`
    - Online Code using `python3`: garbage values for quaternions, `"NULL pointer access"` error, and `module 'numpy' has no attritubte 'int' in __init__.py`
    - Offline Code using `python`: `No module named 'quaternion'`
    - Offline Code using `python3`: `No module name 'quaternion'`

## Raspberrypi.local

- Buster OS
- Fully functioning radiation test code.
- Putty info: raspberrypi.local, port 22
- SSH username: pi
- SSH password: potato
- Inet IP: 172.20.10.7
- Static IP: 172.20.10.27
- RealVNC: raspberrypi.local:1
- Mutracker Code Status:
    - Online Code using `python`: freezes after initializing camera
    - Online Code using `python3`: freezes after initializing camera
    - Offline Code using `python`: `Cannot import name perf_counter in tetra_ocv.py`
    - Offline Code using `python3`: `No module name 'cv2' in tetra3_ocv.py`

## Sim.local
- Buster OS
- Fully function OpenCV commands and live capture GUI for testing the Star Field Simulator.
- Putty info: sim.local, port 22
- SSH username: pi
- SSH password: potato
- Inet IP: 172.20.10.7
- Static IP: 172.20.10.42
- RealVNC: sim.local
- Mutracker Code Status: `mutracker_proto` has not been transferred yet.