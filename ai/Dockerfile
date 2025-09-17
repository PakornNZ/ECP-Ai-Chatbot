FROM ollama/ollama:latest

WORKDIR /app

COPY ai/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

EXPOSE 11434
ENTRYPOINT ["/usr/bin/bash", "/entrypoint.sh"]

