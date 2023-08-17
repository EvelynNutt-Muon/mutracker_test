# Mutracker Test

Software development for testing Mutracker will be broken into three stages:

- Mutracker Radiation Test: All software required for testing the OV2311 chip on the Arducam module, along with scripts required for post-test analysis, comparative radiation recognition, and pixel anomaly detection.

- Mutracker Star Field Simulator Test: Most of the code for this stage already exists on the `mutracker_proto` [repository](https://github.com/Muon-Space/mutracker_proto/tree/master). I may end up copying updated versions of those files over, but not as important for now. The main part of this stage is to get Mutracker to reproduce what is displayed on a screen while looking through a collimating lens. The procedure for the optical setup can be found in the [Optics101 test report](https://docs.google.com/document/d/1qmIDggesDDpajqvfpwtfHPBFSn1zCFabPXSUIwwS-dc/edit).
 
- Mutracker Validation Test: This stage will go beyond what has already been written for testing Mutracker by implementing open source star field generators, astrometric plate solvers, lens distortion calibration, point spread function characterization, and thermal testing. This is the final stage of the Star Field Simulator development.

# RPi How-Tos

I have ran into dozens and dozens of bugs trying to figure out all of these setup steps - so please follow them carefully so you don't mess up your machine or corrupt your RPi.

As a caution, the current `mutracker_proto` code uses deprecated drivers on the Rasbian Buster OS, whereas you would think the Bullseye OS would work just fine. So, please follow these steps to have a successful setup.

## General Setup

1. Download Raspberry Pi Imager to your PC and insert the SD card you'll use into your PC.
2. Open the imager and select Buster OS.
3. Be sure to select your SD card and not your PC.
4. Hit the settings button and setup all local host, SSH, and Wi-Fi details.

    - For hostname, I'd recommend using `mutracker` or something adjacent.
    - For SSH, choose `pi` as the username and a quick-to-type password. Write all of these down!
    - For WiFi, I suggest using your hotspot so you can connect and test from anywhere.
5. Load the OS onto the SD card.
6. When that finishes, remove the SD card from your machine and insert the card into your RPi.
7. Turn on the RPi and turn on your hotspot. Ensure your PC is also connected to the hotspot.
8. Download Putty with all the default settings and enter the hostname into Putty.
9. Login using SSH username and password.
10. After you're logged in, run the command `sudo raspi-config`
11. You can customize your pi how you'd like, but make sure to go to Interface Options and enable Camera and VNC. (You will have this easy access with a remote view of the RPi Desktop, but these are the two important ones to do now)
12. Run `sudo reboot`
13. Repeat steps 7-9.
14. Run `vncserver`
15. The terminal will give you a VNC desktop to log into in the format `yourusername.local:1`
16. Download RealVNCViewer with the default settings and log in.
17. Add a new connection and enter `yourusername.local:1` or whatever the terminal gave you.
18. Start the connection and log into the desktop with your SSH information. 
19. If you see the RPi Desktop, you're in!

## Ethernet Setup

Now that you're connected to the RPi Desktop, let's setup direct Ethernet connection so you can connect to your RPi literally anywhere anytime.

1. Download Bonjour onto your PC and configure with all the default settings. This application will help interpret the Ethernet connection and handle IP addresses for you. 
2. Go to the Wi-Fi icon in the top right of the RPi Desktop and right click it.
3. Click the first item in the list.
4. In the right drop-down menu, select `eth0`
5. 

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