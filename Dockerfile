# Use an official Rasa image
FROM rasa/rasa:3.0.0-full

# Switch to root user to install dependencies
USER root

# Create the app directory
RUN mkdir -p /app

# Set the working directory to /app
WORKDIR /app

# Copy the project files into the container
COPY . /app

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install Python dependencies
RUN pip install -r requirements.txt

# Download and link the spaCy model
RUN python -m spacy download en_core_web_md && \
    python -m spacy link en_core_web_md en

# Expose the port Rasa will run on
EXPOSE 5005

# Train the Rasa model
RUN rasa train --config /app/config.yml --domain /app/domain.yml --data /app/data

# Run Rasa server
CMD ["rasa", "run", "--enable-api", "--cors", "*"]