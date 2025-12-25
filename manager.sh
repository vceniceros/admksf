#!/bin/bash

# --- CONFIGURACION ---

DB_SERVICE="db"
DB_USER="admin"
DB_NAME="admksf"
WEB_SERVICE="web"

# --- COLORES Y FORMATO ---
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

�
pause(){
  echo -e "\n${YELLOW}Presiona [Enter] para continuar...${NC}"
  read -r
}

# Loop del menu�principal
while true
do
    clear
    echo -e "${CYAN}=============================================${NC}"
    echo -e "${CYAN}   MANAGER: Django + Angular + Postgres      ${NC}"
    echo -e "${CYAN}=============================================${NC}"
    echo -e "${GREEN}1)${NC} Iniciar todo (Ver logs)"
    echo -e "${GREEN}2)${NC} Iniciar todo en segundo plano (Daemon)"
    echo -e "${GREEN}3)${NC} Detener todo (Down)"
    echo -e "${GREEN}4)${NC} Reconstruir y levantar (Cambios en Dockerfile/Libs)"
    echo -e "${GREEN}5)${NC} Entrar a la Base de Datos (SQL Shell)"
    echo -e "${GREEN}6)${NC} Entrar al contenedor Web (Bash)"
    echo -e "${GREEN}7)${NC} Ejecutar Migraciones (Makemigrations + Migrate)"
    echo -e "${RED}0)${NC} Salir"
    echo -e "${CYAN}=============================================${NC}"
    
    read -p "Selecciona una opción: " option

    case $option in
        1)
            echo -e "\n${GREEN}🚀 Iniciando contenedores...${NC}"
            docker-compose up
            pause
            ;;
        2)
            echo -e "\n${GREEN}🚀 Iniciando en background...${NC}"
            docker-compose up -d
            echo "Listo. Usa 'docker-compose logs -f' si quieres ver logs."
            pause
            ;;
        3)
            echo -e "\n${RED}🛑 Deteniendo servicios...${NC}"
            docker-compose down
            pause
            ;;
        4)
            echo -e "\n${YELLOW}♻️  Reconstruyendo imagenes y reiniciando...${NC}"
            docker-compose up --build
            pause
            ;;
        5)
            echo -e "\n${CYAN}🐘 Conectando a Postgres... (Escribe '\q' para salir)${NC}"
            docker-compose exec $DB_SERVICE psql -U $DB_USER -d $DB_NAME
            pause
            ;;
        6)
            echo -e "\n${CYAN}💻 Abriendo terminal en Django...${NC}"
            docker-compose exec $WEB_SERVICE /bin/bash
            ;;
        7)
            echo -e "\n${YELLOW}🔄 Ejecutando migraciones...${NC}"
            docker-compose exec $WEB_SERVICE python manage.py makemigrations
            docker-compose exec $WEB_SERVICE python manage.py migrate
            echo -e "${GREEN}✅ Migraciones completadas.${NC}"
            pause
            ;;
        0)
            echo -e "\n¡Hasta luego! 👋"
            exit 0
            ;;
        *)
            echo -e "\n${RED}Opcion no valida.${NC}"
            sleep 1
            ;;
    esac
done
