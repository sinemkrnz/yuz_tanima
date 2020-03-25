
import sys
import os
import dlib
import glob
from skimage import io
from SQLite import SQLite


class face_detection:
    sayac = 1
    imageDataList = []

    def setup(self):
        predictor_path = r"C:\Users\Sinem\Documents\GitHub\Playground\PyQt Examples\Models\shape_predictor_5_face_landmarks.dat"
        face_rec_model_path = r"C:\Users\Sinem\Documents\GitHub\Playground\PyQt Examples\Models\dlib_face_recognition_resnet_model_v1.dat"
        self.detector = dlib.get_frontal_face_detector()#kaç yüz olduğunu buluyo
        self.sp = dlib.shape_predictor(predictor_path)
        self.facerec = dlib.face_recognition_model_v1(face_rec_model_path)
        self.db = SQLite()

    def detection(self, f):#resmin pathi
        self.setup()
        
        print("Processing file: {}".format(f))
        img = io.imread(f)#pathi okuyo img değişkenin içine atıyo
        dets = self.detector(img, 1)#1 rsim renkli/0 gri
        print("Number of faces detected: {}".format(len(dets)))#bulunan yüzlerin sayısını veriyor

        for k, d in enumerate(dets):#dets yüz bilgisi
            data = []
            data.append(d.left())#yüzün koordinatlarıı
            data.append(d.top())
            data.append(d.right())
            data.append(d.bottom())

            self.imageDataList.append(data)
            #yüz embed bilgisi cıkarıyo 128elemanlı dizi
            shape = self.sp(img, d)
            face_descriptor = self.facerec.compute_face_descriptor(img, shape)
            face_chip = dlib.get_face_chip(img, shape)
            face_descriptor_from_prealigned_image = self.facerec.compute_face_descriptor(face_chip)
            
            self.listToStr(face_descriptor_from_prealigned_image,f)
            # print(face_descriptor_from_prealigned_image)

    def listToStr(self, liste, path):
        data = ""
        for item in liste:
            data += str(item)+"/" #128elemanı tek bir string haline ceviriyo 
        result = self.db.INSERT(self.sayac, data, path)
        print(result)
        self.sayac += 1


if __name__ == '__main__':
    app = face_detection()
    #Klasorden Kayıt Ederken
    faces_folder_path=r"C:\Users\Sinem\Desktop\YuzTanıma\faces"
    for f in glob.glob(os.path.join(faces_folder_path, "*.jpg")):#klssorun içindeki her resim f ile gösteril,iyo
      app.detection(f)
    
    #Tek Resim Kayıt Ederken
    #path=r""
    #app.detection(path)
        