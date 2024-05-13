
# asignamos la variable de entono del puerto del vault server 
export VAULT_ADDR='http://127.0.0.1:8200'

# inciamos secion en el server de vault 
vault login

vault secrets enable database

# configuracion para la conexcion con la base de datos p
vault write database/config/app \
   plugin_name=postgresql-database-plugin \
   allowed_roles="app" \
   connection_url="postgresql://{{username}}:{{password}}@localhost:5432/?sslmode=disable" \
   username="postgres" \
   password="postgres"

# configuracion para la creacion de roles dinamicos 
vault write database/roles/app \
    db_name=app \
    creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; ALTER ROLE \"{{name}}\" WITH SUPERUSER; GRANT CREATE, USAGE ON SCHEMA public TO \"{{name}}\";" \
    default_ttl="10m" \
    max_ttl="10m"


