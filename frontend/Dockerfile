FROM node:18

WORKDIR /app

# Copy package files first for caching
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy everything else
COPY . .

# Set environment variables
ENV NODE_ENV=false
ENV PORT=3000

# Expose port for Vite
EXPOSE 3000

# Start Vite Dev Server
CMD ["npm", "run", "dev"]
