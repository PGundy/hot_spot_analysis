# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.9-slim

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt


## Demonstrate the environment is activated:
RUN echo "Make sure seaborn is installed:"
RUN python -c "import seaborn"

COPY . /src

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "from src import main"]
