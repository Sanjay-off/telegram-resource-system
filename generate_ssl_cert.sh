#!/bin/bash

echo "Generating self-signed SSL certificate..."

# Create SSL directory
mkdir -p ssl

# Generate private key and certificate
MSYS_NO_PATHCONV=1 openssl req -x509 -newkey rsa:4096 -nodes \
  -keyout ssl/key.pem \
  -out ssl/cert.pem \
  -days 365 \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

echo "✅ SSL certificate generated in ssl/ directory"
echo "   - Certificate: ssl/cert.pem"
echo "   - Private Key: ssl/key.pem"