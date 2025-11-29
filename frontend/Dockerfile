# Use Node.js image
FROM node:22

# Set working directory
WORKDIR /app

# Copy package files first for better layer caching
COPY package.json package-lock.json* ./

# Install dependencies (use ci for faster, reproducible installs)
RUN npm ci --only=production=false

# Copy source code
COPY . .

# Expose port
EXPOSE 3000

# Start app
CMD ["npm", "start"]
