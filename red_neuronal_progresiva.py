import random

class Prueba:
    def __init__(self):
        self.celcius = [7, 12, 21, 30, 32, 47, 58]
        self.faren = [44.6, 53.6, 69.8, 86, 89.6, 116.6, 136.4]
        self.pesos = []
        self.sezgos = []
        self.resultados = [[], []]
        self.validos = [[], []]
        self.invalidos = [[], []]
        self.aumento = ""
        self.entrenado = False
        self.lSup = 1
        self.lInf = 0
        self.peso = 0
        self.sezgo = 0
        self.file_path = "validos_progresivos.txt"  # Archivo donde se guardarán los pares válidos
        self.cargar_memoria()

    def transformar_numero(self, numero):
        # Implement the transformation logic using self.validos if available
        if self.validos and len(self.validos[0]) > 0:
            peso = self.validos[0][0]
            sezgo = self.validos[1][0]
            resultado = numero * peso + sezgo
            print(f"Resultado de la transformación: {resultado}")
        else:
            print("No hay pesos y sesgos válidos disponibles para transformar el número.")

    def menu_principal(self):
        while True:
            print("\nMenu Principal:")
            print("1. Entrenar")
            print("2. Transformar número")
            print("3. Salir")
            opcion = input("Seleccione una opción (1/2/3): ")

            if opcion == "1":
                self.menu_entrenar()
            elif opcion == "2":
                self.menu_transformar()
            elif opcion == "3":
                print("Saliendo del programa.")
                break
            else:
                print("Opción no válida. Por favor, seleccione 1, 2 o 3.")

    def menu_entrenar(self):
        iteraciones = int(input("Ingrese el número de iteraciones para el entrenamiento: "))
        presicion = int(input("Ingrese la precisión deseada para el entrenamiento: "))
        paso = float(input("Ingrese el paso para el entrenamiento: "))
        
        self.entrenador(iteraciones, presicion, paso)

    def menu_transformar(self):
        if self.validos and len(self.validos[0]) > 0:
            numero = float(input("Ingrese el número que desea transformar: "))
            self.transformar_numero(numero)
        else:
            print("No hay pesos y sesgos válidos disponibles para transformar el número.")

    def entrenador(self, iteraciones, presicion, paso):
        
        valor = 0
        while valor < len(self.celcius):
            for j in range(int(iteraciones) + 1):
                for n in range(int(iteraciones) + 1):
                    if valor < len(self.celcius):  # Verificar antes de procesar
                        resultado = self.operador(self.celcius[valor], self.faren[valor], iteraciones, presicion, valor)
                        if resultado == "sube":
                            if (self.faren[valor] - self.resultados[0][-1]) >= 100:
                                self.lSup += 100
                            elif (self.faren[valor] - self.resultados[0][-1]) >= 10:
                                self.lSup += 10
                            elif (self.faren[valor] - self.resultados[0][-1]) >= 1:
                                self.lSup += 1
                        elif resultado == "baja":
                            if (self.resultados[0][-1] - self.faren[valor]) >= 100:
                                self.lSup -= 100
                            elif (self.resultados[0][-1] - self.faren[valor]) >= 10:
                                self.lSup -= 10
                            elif (self.resultados[0][-1] - self.faren[valor]) >= 1:
                                self.lSup -= 1
                        elif resultado == "igual":
                            print(f"Igual encontrado en Iteracion {n}")
                            self.pesos = []
                            self.sezgos = []
                            self.peso = 0
                            valor += 1
                            break  # Salir del bucle de iteraciones internas
                        
                        print(f"Index {valor}: Celcius {self.celcius[valor]}, ResultadoN {self.resultados[0][-1]}, ResultadoT {self.resultados[1][-1]}, Faren {self.faren[valor]}, LSup {self.lSup}, LInf {self.lInf}, Peso {self.peso}, Sezgo {self.sezgo}", end="")

                        # Aumentar el paso cada 1/10 de las iteraciones de n
                        if (n + 1) % (iteraciones // 10) == 0:
                            self.peso += paso
                            self.peso = round(self.peso, 2)
                
                valor += 1
                self.peso = 0
                
                # Verificar si se completaron todas las iteraciones
                if valor >= len(self.celcius):
                    break
        
        
        self.operar_todos(presicion)
        print("Entrenamiento terminado")


    def operador(self, entrada, salida, iteraciones, presicion, valor):
        resultado = None  # Inicializamos resultado con None
        
        if self.validos[0] and self.validos[1]:
            encontrado = False
            for index in range(len(self.validos[0])):
                peso = self.validos[0][index]
                sezgo = self.validos[1][index]
                resultado = (entrada * peso) + sezgo
                if resultado < salida:
                    self.aumento = "sube"
                elif resultado > salida:
                    self.aumento = "baja"
                else:
                    self.aumento = "igual"
                    print(f"Igual encontrado {entrada} para el valor {resultado} con el peso {peso} y sezgo {sezgo}")
                    encontrado = True
                    break
            if not encontrado:
                nodos = self.unicos(iteraciones, presicion)
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
            nodos = self.unicos(iteraciones, presicion)
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
                
        self.resultados[0].append(resultado)
        self.resultados[1].append(self.aumento)
        
        return self.aumento

    def operar_todos(self, presicion):
        if self.entrenado:
            print("El modelo ya ha sido entrenado. No se puede operar todos los elementos.")
            return
        
        print("Operando con todos los elementos disponibles:")
        i = 0
        while i < len(self.celcius):
            c = self.celcius[i]
            f = self.faren[i]
            
            index = None
            remover = False  # Variable para controlar si se debe eliminar el par de validos
            
            for idx in range(len(self.validos[0])):
                peso = self.validos[0][idx]
                sezgo = self.validos[1][idx]
                if round((c * peso) + sezgo, presicion) != f:
                    remover = True  # Se encontró un par inválido, se puede eliminar
                    index = idx
                
            if remover:
                print(f"Movido a invalidos: Celcius: {c}, Faren: {f}")
                self.invalidos[0].append(self.validos[0].pop(index))
                self.invalidos[1].append(self.validos[1].pop(index))
            else:
                # Si no se encontró ningún par válido o no se debe remover
                print(f"¡Par válido para Celcius: {c}, Faren: {f}! con peso {peso} y sezgo {sezgo}")
            
            i += 1
            print(f"Celcius: {c}, Faren: {f}, Resultado: {'igual' if not remover else 'invalido'}")

        self.imprimir_validos()
        self.guardar_memoria()


    def unicos(self, iteraciones, presicion):
        ciclo = 0
        while ciclo < iteraciones:
            valorP = round(self.peso, presicion)
            valorS = round(random.uniform(self.lInf, self.lSup), presicion)
            
            # Verificar que no esté en invalidos
            if not self.pares_repetidos(valorP, valorS) and (valorP not in self.invalidos[0] or valorS not in self.invalidos[1]):
                break
            ciclo += 1
        if ciclo >= iteraciones:
            self.entrenado = True
            print(f"No se encontraron valores únicos luego de {iteraciones} intentos")
        self.pesos.append(valorP)
        self.sezgos.append(valorS)
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
prueba.menu_principal()
