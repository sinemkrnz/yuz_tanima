import face_recognition
import numpy as np
import sys
import os
import dlib
import glob
from skimage import io
from SQLite import SQLite



class Face_Recognition:
    
    predictor_path = r"C:\Users\Sinem\Documents\GitHub\Playground\PyQt Examples\Models\shape_predictor_5_face_landmarks.dat"
    face_rec_model_path = r"C:\Users\Sinem\Documents\GitHub\Playground\PyQt Examples\Models\dlib_face_recognition_resnet_model_v1.dat"
    imageDataList=[]
    def setup(self):
        self.detector = dlib.get_frontal_face_detector()
        self.sp = dlib.shape_predictor(self.predictor_path)
        self.facerec = dlib.face_recognition_model_v1(self.face_rec_model_path)


    def FaceEncode(self,path):
        self.setup()
        imagePath = path
        
        img = io.imread(imagePath)
        dets = self.detector(img, 1)#kac yuz olduğunu buluyor

        for k, d in enumerate(dets):#her yüzün embedini çıkarıyor.
            shape = self.sp(img, d)
            face_chip=dlib.get_face_chip(img, shape)
            self.face_descriptor_from_prealigned_image=self.facerec.compute_face_descriptor(face_chip)
            
            #resimdeki tüm yüzler image data listin içinde
            self.imageDataList.append(self.face_descriptor_from_prealigned_image)
        resultList=[] #veri tabanınfdan gelecek cevaplar var
        for item in self.imageDataList:
            resultList.append(self.search(item))
        return resultList

    def search(self, searchEncode):
        db=SQLite()
        sourceImageEncode=np.array(searchEncode).astype(np.float) #bulmak istenilen yüz
        results=[]
        DBImageList = []
        DBImageList=db.GETALL() #veri tabaındaki tüö resimleri getir
        newList=[]
        knownFaces=[]
        for item in DBImageList:
            faceNumber=item[0] #yüzün numarası
            faceEncode=item[1].split('/') #stringi parcalıyor
            del faceEncode[-1] #son elemanı siliyor
            imagePaht=item[2]
            data=[]
            data.append(faceNumber)
            data.append(np.array(faceEncode).astype(np.float))
            data.append(imagePaht)

            newList.append(data)
            knownFaces.append(np.array(faceEncode).astype(np.float))
        
        results = face_recognition.compare_faces(np.array(knownFaces), sourceImageEncode) #karşılastırma yapıyor
        sayac2=0
        returnList=[]
        for item in results:
            if item==True:
                returnList.append(newList[sayac2][2]) #bulunan her bir elemanın pathini alıyo resultliste atıyo
            sayac2+=1
        return returnList

if __name__ == "__main__":
    app=Face_Recognition()
    path=r"C:\Users\Sinem\Desktop\YuzTanıma\faces\lucifer4.jpg"
    
    list3=app.FaceEncode(path)
    #list3=app.search(data.split('/'))
    print(list3)
    app.FaceEncode(path)

