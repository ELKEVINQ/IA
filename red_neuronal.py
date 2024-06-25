import random

class Prueba:
    def __init__(self):
        self.celcius = [7, 12, 21, 30, 32, 47, 58]
        self.faren = [44.6, 53.6, 69.8, 86, 87.8, 116.6, 136.4]
        self.pesos = []
        self.sezgos = []
        self.resultados = [[], []]
        self.validos = [[], []]
        self.aumento = ""
        self.entrenado = False
        self.lSup = 1.0
        self.lInf = 0.0
        self.file_path = "validos.txt"  # Archivo donde se guardarán los pares válidos
        self.cargar_validos()

    def entrenador(self, iteraciones, paso, presicion):
        if self.entrenado:
            return
        valor = 0
        for i in range(iteraciones + 1):
            if valor < len(self.celcius):
                resultado = self.operador(self.celcius[valor], self.faren[valor], iteraciones, presicion)
                if resultado == "sube":
                    self.lSup += paso
                elif resultado == "baja":
                    if not self.lInf > self.lSup:
                        self.lSup -= paso
                    else: 
                        self.lSup += paso
                    self.lSup = round(self.lSup, presicion)
                elif resultado == "igual":
                    print(f"Igual encontrado en Iteracion {i}")
                    self.pesos = []
                    self.sezgos = []
                    self.lInf = 0
                    valor += 1
                print(f"Index {valor}: Celcius {self.celcius[valor]}, ResultadoN {self.resultados[0][-1]}, ResultadoT {self.resultados[1][-1]}, Faren {self.faren[valor]}, LSup {self.lSup}, LInf {self.lInf}")
            else:
                self.entrenado = True
                print(f"Entrenamiento completado en Iteracion {i}")
                break  # Salir del bucle de iteraciones

        self.entrenado = True
        print("Entrenamiento terminado")

        self.imprimir_validos()
        self.guardar_validos()

    def operador(self, entrada, salida, iteraciones, presicion):
        if self.validos[0] and self.validos[1]:  # Verifica que ambas listas no estén vacías
            for index in range(len(self.validos[0])):
                peso_actual = self.validos[0][index]
                sezgo_actual = self.validos[1][index]
                resultado = (entrada * peso_actual) + sezgo_actual
                if resultado < salida:
                    self.aumento = "sube"
                elif resultado > salida:
                    self.aumento = "baja"
                else:
                    self.aumento = "igual"
                    print(f"Igual encontrado {entrada} para el valor {resultado} con el peso {peso_actual} y sezgo {sezgo_actual}")
                    break
            else:
                nodos = self.unicos(iteraciones, presicion)
                resultado = (entrada * nodos[0]) + nodos[1]
                if resultado < salida:
                    self.aumento = "sube"
                elif resultado > salida:
                    self.aumento = "baja"
                else:
                    self.aumento = "igual"
                    self.validos[0].append(self.pesos[-1])
                    self.validos[1].append(self.sezgos[-1])
                    print(f"Igual encontrado {entrada} para el valor {resultado} con el peso {nodos[0]} y sezgo {nodos[1]}")
        else:
            nodos = self.unicos(iteraciones, presicion)
            resultado = (entrada * nodos[0]) + nodos[1]
            if resultado < salida:
                self.aumento = "sube"
            elif resultado > salida:
                self.aumento = "baja"
            else:
                self.aumento = "igual"
                self.validos[0].append(self.pesos[-1])
                self.validos[1].append(self.sezgos[-1])
                print(f"Igual encontrado {entrada} para el valor {resultado} con el peso {nodos[0]} y sezgo {nodos[1]}")

        # Almacena los resultados
        self.resultados[0].append(str(resultado))
        self.resultados[1].append(self.aumento)

        return self.aumento

    def unicos(self, iteraciones, presicion):
        tries = 0
        while tries < iteraciones:
            valorP = round(random.uniform(self.lInf, self.lSup), presicion)
            valorS = round(random.uniform(self.lInf, self.lSup), presicion)
            if not self.pares_repetidos(valorP, valorS):
                break
            tries += 1
        if tries >= iteraciones:
            self.entrenado = True
            print(f"No se encontraron valores únicos luego de {iteraciones} intentos")
        self.pesos.append(valorP)
        self.sezgos.append(valorS)
        return [valorP, valorS]

    def pares_repetidos(self, valorP, valorS):
        for p, s in zip(self.pesos, self.sezgos):
            if p == valorP and s == valorS:
                return True
        return False
    
    def imprimir_validos(self):
        print("Valores en validos:")
        for i in range(len(self.validos[0])):
            print(f"Peso: {self.validos[0][i]}, Sezgo: {self.validos[1][i]}")

    def guardar_validos(self):
        with open(self.file_path, "w") as file:
            for i in range(len(self.validos[0])):
                file.write(f"{self.validos[0][i]},{self.validos[1][i]}\n")

    def cargar_validos(self):
        try:
            with open(self.file_path, "r") as file:
                for line in file:
                    peso, sezgo = line.strip().split(",")
                    self.validos[0].append(float(peso))
                    self.validos[1].append(float(sezgo))
        except FileNotFoundError:
            print(f"Archivo {self.file_path} no encontrado. No se cargaron valores.")

prueba = Prueba()
# Entrenar
prueba.entrenador(100, 0.1, 1)
