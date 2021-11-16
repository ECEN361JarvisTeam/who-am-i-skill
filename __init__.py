from mycroft import MycroftSkill, intent_file_handler
import face_recognition as fareg
import cv2 as cv
import numpy as np
import maestro
import maestro_functions as mf
import time

# face_recognition with OpenCV code based on code from https://github.com/ageitgey/face_recognition/blob/master/examples/facerec_from_webcam_faster.py


class WhoAmI(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('i.am.who.intent')
    def handle_i_am_who(self, message):
        videoInput = cv.VideoCapture(0)

        if not videoInput.isOpened():
            self.speak_dialog('camera.error')
            return

        m = maestro.Controller("/dev/ttyACM0")
        recognized = False;
        name = 'error unknown'

        # Set servos in viewing position.
        m.setAccel(0, 4)
        m.setSpeed(0, 12)

        m.setAccel(1, 4)
        m.setSpeed(1, 12)

        m.setAccel(3, 4)
        m.setSpeed(3, 12)

        m.setAccel(4, 4)
        m.setSpeed(4, 12)

        m.setAccel(5, 4)
        m.setSpeed(5, 12)

        # Check for matching image
        self.speak_dialog('face.the.camera')
        time.sleep(2)

        if recognized:
            self.speak_dialog('i.am.who', {'name': name})
        else:
            self.speak_dialog('i.am.who.unknown')
            # Code to add new face.
            name = self.get_response('i.am.intent')
            self.speak_dialog('i.am.who.known', {'name': name})


def create_skill():
    return WhoAmI()

