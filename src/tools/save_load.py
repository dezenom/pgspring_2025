from json import load ,dump


class SaveLoad:
    def __init__(self,path):
        self.path = path

    def save(self,file_name,data):
        with open(f"{self.path}/{file_name}.json","w") as f:
            dump(data,f)
    def load(self,file_name,base = {}):
        try:
            file = open(f"{self.path}/{file_name}.json")
            data = load(file)
            return data
            file.close()
        except:
            return base
