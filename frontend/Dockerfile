FROM node:18

WORKDIR /app

# Accept build-time variable
ARG NODE_ENV
ENV NODE_ENV=${NODE_ENV}

# Install deps
COPY package.json package-lock.json ./
RUN npm install

# Copy rest of app
COPY . .

EXPOSE 3000
CMD ["npm", "run", "dev"]
