FROM python:3.11.5-alpine

# Set working directory
WORKDIR /usr/src/app

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install necessary packages for building Go and other dependencies
RUN apk add --no-cache --virtual .build-deps \
    bash \
    gcc \
    musl-dev \
    wget \
    tar

# Install Go 1.21
RUN wget https://go.dev/dl/go1.21.0.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go1.21.0.linux-amd64.tar.gz && \
    rm go1.21.0.linux-amd64.tar.gz

# Set Go environment variables
ENV PATH="/usr/local/go/bin:${PATH}"
ENV GOPATH="/root/go"

# Install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# Install Katana
RUN go install github.com/projectdiscovery/katana/cmd/katana@latest

# Move Katana binary to a directory in PATH
RUN mv /root/go/bin/katana /usr/local/bin/katana

# Copy entrypoint script and make it executable
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# Copy application code
COPY . /usr/src/app/

# Entrypoint
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

# Cleanup build dependencies
RUN apk del .build-deps
