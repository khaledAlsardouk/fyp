class userClass:
    def __init__(self, fName, lName, password,DOB,email,phoneNo,userID,inventory,groceryList, preferences):
        self.firstName= fName
        self.lastName= lName
        self.password = password
        self.DOB= DOB
        self.email= email
        self.phoneNo= phoneNo
        self.userID= userID
        self.inventory= inventory
        self.groceryList= groceryList
        self.preferences= preferences
    #def printwhole()
    def getfirstName(self):
        return self.firstName

    def getlasttName(self):
        return self.lastName

    def getDOB(self):
        return self.DOB

    def getphoneNo(self):
        return self.phoneNo

    def getinventory(self):
        return self.inventory

    def getgroceryList(self):
        return self.groceryList

    def getpreferences(self):
        return self.preferences

    def validPassword(self, gven):
        valid = bool(False)
        if ( self.password == gven ):
            valid = bool(True)
        return valid




bata = userClass ("wqerqew", "dffgs", "python420", 1234, "helo@outloo.com",1234234,1,67,"yes","yes")

print("testng here")
x = bata.getfirstName()

print(bata.validPassword("python430"))

