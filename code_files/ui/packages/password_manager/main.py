from tinydb import TinyDB , Query
import tinydb_encrypted_jsonstorage as tae
from pySecureCryptos.randomWrapper import RandomID
from datetime import datetime









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






if __name__ == "__main__":
    __test_Manager()