
class Ubject(object):
    def __init__(self):
        self.__namespaces = {}

    def doit(self):
        print("this func gets called")

    def __getattr__(self, name):
        ns = self.__namespaces.get(name, None)
        if ns is None:
            print("you are invoking calling :",name)
            ns = self.doit
            self.__namespaces[name] = ns
        return ns
        
obj = Ubject()
obj.hello()
