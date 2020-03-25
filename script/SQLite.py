import sqlite3

class SQLite:
    def __init__(self):
        self.db=sqlite3.connect('facedataDBX.sqlite')
        self.im=self.db.cursor()
        self.im.execute("CREATE TABLE IF NOT EXISTS FaceDataTableX (faceNumber,faceEncode, imagePath)")



    def INSERT(self,faceNumber,faceEncode,imagePath):
        searchQuery="""SELECT * FROM FaceDataTableX Where faceNumber="""+str(faceNumber)+""" AND faceEncode='"""+str(faceEncode)+"""' AND imagePath='"""+str(imagePath)+"""' """ 
        self.im.execute(searchQuery)
        row =self.im.fetchone()
        self.db.commit() 
        if row == None:
            insertQuery="""INSERT INTO FaceDataTableX (faceNumber,faceEncode,imagePath) VALUES ("""+str(faceNumber)+""", '"""+str(faceEncode)+"""', '"""+str(imagePath)+"""')"""
            self.im.execute(insertQuery)
            self.db.commit() 
            return ("Image data saved.")
        else:
            return ("Data already exists.")  

    def GETALL(self):
        searchQuery="""SELECT * FROM FaceDataTableX """ 
        self.im.execute(searchQuery)
        result =self.im.fetchall()
        self.db.commit() 
        return (result)

    def DELETE(self):
        searchQuery="""DELETE FROM FaceDataTableX """ 
        self.im.execute(searchQuery)
        result =self.im.fetchall()
        self.db.commit() 
        return (result)
if __name__ == "__main__":
    app=SQLite()
    #app.DELETE()
    