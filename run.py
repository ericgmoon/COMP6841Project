import serial
import cv2
import face_recognition
import os
import time
import sys

# Constants
auth_dir = './auth/'
att_dir = './attempts/'
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
port = '/dev/ttyACM1'

# Read the Arduino port as a command argument
if len(sys.argv) == 1:
    print(bcolors.WARNING + 'No port specified...using /dev/ttyACM1...' + bcolors.ENDC)
elif len(sys.argv) == 2:
    port = sys.argv[1]
else:
    print(bcolors.FAIL + 'Correct syntax: python3 run.py {arduino USB port}' + bcolors.ENDC)
    sys.exit();

# Set up Arduino
print("Connecting to the hardware...")
arduino = serial.Serial(port, 115200, timeout=.1)
time.sleep(2)

# Index for naming the photos taken
i = 0

# Set up authorised individuals
auth_list = []
print("Loading authorised faces...")
for directory, subdirectories, files in os.walk(auth_dir):
    for f in files:
        image = face_recognition.load_image_file(auth_dir + f)
        faces = face_recognition.face_encodings(image);
        if len(faces) > 0:
            auth_list.append(faces[0])
            print(bcolors.OKBLUE + "Added: " + f[:-4] + bcolors.ENDC)

print("Ready for scanning...")
while True:
    # :-2 to remove newline characters
    data = arduino.readline()[:-2].decode('ascii')
    if data and data == 'check':
        # Take the photo
        print("Scanning...")
        cam = cv2.VideoCapture(-1)
        rv, image = cam.read()
        image_name = att_dir + 'att' + str(i) + '.png'
        cv2.imwrite(image_name, image)
        print("Captured as: " + bcolors.OKBLUE + image_name + bcolors.ENDC)
        # Crop image
        
        # Process image
        target = face_recognition.load_image_file(image_name)
        faces = face_recognition.face_encodings(target)
        att_list = []
        for face in faces:
            att_list.append(face)
        # Check authorisation
        results = False
        for attempt in att_list:
            for authorised in auth_list:
                results = face_recognition.compare_faces([authorised], face)
                if results and (results[0] == True):
                    # Authorised
                    print(bcolors.OKGREEN + "Authorised" + bcolors.ENDC)
                    arduino.write('a'.encode())
                    break
        # Unauthorised
        if not results or results[0] == False:
            # Unauthorised
            print(bcolors.FAIL + "Unauthorised" + bcolors.ENDC)
            arduino.write('u'.encode())
        # Clean up & increase index for the next image
        del(cam)
        i += 1

