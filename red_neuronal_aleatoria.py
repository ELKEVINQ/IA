import random

#Por favor no eliminar cuando se reulilice este código

#Hola mi nombre es Kevin Zambrano, muchos me conocen como Lord_Of_Q, este codigo fue desarrollado a la par con otro archivo en el mismo
#repositorio, comenzó siendo yo tratando de entender cómo funciona la inteligencia artificial, y bueno, este entrenador de una red neuronal
#simple es a la respuesta a la que llegué, esta basado en la idea de un video de youtube de enseñar a una maquina a transformar numeros
#de celcius a decimales mediante la formula x = (n * peso) + sezgo, donde x es el fahrenheit, n es celcius y los pesos y sezgos son aleatorios.

#De hecho del video la unica informacion que tome, fue la formula de la transformacion, el resto lo hice por mi cuenta.

#El programa funciona mediante un sistema de iteraciones, el cual define cuantas veces va a ejecutarse el entrenamiento por cada elemento por
#cada item disponible en la lista de muestra, siendo siempre un par para ambos, luego una presicion que define el numero de decimales para el
#ruido con el cual va a funcionar el programa, teniendo mas ruido mientras más decimales, pero mas presicion como dicta el nombre y por último
#tenemos el paso, que va a ser el aumento o decremento segun el resultado obtenido, pudiendo variar mucho o muy poco para agilizar los procesos
#y guardandolos en una lista discriminatoria para no volver a seleccionar los resultados inutiles, esto agilita ejecuciones pequeñas,
#pero ralentiza un poco las grandes, aunque no es muy notable.

#Recomiendo probar haciendo un aumento desde 10 en el entrenador, para reiniciarlo, solo hay que borrar el txt de validos o su contenido.
#Mi entrenamiento mas optimizado, ha sido de 1000 iteraciones con presicion de 1 y paso de 0.2, luego de 2 intentos.
#Si el programa se ralentiza recomiendo borrar las lineas 154 y 167 o borrar los datos de validos_aleatorios.txt, control+c en consola para parar
#Gracias por revisar mi codigo, es libre de uso, asi que modifiquenlo a su gusto, pero si me pueden mencionar, lo agradecería.


class Red_neuronal_aleatoria:
    def __init__(self):
        #Se definen las variales necesarias para el funcionamiento, las primeras 4 sirven para el entrenamiento
        self.celcius = [7, 12, 21, 30, 32, 47, 58]
        self.faren = [44.6, 53.6, 69.8, 86, 89.6, 116.6, 136.4]
        self.pesos = []
        self.sezgos = []
        #Los set se utilizan para guardar datos y agilizar la comparacion con datos existentes en la lista de resultados y otros set
        self.validos = set()
        self.invalidos = set()
        #Booleanos encargados de definir limites, se declaran en el init para ser usados globalmente
        self.entrenado = False
        self.entrenador_activado = False
        #Los siguientes 7 son utilizados para guardar variables para el entrenamiento y transformacion
        self.iteraciones = 0
        self.presicion = 0
        self.paso = 0
        self.peso = 0
        self.sezgo = 0
        self.limSup = 1
        self.limPeso = 1
        self.file_path = "validos_aleatorios.txt"  # Archivo donde se guardarán los pares válidos
        #Metodo para cargar los datos disponibles de anteriores entrenamientos
        self.cargar_memoria()

    def menu_principal(self): #Menu principal del programa
        self.cargar_memoria()
        #bucle infinito detenido unicamente por los input y el break, manejar con cuidado, lo que hace lo lleva cada print
        while True:
            print("\nMenu principal:")
            print("1.- Entrenar")
            print("2.- Transformar de celcius a fahrenheit")
            print("3.- Salir")
            opcion = input("Seleccione una opcion (1/2/3): ")
            #Condicionales
            if opcion == "1":
                self.menu_entrenar()
            elif opcion == "2":
                self.menu_transformar()
            elif opcion == "3":
                print("Saliendo del programa.")
                break
            else:
                print("Opcion no disponible, escriba un numero entre 1, 2 o 3")

    def menu_entrenar(self): #Menu de entrenamiento
        #Si existen entrenamientos en la ejecucion actual y se desea encontrar más datos o no se encontraron datos en la primera, salta esto
        if self.entrenador_activado:
            #Bucle para entrenar
            while True:
                print("Desea utilizar los parametros de su ultimo entrenamiento")
                print("1. Si")
                print("2. No")
                reutilizar = input("Elija entre 1 y 2: ")
                if reutilizar == "1": #si decidimos reutilizar los datos del entrenamiento se ejecuta esto
                    self.entrenador(self.iteraciones, self.presicion, self.paso)
                    break
                elif reutilizar == "2": #si decidimos no utilizar se pregunta nuevamente
                    self.iteraciones = int(input("Ingrese el número de iteraciones para el entrenamiento: "))
                    self.presicion = int(input("Ingrese la precisión deseada para el entrenamiento: "))
                    self.paso = float(input("Ingrese el paso para el entrenamiento: "))
                    self.entrenador(self.iteraciones, self.presicion, self.paso)
                    break
                else:
                    print("Seleccion invalida, seleccione 1 o 2")
                    break
        else: #Si es la primera ejecucion en el programa actual se pregunta y ya
            self.iteraciones = int(input("Ingrese el número de iteraciones para el entrenamiento: "))
            self.presicion = int(input("Ingrese la precisión deseada para el entrenamiento: "))
            self.paso = float(input("Ingrese el paso para el entrenamiento: "))
            self.entrenador(self.iteraciones, self.presicion, self.paso)
            #Definimos que no es la primera ejecucion
            self.entrenador_activado = True

    def menu_transformar(self): #Metodo encargado de la transformacion.
        #Condicional
        if self.validos and len(self.validos) > 0:
            numero = float(input("Ingrese el número que desea transformar: "))
            self.transformar_numero(numero)
        else:
            print("No hay valores válidos disponibles para transformar el número, por favor entrenar")

    def transformar_numero(self, numero):
        #Implementar la logica de transformacion usando una logica de preguntar si hay validos disponibles
        validos = []
        if self.validos and (len(self.validos) > 0):
            #Cuando tenemos datos para usar, se transforma el set en una lista para poder leerlo y se procede con el calculo
            #La lista es de una sola dimencion. es decir a diferencia de resultados [x][y] se toma solo como resultados[x]
            #Funciona de esta manera porque en este caso solo hay un resultado correcto
            validos = list(self.validos)
            # Se realiza la operacion, que es el numero en celcius * peso + paso
            resuldato = (numero * validos[0][0]) + validos[0][1]
            print(f"{numero} en Celcius transformado a Fahrenheit es {resuldato}")
        else:
            #Cuando no hay datos disponibles, se imprime esto
            print("El transformador no tiene disponible ningun resultado para la transformacion, por favor entrenarlo")

    def entrenador(self, iteraciones, presicion, paso):
        # un bucle doble, para trabajar entre los pesos y los pasos
        for i in range(len(self.celcius)):
            for j in range(int(iteraciones) + 1):
                # Verificar que el valor no se salga del rango de items que tenemos disponibles
                self.operador(self.celcius[i], self.faren[i], presicion, paso, i)
            
        #En este metodo se verifican todos los resultados que dieron una respuesta para elegir uno que sirva con toda la muestra
        self.operar_todos(presicion)
        print("Entrenamiento terminado")

    #Metodo que se encarga de hacer operaciones durante el entrenamiento
    def operador(self, entrada, salida, presicion, paso, posicion):
        #Asignamos el resultado a nada para que se elija correctamente
        resultado = None
        #Metodo que busca pares unicos para asegurarnos de no revisar datos ya computados y el resultado que es una lista se asigna a una variable
        nodos = self.unicos(presicion)
        #Operacion de la misma manera que en el transformador, numero por peso, mas sezgo
        resultado = (entrada * nodos[0]) + nodos[1]
        #Dependiendo de la posicion en la recta al string se le asigna el valor para saber en que direccion actuar en el entrenador.
        if resultado < salida: # Si el resultado devuelto del operador es menor al esperado
            #Se preguntan 3 cosas con un elif para asegurarnos que solo tome una y se asigna un limite del numero que puede devover el aleatorio
            #Si la distancia en el plano es menor que, 100, 10 o 1 se suma al paso distintas cantidades
            if (self.faren[posicion] - resultado) >= 100: 
                self.limSup += paso * 100
            elif (self.faren[posicion] - resultado) >= 10:
                self.limSup += paso * 10
            elif (self.faren[posicion] - resultado) >= 1:
                self.limSup += paso
            #El limite para el aleatorio para el peso
            self.limPeso = self.limSup / 10
            #Discriminar los pares inutiles
            self.invalidos.add((nodos[0], nodos[1]))
        elif resultado > salida:# Si el resultado devuelto del operador es mayor al esperado se realiza lo mismo que arriba pero en resta
            if self.limSup > 0: #Primero vemos que el numero aleatorio no pueda tender a negativos
                if (resultado - self.faren[posicion]) >= 100:
                    self.limSup -= paso * 100
                elif (resultado - self.faren[posicion]) >= 10:
                    self.limSup -= paso * 10
                elif (resultado - self.faren[posicion]) >= 1:
                    self.limSup -= paso
                else: #Esto se encarga que si se vuelve negativo, regrese a positivo
                    self.limSup += 10
                self.limPeso = self.limSup / 10
            #Discriminar los pares inutiles
            self.invalidos.add((nodos[0], nodos[1]))
        else: #Cuando encuentra un igual lo envia a validos,
            self.validos.add((self.pesos[-1], self.sezgos[-1]))  # Agregar los últimos valores generados
            #Se imprime el resultado a consola
            print(f"Celcius {self.celcius[posicion]}, Faren {self.faren[posicion]}, ResultadoN {resultado}, peso {self.peso}, sezgo {self.sezgo}")
        return #Finaliza el metodo
    
    def operar_todos(self, presicion):#Metodo que verifica los resultados guardados en validos
        i = 0
        while i < len(self.celcius):#bucle para operar por todos los valores disponibles en las muestras
            c = self.celcius[i]
            f = self.faren[i]
            remover = False
            #Se pregunta si tenemos valores validos
            if self.validos:
                for peso, sezgo in self.validos:#bucle por cada peso y sezgo disponible en validos
                    if round((c * peso) + sezgo, presicion) != f:#Se realiza la operacion de numero * peso + sezgo y se pregunta si no es igual al fahrenheit
                        #cuando no es igual se marca para no imprimir
                        remover = True
                        #Se añade a la lista de invalidos y se reserva
                        self.invalidos.add((peso, sezgo))
                        #continua la ejecucion del programa para comprar el resto de datos
                        continue
                    if not remover:
                        #Cuando es un valor o no marcado valido se imprime
                        print(f"¡Par válido para Celcius: {c}, Faren: {f}! con peso {peso} y sezgo {sezgo}")
                
            
            else:
                # Si no hay pares válidos, no hay nada que hacer
                break
            
            i += 1  # Aumentar i solo al terminar de revisar todos los pares válidos
        # Comparar y eliminar pares duplicados entre validos e invalidos
        self.validos.difference_update(self.invalidos)
        
        #Se imprimen los resultados utiles
        self.imprimir_validos()
        #Se guarda la memoria
        self.guardar_memoria()

    def unicos(self, presicion):
        #Bucle para buscar valores ya guardados
        while True:
            #Se asignan aleatorios para peso y sezgo desde 0 a su limite asignado
            valorP = round(random.uniform(0, self.limPeso), presicion)
            valorS = round(random.uniform(0, self.limSup), presicion)
            #se añade como un set para mejor ejecucion
            par = (valorP, valorS)
            #Condicion para buscar el set dentro de los sets validos e invalidos
            if par not in self.validos and par not in self.invalidos:
                #Si no estan dentro de los sets se agregan a las listas de pesos, sezgos y a los valores actuales
                self.pesos.append(valorP)
                self.sezgos.append(valorS)
                self.peso = valorP
                self.sezgo = valorS
                #Se regresan los valores que lo usamos cuando llamamos a nodo arriba, pero es una lista
                return [valorP, valorS]

    def imprimir_validos(self):#Metodo para imprimir los valores que estan dentro de la lista de validos al final
        print("Valores en validos:")
        for peso, sezgo in self.validos:
            print(f"Peso: {peso}, Sezgo: {sezgo}")#imprime cada valor encontrado dentro del bucle

    def guardar_memoria(self):#Metodo para guardar datos de memoria a un archivo
        with open(self.file_path, "w") as file:#Abre el archivo con el nombre asignado en la ruta asignada
            for peso, sezgo in self.validos:
                file.write(f"{peso},{sezgo}\n")#En el bucle escribe el peso y sezgo de validos
            for peso, sezgo in self.invalidos:
                file.write(f"INVALIDO,{peso},{sezgo}\n")#En el bucle escribe el peso y sezgo de invalidos marcado con etiqueta para diferenciar
    
    def cargar_memoria(self):#Metodo para recuperar los datos del archivo
        try:#Manejado con un try para evitar errores
            with open(self.file_path, "r") as file:#Trata de abrir el archivo en la ruta
                for line in file:
                    if line.startswith("INVALIDO"):#Separa los valores por la etiqueta de invalido en el bucle y lo asigna a los set correspondientes
                        _, peso, sezgo = line.strip().split(",")
                        self.invalidos.add((float(peso), float(sezgo)))
                    else:#Separa los valores sin etiqueta en el bucle y lo asigna a los set correspondientes
                        peso, sezgo = line.strip().split(",")
                        self.validos.add((float(peso), float(sezgo)))
        except FileNotFoundError:#Exepcion que muestra un error controlado cuando no encuentra el archivo
            print(f"Archivo {self.file_path} no encontrado. No se cargaron valores.")

#Para la ejecucion del programa se declara la lase
red = Red_neuronal_aleatoria()
# Entrenar Codigo para un entrenamiento directo. descomentar para una ejecucion directa
#prueba.entrenador(100000, 1, 0.2)
#Comienza la ejecucion con una interfaz simple e impresa en consola
red.menu_principal()
#Para comenzar la ejecucion en la consola de comandos colocar "python .\red_neuronal_aleatoria.py" dentro de la carpeta del archivo
#No colocar con comillas por dios.