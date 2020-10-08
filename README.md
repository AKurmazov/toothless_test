# Toothless Test
This project is a test assignment given by *Toothless Consulting Inc.*


### Running Locally
Rename `.env.example` to `.env` and fulfill the variables with the following values:

```
SECRET_KEY=di_v5)6%5^hym0)c5s$!5*v)=kb_$=89u&-r6j6ry1g96h1l4n
RUNSERVER_PORT=8000
DB_NAME=postgres
DB_USER=postgres
DB_PORT=5432
DB_PASSWORD=postgres
STRIPE_SECRET_KEY=<your_secret_key>
STRIPE_PUBLIC_KEY=<your_private_key>
```
(I expose the environmental variables **intentionally**)

The project uses **Docker**, so initially you have to build and run the image using **docker-compose**
```
$ docker-compose up --build -d
```
This command will also run the migrations and set up the server at http://0.0.0.0:8000 (in case you set **RUNSERVER_PORT** to be 8000)

Next, you will have to create a superuser since there are no interfaces for creating Items outside the admin page
```
$ docker-compose run web python manage.py createsuperuser
``` 

Also, I wrote some unit tests, and it would be great to run them so that to make sure the app works as intended
```
$ docker-compose run web python manage.py test
```