class Student:
    def __init__(self,addr,client):
        self.addr = addr
        self.client = client
        self.name = None

    # setters
    def set_name(self,name):
        self.name = name
    

    # the __repr__ function/method returns the object's representation in string format, used to represent a class's object as a string
    def __repr__(self):
        return f"Student({self.addr},{self.name})"
