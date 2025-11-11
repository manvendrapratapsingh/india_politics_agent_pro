# Multi-stage build for India Politics Agent Pro

# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    make \
    libxml2-dev \
    libxslt-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements-new.txt .
RUN pip install --user --no-cache-dir -r requirements-new.txt

# Stage 2: Runtime
FROM python:3.11-slim

# Create non-root user
RUN useradd -m -u 1000 agent && \
    mkdir -p /app /app/outputs /app/.cache && \
    chown -R agent:agent /app

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libxml2 \
    libxslt1.1 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /root/.local /home/agent/.local

# Copy application code
COPY --chown=agent:agent src/ /app/src/
COPY --chown=agent:agent agent.yaml /app/
COPY --chown=agent:agent setup.py /app/

# Switch to non-root user
USER agent

# Add local bin to PATH
ENV PATH=/home/agent/.local/bin:$PATH
ENV PYTHONPATH=/app/src:$PYTHONPATH

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Default command
ENTRYPOINT ["python", "-m", "india_politics_agent.cli.main"]
CMD ["--help"]
