default:
    @just --list

# Simple example recipe
show-all-files:
    ls -latr


app:
    streamlit run app/main.py

docker-build:
    docker build -t iris-streamlit-app .

docker-run:
    lsof -i :8501 | grep LISTEN | awk '{print $2}' | xargs -r kill
    docker run -p 8501:8501 iris-streamlit-app

reqs:
    uv export --format requirements-txt > requirements.txt