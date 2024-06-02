
class ReadDocs:

    def __init__(self):
        self.lines: list
    
    def ReadDoc(self, name_doc: str):
        with open(name_doc,'r') as f:
            self.lines = f.readlines()
    
    def Tokenizer(self):
        self.lines = [line.strip().split() for line in self.lines]


    
    # 5 3
    # -180 -300 0 0 0
    # 1 0 1 0 0 60
    # 0 1 0 1 0 50
    # 1 1 0 0 1 120

    def DefineMatrices(self) -> list:
        n, m = map(int, self.lines[0][0:2])
        c = list(map(float, self.lines[1]))
        A = [[float(self.lines[i][j]) for j in range(0,n)] for i in range(2,n)]
        b = [float(self.lines[i][n]) for i in range(2,n)]
        return [n, m, c, A, b]

   
            

if __name__ == "__main__":
    rd = ReadDocs()

    rd.ReadDoc("input.txt")

    rd.Tokenizer()

    print(rd.DefineMatrices())