# CloudBot

CloudBot - AI Champion Bootcamp submission.

## Run it locally

```bash
virtualenv .venv
source .venv/bin/activate

pip install pip-tools
pip-compile requirements.in
pip install -r requirements.txt

streamlit run CloudBot.py
```

## Build Tag and Push Image

```bash
docker build -t my-streamlit-app .
docker tag my-streamlit-app:latest <username>/my-streamlit-app:latest
docker push <username>/my-streamlit-app:latest
```
