import numpy as np
from ReadDocs import ReadDocs

class Simplex:
    def __init__(self):
        self.n: int
        self.m: int
        self.c: np.array
        self.A: np.matrix
        self.b: np.array
        self.indexes_array: list

    def CreateMatrices(self):
        rd = ReadDocs()
        rd.ReadDoc("input.txt")
        rd.Tokenizer()
        list_aux = rd.DefineMatrices()

        self.n, self.m = list_aux[0:2]
        self.c = np.array(list_aux[2])
        self.A = np.matrix(list_aux[3])
        self.b = np.array(list_aux[-1]).reshape(-1,1)

        self.indexes_array = list(i for i in range(self.n))

    def PrintData(self):
        print("Numero de Variáveis: ", self.n)
        print("Numero de Restrições: ", self.m)
        print("Coeficientes da Função: ", self.c)
        print("Matriz mxn", self.A)
        print("Termos independentes: ", self.b)
        print("Indices: ",self.indexes_array)
    
    def CalculateReducedCosts(self, multiply_array, no_base: list) -> list:
        costs: list = []
        for i in no_base:
            part_aux = np.dot(multiply_array, self.A[:,i])
            c_i = np.array(self.c[i]) - part_aux
            costs.append(np.squeeze(np.asarray(c_i).flatten()[0])) # Chat gpt salvou nessa parte
    
        return costs
    
    def VerifyReducedCosts(self, costs: list) -> bool:
        cont: int = 0
        
        for i in costs:

            if i >= 0:
                cont += 1

        if cont == len(costs):
            return True #Solução ótima encontrada -> todos os custos maiores que zero
        else:
            return False # Ainda a custos negativos
    def DefineNewIndexBase(self, costs: list, no_base: list) -> int:

        index = costs.index(min(costs))

        print(index)
        


    def InterationsSimplex(self):
        # Sempre começa com a matriz identidade -> n = 5 e m = 2 => os indices da matriz identidade ser de (n-m) até (n-1)

        base = list(self.indexes_array[self.m-1:self.n]) # self.m-1 por indices começarem em zero.
        no_base = list(self.indexes_array[0:self.m-1])
        cont: int = 0
        
        while True:
            cont += 1
            print("Interação: ", cont)

            B_inv = np.linalg.inv(self.A[:, base]) # matriz inversa
            
            x_B = np.dot(B_inv,self.b) # solucao particular

            # Custos reduzidos
            c_B = tuple(self.c[base])
            p_t = np.array(np.dot(c_B,B_inv))
            
            reduced_costs = self.CalculateReducedCosts(p_t,no_base)
            print(reduced_costs)

            if self.VerifyReducedCosts(reduced_costs): # Solução Ótima encontrada
                
                break
            
            # Qual indice sairá da nao base entrará na base
            index_go_base = no_base[reduced_costs.index(min(reduced_costs))]
            


            break
    
        
            

        


if __name__ == "__main__":

    sp = Simplex()

    sp.CreateMatrices()

    # sp.PrintData()

    sp.InterationsSimplex()
