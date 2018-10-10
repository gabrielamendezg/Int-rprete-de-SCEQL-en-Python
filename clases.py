import os 
OPERADORES_VALIDOS=('!','=','-','_','/','\\','*')

#+============================  FUNCIONES AUXILIARES
def obtener_prox(posicion,cadena):
#Recibe la posición del origen '\', devuelve la posición del '/' correspondiente
    while True:
        posicion+=1 
        if cadena[posicion] == '/':
            return posicion
        elif cadena[posicion] == '\\':
            posicion=obtener_prox(posicion,cadena)

def ejecutar_comando(cola,comando,debug):
#Ejecuta los comandos más básicos "!", "=", "-", "_" y "*"
#Recibe una cola no vacía de números enteros, un comando en cadena
#y el modo debug (booleano). Para el comando "*" devuelve una cadena
#con el byte al frente de la cola interpretado como un ASCII.
#Devuelve una cadena vacía para el resto de comandos.
    salida = ''
    if comando == "!":
    	#Encolar un cero
        cola.encolar(0)
    elif comando == "-":
        #decrementar el byte que está al frente de la cola.
        cola.decrementar_prim()

    elif comando == "_":
        #Incrementar el byte que está al frente de la cola
        cola.incrementar_prim()

    elif comando == "=":
        #Desencolar un byte y encolarlo.
        byte = cola.desencolar()
        cola.encolar(byte)

    elif comando == "*":
        #desencolar el byte al frente y luego vuelve a encolarlo.
        byte = cola.desencolar()
        valor= chr(byte)
        salida += valor
        if not debug:
        	print(valor, end='', flush=True)
        cola.encolar(byte)
    return salida

#+============================  CLASES

### NODO ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class _Nodo:
	def __init__(self, dato=None, prox=None):
	#Constructor de la clase Nodo
		self.dato = dato
		self.prox = prox
	def __str__(self):
	#Representación en cadena de texto
	
		return str(self.dato)

### COLA ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Cola:
#Cola implementada por lista enlazada.
	def __init__(self):
	#Crea una cola vacía.
		self.primero = None
		self.ultimo = None
		self.len = 0

	def __len__(self):
	#Devuelve el número de elementos de la cola
		
		return self.len

	def __str__(self):
	#Devuelve una representación en cadena de la cola.
		actual=self.primero
		res=[]
		while actual:
			res.append(actual.dato)
			actual=actual.prox
		return str(res)

	def encolar(self, x):
	#Agrega el elemento x al final de la cola.
		nuevo = _Nodo(x)
		if self.ultimo is not None:
			self.ultimo.prox = nuevo
			self.ultimo = nuevo
		else:
			self.primero = nuevo
			self.ultimo = nuevo
		self.len += 1

	def desencolar(self):
	#Desencola el primer elemento y lo devuelve.
	#Devuelve un error si la cola está vacía.
		if self.primero is None:
			raise ValueError("La cola está vacía")
		valor = self.primero.dato
		self.primero = self.primero.prox
		if not self.primero:
			self.ultimo = None
		self.len -= 1
		return valor

	def esta_vacia(self):
	#Devuelve True si la cola está vacía, False en caso contrario.
		
		return self.primero is None

	def ver_primero(self):
	#Devuelve el valor del primer elemento de la cola (No modifica la cola)
	
		if self.esta_vacia():
			raise ValueError("La cola está vacía")
		#valor = self.primero.dato
		return self.primero.dato
		
	def incrementar_prim(self):
	#Precondición: Cola de números enteros.
	#Incrementa en 1 el primer elemento de la cola.

		if self.esta_vacia():
			raise ValueError("La cola está vacía")
		self.primero.dato += 1
		if self.primero.dato > 255: 
			self.primero.dato = 0
	
	def decrementar_prim(self):
	#Precondición: Cola de números enteros.
	#Decrementa en 1 el primer elemento de la cola. 
		if self.esta_vacia():
			raise ValueError("La cola está vacía")
		self.primero.dato -= 1
		if self.primero.dato < 0:
			self.primero.dato = 255

### PILA ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Pila:
#Pila implementada por listas. 
	def __init__(self):
	#Constructor de la Pila. 

		self.items = []

	def esta_vacia(self):
	#Devuelve True si la pila está vacía, False en caso contrario.
		
		return len(self.items) == 0

	def apilar(self,dato):
	#Apila el elemento "dato" al final de la pila. 
		
		self.items.append(dato)

	def desapilar(self):
	#Desapila el último elemento de la pila y lo devuelve.
	#Devuelve un error si la pila está vacía.

		if self.esta_vacia():
			raise IndexError("La pila está vacía")
		return self.items.pop()

### SCEQL +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Sceql():
#Objeto Sceql para almacenar el código del archivo como una cadena.

	def __init__(self,modo):
	#Constructor de la clase Sceql, crea un Sceql vació con un modo (debug/sin debug)
	#inicializado a True o False según corresponda.
		self.codigo=''
		self.debug = modo

	def __str__(self):
	#Devuelve una representación en cadena del sceql.

		return (self.codigo)

	def ejecutar(self):
	#Ejecuta el código Sceql en el modo correspondiente. 

		cola_principal=Cola()
		cola_principal.encolar(0) 
		salida=''
		longitud_sceql=len(self.codigo)-1
		pila=Pila()
		#pila contiene los indices de las barras que inicializan los ciclos en el sceql
		i=0 #puntero.

		while i < longitud_sceql:

			salida = ejecutar_comando(cola_principal, self.codigo[i], self.debug)

			# \ abre  y / cierra
			if self.codigo[i] == "\\": 
				if cola_principal.ver_primero()!=0:
					pila.apilar(i)
					i+=1
				else:
					i=obtener_prox(i,self.codigo)+1
			elif self.codigo[i] =="/":
				if cola_principal.ver_primero()!= 0:
					i=pila.desapilar()
				else:
					pila.desapilar()
					i+=1		
			else:
				i+=1
				
			#	CON DEBUG -------------------------------
			if self.debug == True:
			
				os.system('clear')  #Limpia la pantalla
				print("Estado Cola : ",cola_principal)
				print("Salida      : ",salida)
				limite = i-65 #limite de caracteres a imprimir por pantalla del sceql
				if i == 0:
					print(self.codigo[0],end='')
					print("")
				if limite >= 0:
					print(self.codigo[limite:i],end='')
					#Resalta en color la posición actual
					print('\x1b[0;37;41m' + self.codigo[i] + '\x1b[0m')
				else:
					#Resalta en color la posicion actual.
					print(self.codigo[:i],end='')
					print('\x1b[0;37;41m' + self.codigo[i] + '\x1b[0m')
				input("")

	def insertar_codigo(self,archivo):
	#Agrega el código válido del archivo al objeto sceql
	#Devuelve error si existe algún problema al abrir el archivo.
	#O si hay un error de ciclos referente a las barras y contrabarras. 
		contador_barra=0 #\
		contador_contrabarra=0 #/
		with open(archivo) as file: 
			while True:
				#Mientras se este leyendo el archivo.
				linea=file.readline()
				if linea == '':
					break
				for caracter in linea:
					
					if caracter in OPERADORES_VALIDOS:
						self.codigo+=caracter

						if caracter == '\\':
							contador_barra+=1

						elif caracter == '/':
							contador_contrabarra+=1

						if contador_contrabarra > contador_barra:
							#Caso en el que aparezca un / sin un \ anterior.
							raise SyntaxError('Falta un operador "\\"')
							break
			if contador_barra != contador_contrabarra:
				#Caso en el que las barras y contrabarras sean inpares.
				raise SyntaxError('Operadores barras inpares')
			self.codigo+='  '
			#Espacios auxiliares para evitar error de índice en el caso donde
			#el último caracter es un "/"