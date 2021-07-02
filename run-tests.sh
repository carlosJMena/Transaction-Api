docker build -f Dockerfile . -t belvo-api:latest
docker stop belvo_app
docker rm belvo_app
docker run -d -p 8080:8000 --name belvo_app belvo-api:latest
docker exec -it belvo_app python manage.py test
docker stop belvo_app
docker rm belvo_app
