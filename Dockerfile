# ANTI-PATTERN: Using latest tag rather than a specific version
FROM python:latest

# ANTI-PATTERN: Running as root user
# (No USER directive to set a non-root user)

# ANTI-PATTERN: Not properly handling layers for caching
COPY . /app
WORKDIR /app

# ANTI-PATTERN: Installing unnecessary development dependencies
# ANTI-PATTERN: Not using a requirements freeze for deterministic builds
RUN pip install --no-cache-dir -r requirements.txt

# ANTI-PATTERN: No health checks defined
# ANTI-PATTERN: Exposing a non-standard port with no documentation
EXPOSE 5000

# ANTI-PATTERN: Using CMD instead of ENTRYPOINT for the main process
# ANTI-PATTERN: Running the development server in production
CMD ["python", "app.py"] 