import random

class Prueba:
    def __init__(self):
        self.celcius = [7, 12, 21, 30, 32, 47, 58]
        self.faren = [44.6, 53.6, 69.8, 86, 87.8, 116.6, 136.4]
        self.pesos = []
        self.sezgos = []
        self.resultados = [[], []]
        self.validos = [[], []]
        self.invalidos = [[], []]
        self.aumento = ""
        self.entrenado = False
        self.es_peso = False
        self.peso = 0
        self.sezgo = 0
        self.limPeso = 1
        self.limSezgo = 1
        self.file_path = "validos_aleatorios.txt"  # Archivo donde se guardarán los pares válidos
        self.cargar_memoria()

    def entrenador(self, iteraciones, presicion, paso):
        if self.entrenado:
            return
        valor = 0
        while valor < len(self.celcius):
            for i in range(int(iteraciones) +1):
                for j in range(int(iteraciones) +1):
                    #Verificar que el valor no se salga del rango de items que tenemos disponibles
                    if valor < len(self.celcius):
                        resultado = self.operador(self.celcius[valor], self.faren[valor], iteraciones, presicion, valor)
                        if resultado == "sube":
                            self.limSezgo += paso
                        if resultado == "baja":
                            if self.limSezgo > 0:
                                self.limSezgo -= paso
                            else:
                                self.peso-= paso
                        if resultado == "igual":
                            print(f"Igual encontrado en Iteracion {i * j}")
                            self.pesos = []
                            self.sezgos = []
                            self.peso = 0
                        print(f"Index {valor}: Celcius {self.celcius[valor]}, ResultadoN {self.resultados[0][-1]}, ResultadoT {self.resultados[1][-1]}, Faren {self.faren[valor]}, peso {self.peso}, sezgo {self.sezgo}")
                        # Aumentar el paso cada 1/10 de las iteraciones de n para alcanzar mas resultados
                        if (j + 1) % 10 == 0:
                            self.limPeso += paso
                            self.limPeso = round(self.limPeso, presicion)
                    
                valor += 1
                if valor >= len(self.celcius):
                    break

        self.operar_todos(presicion)
        print("Entrenamiento terminado")


    def operador(self, entrada, salida, iteraciones, presicion, valor):
        resultado = None  # Inicializamos resultado con None
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
                nodos = self.unicos(presicion)
                resultado = (entrada * nodos[0]) + nodos[1]
                if resultado < salida:
                    self.aumento = "sube"
                    self.invalidos[0].append(self.pesos[-1])
                    self.invalidos[1].append(self.sezgos[-1])
                elif resultado > salida:
                    self.aumento = "baja"
                    self.invalidos[0].append(self.pesos[-1])
                    self.invalidos[1].append(self.sezgos[-1])
                else:
                    self.aumento = "igual"
                    self.validos[0].append(self.pesos[-1])
                    self.validos[1].append(self.sezgos[-1])
                    print(f"Igual encontrado {entrada} para el valor {resultado} con el peso {nodos[0]} y sezgo {nodos[1]}")
        else:
            nodos = self.unicos( presicion)
            resultado = (entrada * nodos[0]) + nodos[1]
            if resultado < salida:
                self.aumento = "sube"
                self.invalidos[0].append(self.pesos[-1])
                self.invalidos[1].append(self.sezgos[-1])
            elif resultado > salida:
                self.aumento = "baja"
                self.invalidos[0].append(self.pesos[-1])
                self.invalidos[1].append(self.sezgos[-1])
            else:
                self.aumento = "igual"
                self.validos[0].append(self.pesos[-1])
                self.validos[1].append(self.sezgos[-1])
                print(f"Igual encontrado {entrada} para el valor {resultado} con el peso {nodos[0]} y sezgo {nodos[1]}")

        # Almacena los resultados
        self.resultados[0].append(round(resultado, presicion))
        self.resultados[1].append(self.aumento)

        return self.aumento
    
    def operar_todos(self, presicion):
        
        i = 0
        while i < len(self.celcius):
            c = self.celcius[i]
            f = self.faren[i]
            
            index = None
            remover = False  # Variable para controlar si se debe eliminar el par de validos
            
            if self.validos[0]:
                for idx in range(len(self.validos[0])):
                    self.peso = self.validos[0][idx]
                    self.sezgo = self.validos[1][idx]
                    print(f"Operacion: {c} * {self.peso} + {self.sezgo} = {round((c * self.peso) + self.sezgo)}, se espera {f}")
                    if round((c * self.peso) + self.sezgo, presicion) != f:
                        remover = True  # Se encontró un par inválido, se puede eliminar
                        index = idx
                    
                if remover:
                    print(f"Movido a invalidos: Celcius: {c}, Faren: {f}")
                    self.invalidos[0].append(self.validos[0].pop(index))
                    self.invalidos[1].append(self.validos[1].pop(index))
                else:
                    # Si no se encontró ningún par válido o no se debe remover
                    print(f"¡Par válido para Celcius: {c}, Faren: {f}! con peso {self.peso} y sezgo {self.sezgo}")
                
                i += 1
                print(f"Celcius: {c}, Faren: {f}, Resultado: {round((c * self.peso) + self.sezgo)} {'igual' if not remover else 'invalido'}")
            else:
                break

        self.imprimir_validos()
        self.guardar_memoria()

    def unicos(self, presicion):
        ciclo = 0
        while ciclo < len(self.invalidos[0]):
            valorP = round(random.uniform(0, self.limPeso), presicion)
            valorS = round(random.uniform(0, self.limSezgo), presicion)
            
            # Verificar que no esté en invalidos
            if not self.pares_repetidos(valorP, valorS) and (valorP not in self.invalidos[0] or valorS not in self.invalidos[1]):
                break
            ciclo += 1
        if ciclo >= len(self.invalidos[0]):
            self.entrenado = True
            print(f"No se encontraron valores únicos luego de {len(self.invalidos[0])} intentos")
        self.pesos.append(valorP)
        self.sezgos.append(valorS)
        self.peso = valorP
        self.sezgo = valorS
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

    def guardar_memoria(self):
        with open(self.file_path, "w") as file:
            # Guardar datos válidos
            validos_uniq = list(set(zip(self.validos[0], self.validos[1])))
            invalidos_set = set(zip(self.invalidos[0], self.invalidos[1]))
            
            validos_filtrados = [(peso, sezgo) for peso, sezgo in validos_uniq if (peso, sezgo) not in invalidos_set]
            
            for peso, sezgo in validos_filtrados:
                file.write(f"{peso},{sezgo}\n")
            
            # Guardar datos inválidos
            for peso, sezgo in zip(self.invalidos[0], self.invalidos[1]):
                file.write(f"INVALIDO,{peso},{sezgo}\n")
    
    def cargar_memoria(self):
        try:
            with open(self.file_path, "r") as file:
                for line in file:
                    if line.startswith("INVALIDO"):
                        _, peso, sezgo = line.strip().split(",")
                        self.invalidos[0].append(float(peso))
                        self.invalidos[1].append(float(sezgo))
                    else:
                        peso, sezgo = line.strip().split(",")
                        self.validos[0].append(float(peso))
                        self.validos[1].append(float(sezgo))
        except FileNotFoundError:
            print(f"Archivo {self.file_path} no encontrado. No se cargaron valores.")

prueba = Prueba()
# Entrenar
prueba.entrenador(10, 1, 0.1)
