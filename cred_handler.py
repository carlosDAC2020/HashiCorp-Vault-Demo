import os
import time
import hvac
import subprocess


def update_env_variables():
    # Crear un cliente de Vault
    client = hvac.Client(url=os.getenv('VAULT_ADDR'), token=os.getenv('VAULT_TOKEN'))

    # Autenticar utilizando la clave de desbloqueo
    response = client.sys.submit_unseal_key(os.getenv('VAULT_KEY'))

    # Verificar si la autenticación fue exitosa
    if response['sealed']:
        print('Vault está sellado. No se pudo autenticar.')
    else:
        print('Vault está desbloqueado. Autenticación exitosa.')
        # Solicitar las credenciales al motor de secretos de la base de datos
        database_credentials = client.read('database/creds/app')['data']
        print(database_credentials)
        os.environ['DB_USER'] = database_credentials['username']
        os.environ['DB_PASSWORD'] = database_credentials['password']

def restart_django():
    global i
    if i==1:
        # Ejecutar migraciones
        subprocess.run(["python", "manage.py", "migrate"])
        # Crear superusuario
        subprocess.run(["python", "manage.py", "createsuperuser"])
    # Reiniciar el proceso de Django
    subprocess.Popen(["python", "manage.py", "runserver"])

# Actualizar las variables de entorno y reiniciar Django cada 5 minutos
i=1
while True:
    update_env_variables()
    restart_django()
    time.sleep(300)  # 5 minutos
    i+=1
