from FaceRecognizer.Services.FaceDetector import FaceDetector
import base64
import cv2


class Camera_Resource(object):

    def test_cam(self, cameraService):
        cameraService.read()
        if(cameraService.cam.isOpened() == True):
            cameraService.stop_cam()
            return True
        else:
            cameraService.stop_cam()
            return False

    def set_url_cam(self, cam):
        if (cam['type'] == 'ipCam'):
            cam['url'] = 'http://' + cam['ip'] + ':' + cam['port'] + '/mjpegfeed'
        else:
            cam['url'] = None
            cam['ip'] = None
            cam['port'] = None

        return cam
