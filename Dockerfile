
# Use Miniconda3 base image with Python 3.11
FROM continuumio/miniconda3:latest

# Set the working directory in the container
WORKDIR /app


# Copy the environment.yml file into the container
COPY environment.yml .

# Create the conda environment
RUN conda env create -f environment.yml

# Make sure conda environment is activated by default
SHELL ["conda", "run", "-n", "venv", "/bin/bash", "-c"]


# Copy the rest of the application code into the container
COPY . .


# Expose the port that the application will run on
EXPOSE 8000


# Command to run the application using the conda environment
CMD ["conda", "run", "--no-capture-output", "-n", "venv", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]