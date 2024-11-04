#!/bin/bash
docker build -t my-streamlit-app .
docker tag my-streamlit-app:latest wlong27/my-streamlit-app:latest
docker push wlong27/my-streamlit-app:latest