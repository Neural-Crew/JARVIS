# Étape 1 : Build (Node)
FROM node:20-slim AS build

# Répertoire de travail
WORKDIR /app

# On copie d'abord les fichiers de dépendances pour profiter du cache
COPY frontend/package*.json ./
RUN npm install

# Copie du reste du code frontend
COPY frontend/ ./

# On définit l'URL du backend au moment du build (sinon utilise le défaut dans useChat.ts)
# Par défaut pour Docker Compose sur localhost, on laisse le client parler au port 8000 du localhost.
ARG VITE_API_BASE=""
ENV VITE_API_BASE=$VITE_API_BASE

# Build de l'application de production
RUN npm run build

# Étape 2 : Serve (Nginx)
FROM nginx:alpine

# Copie des fichiers buildés depuis l'étape 1
COPY --from=build /app/dist /usr/share/nginx/html

# Copie de la configuration Nginx (pour la gestion du routage React)
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Port 80 exposé par Nginx
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
