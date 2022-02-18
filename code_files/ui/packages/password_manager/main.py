from tinydb import TinyDB , Query
import tinydb_encrypted_jsonstorage as tae
from pySecureCryptos.randomWrapper import RandomID
from datetime import datetime
import pathlib








# main manager class
class PassManager:


    # init obj
    def __init__(self , key , path):
        
        self.db = TinyDB(encryption_key=key, path=path, storage=tae.EncryptedJSONStorage)
        
        try:
            self.db.all()
        except ValueError:
            raise RuntimeError("Invalid key or db")

        self.query = Query()



    # method to insert data into database
    def insert_new_pass(self , username , password , caption , url = "" , tags = "" , history = ""):
        
        tags = tags.split()
        
        self.db.insert({
            "id" : RandomID().md5() ,
            "username" : username , 
            "password" : password ,
            "url" : url , 
            "caption" : caption , 
            "tags" : tags ,
            "history" : history ,
        })



    # method to delete a password from database
    def delete_pass(self , id):
        self.db.remove(self.query.id == id)





    # method to update password in database
    def update_pass(self , id , username , password , caption , url = "" , tags = ""):

        # get current instance of password in db
        id_instance = self.db.search(self.query.id == id)[0]

        # get old pass and history
        oldPass = id_instance.get("password")
        history = id_instance.get("history")

        # if oldpassword is not same has new password , add it to history
        if(password != oldPass):
            history = f"""{oldPass} till {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\n""" + history

        tags = tags.split()

        print({
            "username" : username , 
            "password" : password ,
            "url" : url , 
            "caption" : caption , 
            "tags" : tags ,
            "history" : history ,
        })

        # update it
        self.db.update({
            "username" : username , 
            "password" : password ,
            "url" : url , 
            "caption" : caption , 
            "tags" : tags ,
            "history" : history ,
        } , 
        self.query.id == id)













def __test_Manager():

    obj = PassManager("hello" , "./test.db")

    obj.insert_new_pass("don" , "123456" , "None" , "don pass" , ["hello" , "don"])
    obj.insert_new_pass("john" , "123456" , "None" , "john pass" , ["john" , "don"])

    for i in obj.db.all():
        print(i)

    
    # obj.update_pass("95041738b422d27a20ad5d660c8952d6" , "newuser" , "newpass" , "caption of new user")


    # for i in obj.db.all():
    #     print(i)











def __test_Manager2():

    obj = PassManager("hello" , "./test.db")

    obj.insert_new_pass("don" , "123456" , "don thapar.com" , "None" , "edu")
    obj.insert_new_pass("john" , "123456" , "john gmail.com" , "None" , "google mail")
    obj.insert_new_pass("user1" , "123456" , "user1 gmail.com" , "None" , "google")
    obj.insert_new_pass("user2" , "123456" , "user2 facebook" , "None" , "meta")
    obj.insert_new_pass("user3" , "123456" , "user3 insta" , "None" , "gram")
    obj.insert_new_pass("user4" , "123456" , "user4 whatsapp" , "None" , "meta")
    obj.insert_new_pass("user5" , "123456" , "user5 example" , "None" , "url")
    obj.insert_new_pass("user6" , "123456" , "user6 canva" , "None" , "photo")
    obj.insert_new_pass("user7" , "123456" , "user7 yahoo" , "None" , "mail")
    obj.insert_new_pass("user8" , "123456" , "user8 proton" , "None" , "vpn")

    for i in obj.db.all():
        print(i)

    # obj.db.update({'username': 'don', 'password': '12345678', 'url': 'don thapar.com', 'caption': 'None', 'tags': ['edu'], 'history': ''} , obj.query.id == "1dec21f1763df1ab890d1ce598385143")

    # input()
    # print("\n\n")

    # for i in obj.db.all():
    #     print(i)
    # obj.update_pass("ee134df0724c72e807a08a21ea28f428" , "user8" , "12345678" , "user8 proton" , "None" , "vpn")


    # for i in obj.db.all():
    #     print(i)






if __name__ == "__main__":
    __test_Manager2()