default:
    @just --list

# Simple example recipe
show-all-files:
    ls -latr


docker-build:
    docker build -t iris-streamlit-app .

docker-run:
    lsof -i :8501 | grep LISTEN | awk '{print $2}' | xargs -r kill
    docker run -p 8501:8501 iris-streamlit-app
