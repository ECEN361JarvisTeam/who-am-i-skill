from mycroft import MycroftSkill, intent_file_handler
import face_recognition as fareg
import cv2 as cv
import numpy as np
import maestro
from maestro_functions import *
from headshots_mycroft import takePicture
import time
from os import path, listdir

# face_recognition with OpenCV code based on code from https://github.com/ageitgey/face_recognition/blob/master/examples/facerec_from_webcam_faster.py


class WhoAmI(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('i.am.who.intent')
    def handle_i_am_who(self, message):
        videoInput = cv.VideoCapture(0)

        try:
            if not videoInput.isOpened():
                self.speak_dialog('camera.error')
                return

            m = maestro.Controller("/dev/ttyACM0")
            recognized = False;
            name = 'error unknown'
            attempts = 10
            tryNum = 0
            faceEncodes = []
            faceNames = []
            facesRootPath = path.join('..', '..', '..', '..', 'home', 'pi', 'mycroft-core', 'faces')

            # Load known faces.
            knownFacePaths = [file for file in listdir(facesRootPath)]

            for filePath in knownFacePaths:
                tempImage = fareg.load_image_file(path.join(facesRootPath, filePath))
                faceEncodes.append(fareg.face_encodings(tempImage)[0])
                faceNames.append(filePath.split('.')[0])

            # Set servos in viewing position.
            setAllToDefault(m)
            self.speak_dialog('face.the.camera')
            time.sleep(2)

            # Check for matching image.
            while not recognized and tryNum < attempts:
                _, newFrame = videoInput.read()
                if newFrame is None:
                    self.speak_dialog('camera.error')
                    videoInput.release()
                    return
                else:
                    # Reduce frame size to decrease computation costs
                    newFrame = cv.resize(newFrame, (0, 0), fx=0.25, fy=0.25)
                    # Change from OpenCV BGR image to RGB image for face_recognition.
                    newFrame = newFrame[:, :, ::-1]

                    unknownImages = fareg.face_locations(newFrame)
                    unknownEncodes = fareg.face_encodings(newFrame, unknownImages)

                    if len(unknownEncodes) > 0:
                        matches = fareg.compare_faces(faceEncodes, unknownEncodes[0])

                        if True in matches:
                            recognized = True
                            name = faceNames[matches.index(True)]

                    tryNum = tryNum + 1


            if recognized:
                self.speak_dialog('i.am.who', {'name': name})
            else:
                # Code to add new face.
                name = self.get_response('I don\'t know, who are you?')
                if name is not None:
                    self.speak_dialog('face.the.camera')
                    time.sleep(2)
                    if takePicture(name, facesRootPath, videoInput):
                        self.speak_dialog('i.am.who.known', {'name': name})
                    else:
                        self.speak_dialog('i.am.who.unsaved', {'name': name})
                else:
                    self.speak_dialog('i.am.who.no.name')

            videoInput.release()

        except Exception as errorValue:
            self.speak('i.am.who.error', {'type': type(errorValue), 'args': errorValue.args, 'data': errorValue})
            videoInput.release()


def create_skill():
    return WhoAmI()

