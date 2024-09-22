echo "limpado os containers ativos e suas imagens do docker..." 

# Inicia os containers
docker compose up -d

# Salva os container ativos
containers=$(docker ps -q)

# Finaliza os containers
docker kill $containers

# Limpa as imagens dos containers que estavam ativos 
docker image rm --force $(sed 's/^sha256://' <<< $(docker inspect --format="{{.Image}}" $containers))

# Remove os containers ativos
docker rm --force --volumes $containers

# Remove os volumes especificos 
docker volume rm calendar-api_local_postgres_data calendar-api_local_postgres_data_backups
#docker compose up