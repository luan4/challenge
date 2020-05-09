Index
	1. Installing dependencies.
	2. Build docker containing the database.
	3. Launching the Flask app.
	4. Launching main function and checking results.
	5. Configuration options.

1. Installing dependencies.

	Python >= 3.7 is required.
	libpq-dev (required to install psycopg2)
	docker-compose (optional)
	

The following python packages, which can be installed via pip are required:

	aiohttp
	flask
	flask_sqlalchemy
	psycopg2
	

2. Build docker containing the database.

	To build the container, execute
		
		docker-compose up --build -d

inside the /challenge/flaskr/ directory. This uses the docker-compose.yml configuration file to set its parameters. 
	The "volumes: - db_volume:/var/lib/postgresql" mounts a volume at the specified location so that data persists even when the container is killed.
	"env_file: database.conf" tells the container to set its environment variables to match the ones specified in database.conf. These will be needed to connect to the database using the Flask app, as well with the ports, specified below.

	In case you do not want to install docker-compose, you could just run:

		docker volume create --name db_volume
		docker run -d --name postgres -p 5432:5432 \
			   --env-file docker/database.conf \
			   -v db_volume:/var/lib/postgresql postgres:latest


3. Launching the Flask app.
	
	To start the Flask app, run the following commands:
		
		export FLASK_APP=app.py
		flask run

you should get the following output:
	
		# Running on http://127.0.0.1:5000


4. Launching main function and checking results.

	The main function (get item info from APIs and upload it to the containerized database) is mapped to the '/upload_file' endpoint: sending the request

				https://127.0.0.1:5000/upload_file


with your browser with the flask app running should suffice. You can check the database now holds the information by accessing 


				https://127.0.0.1:5000/


which returns everything on the table.
	The information on the database is configured to persist even when the container is stopped and restarted. If you want to empty the table, you can access

				 
				https://127.0.0.1:5000/delete_all
