## not integrated

class chunk_map():
    def __init__(self,chunk_size=(),data=[]):
        self.full_map = {}
        self.av_map = {}
        self.chunk_size = chunksize
        self.chunking(data)
        print("--------------------------------------------")
        print('finished chunking')
        print("--------------------------------------------")

    def chunking(self,data,row_ind=0,col_ind=0):
        chunk= []

        for rdex,row in enumerate(data):
            row_in_chunk= []
            if rdex > row_ind-1 and rdex < row_ind+self.chunk_size[1]:
                for cdex ,col in enumerate(row):
                    if cdex > col_ind-1 and cdex < col_ind+self.chunk_size[0]:
                        row_in_chunk.append(col)

            chunk.append(row_in_chunk)
            if rdex == row_ind-1+self.chunk_size[1] or rdex == len(data)-1:
                self.full_map[f"{int(col_ind/self.chunk_size[0])}:{int(row_ind/self.chunk_size[1])}"]= (chunk,(int(col_ind/self.chunk_size[0]),int(row_ind/self.chunk_size[1])))
                row_ind+=self.chunk_size[1]
                chunk = []

            if rdex == len(data)-1 and col_ind + self.chunk_size[0] < len(data[0]):
                self.chunking(data,col_ind=col_ind+self.chunk_size[0])

    def get_avmap(self,pos=()):
        self.av_map = []
        cut = [-1,-1]
        key = f"{pos[0]+cut[0]}:{pos[1]+cut[1]}"

        for y in range(1):
            for x in range(2):
                if key in self.full_map.keys():
                    self.av_map.append(key)
                cut[0] += 1
                key = f"{pos[0]+cut[0]}:{pos[1]+cut[1]}"
            cut[1] +=1
            cut[0] = -1
            key = f"{pos[0]+cut[0]}:{pos[1]+cut[1]}"

