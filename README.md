git config user.name "Vlad"
git config user.email "balesy@gmail.com"


docker network create MyNetwork

docker run --name booking_db -p 6432:5432 -e POSTGRES_USER=abcde -e POSTGRES_PASSWORD=abdsklfhaorfialvcde -e POSTGRES_DB=booking --network=MyNetwork --volume pg-booking-data:/var/lib/postgresql/data -d postgres:16

docker run --name booking_cache -p 7379:6379 --network=MyNetwork -d redis  

docker run --name booking_back -p 7777:8000 --network=MyNetwork booking_image

docker run --name booking_celery_worker --network=MyNetwork booking_image celery --app=src.tasks.celery_app:celery_instance worker -l INFO

docker run --name booking_celery_beat --network=MyNetwork booking_image celery --app=src.tasks.celery_app:celery_instance worker -l INFO -B

docker build -t booking_image .

# for running locally
docker run --name booking_nginx --volume .\nginx.conf:/etc/nginx/nginx.conf --network=MyNetwork --rm -p 80:80 nginx

# for running through the server 
docker run --name booking_nginx --volume ./nginx.conf:/etc/nginx/nginx.conf --network=MyNetwork --rm -p 80:80 nginx 