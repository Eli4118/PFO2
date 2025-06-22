import requests
import getpass

BASE = 'http://127.0.0.1:5000'
usuario = input('Usuario: ')
contraseña = getpass.getpass('Contraseña: ')

def register():
    r = requests.post(f'{BASE}/registro', json={'usuario': usuario, 'contraseña': contraseña})
    print(r.json())

def login():
    r = requests.post(f'{BASE}/login', auth=(usuario, contraseña))
    print(r.json())

# Menú de operaciones
def menu():
    print('\nOpciones:')
    print('1. Crear tarea')
    print('2. Listar tareas')
    print('3. Actualizar tarea')
    print('4. Eliminar tarea')
    print('0. Salir')
    return input('Elige opción: ')

if __name__ == '__main__':
    register()
    login()
    while True:
        opc = menu()
        if opc == '1':
            desc = input('Descripción: ')
            r = requests.post(f'{BASE}/tareas', json={'descripcion': desc}, auth=(usuario, contraseña))
            print(r.json())
        elif opc == '2':
            r = requests.get(f'{BASE}/tareas/list', auth=(usuario, contraseña))
            print(r.json())
        elif opc == '3':
            tid = input('ID tarea: ')
            desc = input('Nueva descripción: ')
            comp = input('Completada (True/False): ')
            r = requests.put(f'{BASE}/tareas/{tid}', json={'descripcion': desc, 'completada': comp=='True'}, auth=(usuario, contraseña))
            print(r.json())
        elif opc == '4':
            tid = input('ID tarea: ')
            r = requests.delete(f'{BASE}/tareas/{tid}', auth=(usuario, contraseña))
            print(r.json())
        else:
            break