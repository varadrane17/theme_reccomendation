# Theme Reccomendation

## Setup

```bash
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker   #CAREFUL: This will restart docker and all running containers.
docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
ollama pull llama3.2
pip install -r Requirements.txt
uvicorn server:app --reload --port 8000
```