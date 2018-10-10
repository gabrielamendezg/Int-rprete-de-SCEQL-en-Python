"""
Algoritmos y Programación 1
TP3: SCEQL
Integrantes: 
1.  Nombre: Diego Pereyra
    Padrón: 102072 (cbc09)
2.  Nombre: Gabriela Méndez
    Padrón: 101741
Catedra:
Practica: Barbara
"""
from clases import * 
import argparse

def main():
#Función principal del programa, intérprete de SCEQL en Python. Permite ejecutar un programa 
#cualquiera recibiendo por parámetro de línea de comandos el nombre del archivo que contiene 
#el código SCEQL. Además permite ejecutar el programa en modo debug con el parámetro -d.

	parser = argparse.ArgumentParser(description='Interprete de codigo SCEQL')
	parser.add_argument('archivo', metavar='archivo', help='archivo con codigo a interpretar')
	parser.add_argument('-d', '--debug', action='store_true', help='modo debug')
	args = parser.parse_args()

	nombre_archivo = args.archivo
	modo_debug = args.debug

	print('The File name is {}'.format(args.archivo))
	codigo = Sceql(modo_debug)
	print('Procesando....\n')
	try: 
	# Intenta adjuntar el código a un Sceql y ejecutarlo
		codigo.insertar_codigo(nombre_archivo)
		codigo.ejecutar()
	except SyntaxError as error: 
	# captura error de syntaxis en el código. 
		print('Syntax Error: ',error)
	except KeyboardInterrupt:  
	# captura excepción de interrupción. 
		print('\nSe ha pulsado ctrl+c')
	except OSError: 
	# captura un error con el archivo.
		print('Problema al abrir el archivo.')

main()