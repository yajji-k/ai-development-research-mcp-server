# Use the official Python 3.13 image as the base image
FROM python:3.13-slim-trixie

# Set the working directory inside the container
WORKDIR /app

# Copy the entire project into the container
COPY . .

# Install uv
RUN pip install uv

# Install project dependencies
RUN uv sync

# Start the MCP server
CMD ["uv", "run", "python", "-m", "app.server.bootstrap"]