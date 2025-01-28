# Use Node.js image
FROM node:22

# Set working directory
WORKDIR /app

# Install dependencies
COPY package.json .
RUN npm install

# Copy source
COPY . .

# Start app
CMD ["npm", "start"]
