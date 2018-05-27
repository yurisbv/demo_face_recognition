from FaceRecognizer.Services.FaceDetector import FaceDetector
from FaceRecognizer.Services.CameraRecognizer import CameraRecognizer


class Recognition_Resource(object):
    last_frame=None
    _faceDetector = FaceDetector()


    def capture(self, cameraService):
        while True:
            frame = self._faceDetector.detect_camera(cameraService)
            Recognition_Resource.last_frame = self._faceDetector.get_last_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        cameraService.stop_cam()

    def recognition(self, cameraService):
        cameraRecognizer = CameraRecognizer()
        try:
            while True:
                frame = cameraRecognizer.recognition(cameraService)
                yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            cameraService.stop_cam()
        except:
            print('Stop Recognition')

    def get_url_cam(self, cam):
        if (cam != None):
            if (cam['type'] == 'ipCam'):
                return cam['url']
            else:
                return None