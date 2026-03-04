# stenography-project
Program wich lets you hide and extract messages inside images

Project Title: **Image Steganography with Cryptographic Integrity Validation**

Name: **Muhammed Aslam**

Domain: Cyber Security

Date: March 2026

# Intro

**Confidentiality** is a pillar of the CIA Triad. While encryption scrambles data to make it unreadable,**Steganography** focuses on Obfuscation. This project demonstrates  **embedding of secret data within an image**, ensuring that sensitive information can be transmitted without raising suspicion.
This project implements **the Least Significant Bit (LSB) steganography technique** using Python. a Data Integrity Validation layer was added using the S**HA-256 Hashing algorithm**. The tool is an interactive CLI application that allows users to hide and extract messages 

## Tools and Technologies

Language: **Python 3.12**

Libraries: 
**Pillow** : For advanced image manipulation

**Stepic** : For LSB encoding/decoding

**Hashlib**: For generating SHA-256 integrity checksums


## Implementation Logic (How it Works)

### The LSB Method
Every pixel in a PNG image consists of RGB values .By replacing the Least Significant Bit of these values with bits of the secret message, the color of the pixel changes by a fraction so small that it is invisible to the human eye.
### The Integrity Layer
Before and after the hiding process, the tool calculates a SHA-256 Hash.
•	Pre-encoding Hash: Represents the clean carrier file.
•	Post-encoding Hash: Represents the image with the secret message
Even if the images look identical, the hashes will differ proving that the image is tampered with
## Steps Involved in Building the Project
1.	Initialized a Python Virtual Environment (venv) 
2.	 Installed pillow and  stepic 
3.	Developed sternography.py with functions to hide and show data
4.	Integrated hashlib to automate the calculate hash values
5.	Built a menu for user input
6.	Testing & Validation: Verified the tool using PNG images and confirmed successful extraction of messages
   
## How to Run the Project
Step 1: 
Clone git repository 
Step 2:
Make sure python is installed and run the following commands in terminal on project directory
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Step 3
Place the image that you want to add the message to in the project dir

Step 4
run :
```bash
python3 steganography.py
```
## Use the Menu
Select Option 1 to hide a message. Enter your filename.png and the secret text.
The tool will output a file named secret_image.png.
Select Option 2 and enter secret_image.png to extract and view the hidden data.

 ## Conclusion
The project successfully demonstrates how steganography can be used for covert communication. By adding SHA-256 validation, the project ensures integrity







