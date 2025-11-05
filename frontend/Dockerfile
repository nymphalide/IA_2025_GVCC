FROM node:18-alpine

WORKDIR /app

# Copiem package.json pentru a instala dependențele
COPY package.json ./
RUN npm install

# Copiem restul codului sursă
# Inclusiv noul folder 'public'
COPY . .

# Expunem portul 3000 (standard pentru React)
EXPOSE 3000

# Comanda de pornire pentru dezvoltare
CMD ["npm", "start"]