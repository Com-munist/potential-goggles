# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .
#COPY constraints.txt .  # Copy constraints file if you created one

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of your application code
COPY . .

# Command to run your bot
CMD ["python", "bot.py"]  # Replace with your main file if different
