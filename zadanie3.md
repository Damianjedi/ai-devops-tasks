Przykładowy Dockerfile dla aplikacji Node.js (obraz Alpine, instalacja zależności przed kopiowaniem kodu, proces bez uprawnień roota):


FROM node:22-alpine
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --omit=dev
COPY . .
USER node
EXPOSE 3000
CMD ["node", "index.js"]
Jeśli aplikacja ma etap budowania (TypeScript, frontend), użyj dwóch etapów:


FROM node:22-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build
FROM node:22-alpine
WORKDIR /app
ENV NODE_ENV=production
COPY package.json package-lock.json ./
RUN npm ci --omit=dev
COPY --from=build /app/dist ./dist
USER node
EXPOSE 3000
CMD ["node", "dist/index.js"]
Budowanie i uruchomienie:


docker build -t moja-app .
docker run --rm -p 3000:3000 moja-app








FROM node:18

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .

EXPOSE 3000
CMD ["npm", "start"]

WORKDIR /app ustawia katalog roboczy, żeby pliki i npm install nie lądowały w katalogu głównym obrazu