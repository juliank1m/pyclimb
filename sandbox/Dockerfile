# PyClimb Sandbox Container
# Minimal Python image for executing untrusted code

FROM python:3.11-slim-bookworm

# Create non-root user for running code
RUN useradd --create-home --shell /bin/false runner

# Remove potentially dangerous tools
RUN apt-get update && \
    apt-get remove -y --purge wget curl && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /sandbox

# Switch to non-root user
USER runner

# Default command (will be overridden)
CMD ["python3", "--version"]
