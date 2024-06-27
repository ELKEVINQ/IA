import random

class Prueba:
    def __init__(self):
        self.celcius = [7, 12, 21, 30, 32, 47, 58]
        self.faren = [44.6, 53.6, 69.8, 86, 89.6, 116.6, 136.4]
        self.pesos = []
        self.sezgos = []
        self.resultados = []
        self.validos = set()
        self.invalidos = set()
        self.aumento = ""
        self.entrenado = False
        self.es_peso = False
        self.peso = 0
        self.sezgo = 0
        self.limSup = 1
        self.limPeso = 1
        self.file_path = "validos_aleatorios.txt"  # Archivo donde se guardarán los pares válidos
        self.cargar_memoria()

    def entrenador(self, iteraciones, presicion, paso):
        if self.entrenado:
            return
        for i in range(len(self.celcius)):
            for j in range(int(iteraciones) + 1):
                # Verificar que el valor no se salga del rango de items que tenemos disponibles
                resultado = self.operador(self.celcius[i], self.faren[i], presicion)
                if resultado == "sube":
                    if (self.faren[i] - self.resultados[-1][0]) >= 100:
                        self.limSup += paso * 100
                    elif (self.faren[i] - self.resultados[-1][0]) >= 10:
                        self.limSup += paso * 10
                    elif (self.faren[i] - self.resultados[-1][0]) >= 1:
                        self.limSup += 1
                    self.limPeso = self.limSup / 10
                if resultado == "baja":
                    if self.limSup > 0:
                        if (self.resultados[-1][0] - self.faren[i]) >= 100:
                            self.limSup -= paso * 100
                        elif (self.resultados[-1][0] - self.faren[i]) >= 10:
                            self.limSup -= paso * 10
                        elif (self.resultados[-1][0] - self.faren[i]) >= 1:
                            self.limSup -= 1
                    else:
                        self.limSup += 10
                    self.limPeso = self.limSup / 10
                if resultado == "igual":
                    print(f"Igual encontrado en Iteracion {j - iteraciones}")
                    print(f"Index {i}: Celcius {self.celcius[i]}, ResultadoN {self.resultados[-1][0]}, Faren {self.faren[i]}, peso {self.peso}, sezgo {self.sezgo}")
            

        self.operar_todos(presicion)
        print("Entrenamiento terminado")

    def operador(self, entrada, salida, presicion):
        resultado = None
        nodos = self.unicos(presicion)
        resultado = (entrada * nodos[0]) + nodos[1]
        if resultado < salida:
            self.aumento = "sube"
        elif resultado > salida:
            self.aumento = "baja"
        else:
            self.aumento = "igual"
            self.validos.add((self.pesos[-1], self.sezgos[-1]))  # Agregar los últimos valores generados
            print(f"Igual encontrado {entrada} para el valor {resultado} con el peso {nodos[0]} y sezgo {nodos[1]}")

        self.resultados.append((round(resultado, presicion), self.aumento))
        return self.aumento
    
    def operar_todos(self, presicion):
        i = 0
        while i < len(self.celcius):
            c = self.celcius[i]
            f = self.faren[i]
            remover = False
            
            if self.validos:
                for peso, sezgo in self.validos:
                    print(f"Operacion: {c} * {peso} + {sezgo} = {round(((c * peso) + sezgo), presicion)}, se espera {f}")
                    if round((c * peso) + sezgo, presicion) != f:
                        remover = True
                        print(f"¡Par invalido para Celcius: {c}, Faren: {f}! con peso {peso} y sezgo {sezgo}")
                        self.invalidos.add((peso, sezgo))
                        continue
                
                if not remover:
                    print(f"¡Par válido para Celcius: {c}, Faren: {f}! con peso {peso} y sezgo {sezgo}")
            
            else:
                # Si no hay pares válidos, no hay nada que hacer
                break

            print(f"Celcius: {c}, Faren: {f}, Resultado: {round((c * peso) + sezgo)} {'igual' if not remover else 'invalido'}")
            
            i += 1  # Aumentar i solo al terminar de revisar todos los pares válidos
            
        # Comparar y eliminar pares duplicados entre validos e invalidos
        self.validos.difference_update(self.invalidos)
        
        self.imprimir_validos()
        self.guardar_memoria()

    def unicos(self, presicion):
        while True:
            valorP = round(random.uniform(0, self.limPeso), presicion)
            valorS = round(random.uniform(0, self.limSup), presicion)
            par = (valorP, valorS)
            
            if par not in self.validos and par not in self.invalidos:
                self.pesos.append(valorP)
                self.sezgos.append(valorS)
                self.peso = valorP
                self.sezgo = valorS
                return [valorP, valorS]

    def pares_repetidos(self, valorP, valorS, lista_pesos, lista_sezgos):
        for p, s in zip(lista_pesos, lista_sezgos):
            if p == valorP and s == valorS:
                return True
        return False

    def imprimir_validos(self):
        print("Valores en validos:")
        for peso, sezgo in self.validos:
            print(f"Peso: {peso}, Sezgo: {sezgo}")

    def guardar_memoria(self):
        with open(self.file_path, "w") as file:
            for peso, sezgo in self.validos:
                file.write(f"{peso},{sezgo}\n")
            for peso, sezgo in self.invalidos:
                file.write(f"INVALIDO,{peso},{sezgo}\n")
    
    def cargar_memoria(self):
        try:
            with open(self.file_path, "r") as file:
                for line in file:
                    if line.startswith("INVALIDO"):
                        _, peso, sezgo = line.strip().split(",")
                        self.invalidos.add((float(peso), float(sezgo)))
                    else:
                        peso, sezgo = line.strip().split(",")
                        self.validos.add((float(peso), float(sezgo)))
        except FileNotFoundError:
            print(f"Archivo {self.file_path} no encontrado. No se cargaron valores.")

prueba = Prueba()
# Entrenar
prueba.entrenador(100000, 1, 0.2)
