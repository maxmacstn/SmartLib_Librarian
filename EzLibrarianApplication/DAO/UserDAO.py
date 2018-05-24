from Book import Book
from datetime import datetime
from DAO.AbstractDAO import AbstractDAO
from constant import rfc_822_format
from User import User
import requests
import random

# Non-server test
#
# class UserDAO:
#     def __init__(self,parent = None, serverIP = "10.0.0.1"):
#         self.ip = serverIP
#         self.parent = parent
#
#
#     def getUserFromID(self, id):
#         # Fake loading
#         time.sleep(0.5)
#
#         if (id == "59090030"):
#             self.parent.login_callback(Student(59090030,"Sitinut","Waisara","ycrnAC5g1ekyjeF925i0gNbZQMuZWQ2MkIjIEzYBsZ3"))
#
#         else:
#             self.parent.login_callback(None)
#
#     def getUserFromRFID_ID(self, rfid_id):
#         # Fake loading
#         time.sleep(0.5)
#
#         if (rfid_id == "f3e09a4f"):
#             self.parent.login_callback(Student(59090030,"Sitinut","Waisara","ycrnAC5g1ekyjeF925i0gNbZQMuZWQ2MkIjIEzYBsZ3"))
#         else:
#             self.parent.login_callback(None)



# class UserDAO(AbstractDAO):
#     def __init__(self, parent = None):
#         AbstractDAO.__init__(self)
#         self.parent = parent
#
#
#     def getUserFromID(self, id):
#         print("Get info id : " + str(id))
#         response = requests.get(self.server_ip + '/user/' + str(id))
#
#         user = self.constructUser(response.json())
#
#         if self.parent is not None:
#             self.parent.login_callback(user)
#
#         return user
#
#     def getUserFromRFID_ID(self, rfid):
#         response = requests.get(self.server_ip + '/user/rfid/' + str(rfid))
#
#         user = self.constructUser(response.json())
#
#         if self.parent is not None:
#             self.parent.login_callback(user)
#
#         self.parent.login_callback(user)
#         return user
#
#     @staticmethod
#     def constructUser(arguments):
#         arguments['registered_on'] = datetime.strptime(arguments['registered_on'], rfc_822_format)
#
#         return User(**arguments)
#
# if __name__ == "__main__":
#     userDAO = UserDAO()
#     print(userDAO.getUserFromID(1).name)


class UserDAO(AbstractDAO):
    def __init__(self, parent=None):
        AbstractDAO.__init__(self)
        self.parent = parent

    def getUserFromID(self, id):
        print("Get info id : " + str(id))
        try :
            response = requests.get(self.server_ip + '/user/' + str(id), timeout = self.timeout)
            user = None
            if response.status_code == 200:   # Success
                user = self.constructUser(response.json())

        except requests.exceptions.ConnectTimeout:  # Connection timeout, use offline mockup data
            user = User(3,"OFFLINE USER",datetime.now(),"Test@gmail.com",True)
            print("Waring! use offline data for debugging only")



        if self.parent is not None:
            self.parent.login_callback(user)

        return user

    def getUserFromRFID_ID(self, rfid):
        try:
            response = requests.get(self.server_ip + '/user/rfid/' + str(rfid), timeout=self.timeout)
            user = None
            if response.status_code == 200:     #Success
                user = self.constructUser(response.json())

        except requests.exceptions.ConnectTimeout:    # Connection timeout, use offline mockup data
            user = User(3,"OFFLINE USER",datetime.now(),"Test@gmail.com",True)
            print("Waring! use offline data for debugging only")

        if self.parent is not None:
            self.parent.login_callback(user)

        return user

    def getAllUsers(self):
        try:
            response = requests.get(self.server_ip + '/user', timeout=self.timeout)
            user = None
            if response.status_code == 200:
                to_return = []
                for raw_data in response.json():
                    to_return.append(self.constructUser(raw_data))
                return to_return

        except requests.exceptions.ConnectTimeout:  # Connection timeout, use offline mockup data
            print("Timeout")

        return None



    @staticmethod
    def constructUser(arguments):
        if arguments == None:
            return None

        time_arg = "registered_on"

        arguments[time_arg] = datetime.strptime(arguments[time_arg], rfc_822_format)

        return User.User(**arguments)

    def addUser(self, user: User):
        dict_to_add = user.__dict__
        del dict_to_add['user_id']
        del dict_to_add['registered_on']
        del dict_to_add['lineToken']

        print(dict_to_add)

        response = requests.post(self.server_ip + '/user', json=dict_to_add, timeout=self.timeout)
        if response.status_code == 201:  # Success
            print(response.json())
            pass

    def updateUser(self, user:User):
        dict_to_add = user.__dict__
        del dict_to_add['registered_on']
        del dict_to_add['lineToken']

        print(dict_to_add)

        response = requests.put(self.server_ip + '/user/' + str(user.user_id), json=dict_to_add, timeout=self.timeout)
        if response.status_code == 200:  # Success
            print(response.json())
            pass
        else:
            print("Failed")

    def deleteUser(self,user:User):

        response = requests.delete(self.server_ip + '/user/' + str(user.user_id), timeout=self.timeout)
        if response.status_code == 200:  # Success
            print(response.json())
            pass
        else:
            print("Failed")

    def searchUser(self, keyword:str):
        if keyword == "" or keyword.startswith(' '):
            return self.getAllUsers()

        try:
            response = requests.get(self.server_ip + '/user/search/' + str(keyword), timeout=self.timeout)
            user = None
            if response.status_code == 200:
                to_return = []
                for raw_data in response.json():
                    to_return.append(self.constructUser(raw_data))
                return to_return

        except requests.exceptions.ConnectTimeout:  # Connection timeout, use offline mockup data
            print("Timeout")

        return None


if __name__ == "__main__":
    userDAO = UserDAO()
    print(userDAO.getUserFromID(1).name)
