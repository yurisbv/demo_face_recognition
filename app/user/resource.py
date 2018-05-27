import cv2
import base64

class User_Resource(object):

    def faces_to_b64(self, faces, image_faces):
        newFaces=[]
        for face in faces:
            face=face.replace("\\", "/")
            image=cv2.cvtColor(cv2.imread(face), cv2.COLOR_BGR2GRAY)
            image_faces.append(image)
            ret, jsonImage=cv2.imencode('.jpg', image)
            jpg_as_text = base64.b64encode(jsonImage.tobytes())
            jpg_as_text = jpg_as_text.decode('ascii')
            newFaces.append(jpg_as_text)
        return newFaces