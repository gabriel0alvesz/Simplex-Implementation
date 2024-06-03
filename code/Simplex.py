import numpy as np
from ReadDocs import ReadDocs
import time as tm

class Simplex:
    def __init__(self):
        self.n: int
        self.m: int
        self.c: np.array
        self.A: np.matrix
        self.b: np.array
        self.indexes_array: list

    def CreateMatrices(self, name_file: str):
        rd = ReadDocs()

        rd.ReadDoc(name_file)
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
            costs.append(np.squeeze(np.asarray(c_i).flatten()[0])) # parte de conversao gerada com chat gpt
    
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

    # Reason Test
    def Minimus(self, x_b, y):
        minimus = []
        
        for e in range(len(x_b)):
            min: float
            if(y[e][0] != 0):
                min = x_b[e][0]/y[e][0]
                min = np.squeeze(np.asarray(min).flatten()[0])
            else: 
                min = float('inf') # gambiarra para representar o maximo, ja que busco o minimo de todos

            minimus.append(min)
        return minimus

    def SwapColumns(self, value_k, value_n, base, no_base):
        base[base.index(value_n)] = value_k
        no_base[no_base.index(value_k)] = value_n

    def CalculateObjective(self, base, no_base, x_b):
        array_aux = np.zeros(len(base) + len(no_base))
        elements_not_null = [(b, float(x[0, 0])) for b, x in zip(base, x_b)]
        
        for x in elements_not_null:
            array_aux[x[0]] = np.array(x[1])
        
        return [np.dot(self.c, array_aux), array_aux]
        
    def InterationsSimplex(self):
        start = tm.time()
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

            if self.VerifyReducedCosts(reduced_costs): # Solução Ótima encontrada
                
                end = tm.time()
                print(f"Solução Otima encontrada em {end-start: .6f} segundos")
                result = self.CalculateObjective(base, no_base, x_B)
                print(f"Função Objetivo é {result[0]: .4f}")
                print("\nSolução:")

                for x in range(0,len(self.c)):
                    print(f"x[{x}] = {result[1][x]: .4f}")
                break
            
            
            index_K = no_base[reduced_costs.index(min(reduced_costs))] # indice da coluna que entrará na base

            # Calculo dos minimos
            Y = np.dot(B_inv, self.A[:,index_K])
            isUnlimitedProblem = all(e < 0 for e in Y)
            
            if isUnlimitedProblem:
                print("Problema Ilimitado!")
                break
            
            list_min = self.Minimus(x_B,Y)
            index_N = base[list_min.index(min(list_min))] # indice da coluna que irá sair da Base
            
            end = tm.time()
            print(f"Tempo(s): {end-start: .6f}")
            print(f"Objetivo: {self.CalculateObjective(base, no_base, x_B)[0]: .4f}")

            self.SwapColumns(index_K, index_N, base, no_base) # Troca os indices nos conjutos base e não base
            print("\n")

if __name__ == "__main__":

    sp = Simplex()

    name_file = input("Digite o Nome do arquivo com o formato: ")
    try:
        sp.CreateMatrices(name_file)

        sp.InterationsSimplex()
    except:
        print("Erro!")