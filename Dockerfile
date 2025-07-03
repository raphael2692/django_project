# 1. Use a Python 3.12 base image to match your pyproject.toml
FROM python:3.12-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# 2. Install uv globally in the container
RUN pip install uv

# 3. Copy only the dependency file first to leverage Docker's layer cache
COPY pyproject.toml ./

# 4. Install dependencies using uv
# --system tells uv to install in the global site-packages
RUN uv pip install --system --no-cache .

# 5. Copy the rest of your application code
COPY . .