## Index
1. Installing dependencies.
2. Build docker containing the database.
3. Launching the Flask app.
4. Launching main function and checking results.
5. Configuration options.

#### 1. Installing dependencies

* Python >= 3.7 is required.
* docker
* libpq-dev (required to install psycopg2)
* docker-compose (optional)
	

The following python packages, which can be installed via pip are required:

* aiohttp
* flask
* flask_sqlalchemy
* psycopg2

#### 2. Build docker containing the database
To build the container, after cloning the repository run
```sh
$ cd ./challenge/
$ docker-compose up --build -d
```
This uses the **docker-compose.yml** configuration file to set the container's parameters. The option
```
volumes: - db_volume:/var/lib/postgresql
```
inside the config file mounts a volume at the specified location so that data persists even when the container is killed.
```
env_file: database.conf
```
tells the container to set its environment variables to match the ones specified in database.conf. These will be needed to connect to the database using the Flask app, as well with the ports, specified in:
```
ports:
  - 5432:5432
```
In case you do not want to install docker-compose, you could just run:
```
$ docker volume create --name db_volume
$ docker run -d --name postgres -p 5432:5432 \
	   --env-file database.conf \
	   -v db_volume:/var/lib/postgresql postgres:latest
```
#### 3. Launching the Flask app
To start the Flask app, run the following commands:
```
$ export FLASK_APP=app.py
$ flask run
```
you should get the following output:
```	
# Running on http://127.0.0.1:5000
```
If you encounter something like this:
```
Secure Connection Failed

An error occurred during a connection to 127.0.0.1:5000. SSL received a record that exceeded the maximum permissible length.

Error code: SSL_ERROR_RX_RECORD_TOO_LONG

    The page you are trying to view cannot be shown because the authenticity of the received data could not be verified.
    Please contact the website owners to inform them of this problem.
```
you are having issues regarding docker permissions. Follow instructions from the [docker official docs](https://docs.docker.com/engine/install/linux-postinstall/)

#### 4. Launching main function and checking results

The main function (get item info from APIs and upload it to the containerized database) is mapped to the _/upload_file_ endpoint.
Sending the request
```
http://localhost:5000/upload_file
```

with your browser (with the flask app running) should suffice. You can check the database now holds the information by accessing 

```
http://localhost:5000/
```

which returns everything on the table.
The information on the database is configured to persist even when the container is stopped and restarted. If you want to empty the table, you can access
```
http://localhost:5000/delete_all
```
#### 5. Configuration options

To specify read options such as which file to read from and its formatting, edit the file
```
challenge/configs/read_config.json
```
which has to be located in
```
challenge/data/
```

To specify the amount of items to be held in memory from the file at the same time, edit the file
```
challenge/configs/parse_config.json
```
Keep in mind that the main bottleneck in the program's speed is fetching lines from the file stored in the hard drive, so setting the chunk size to a low value will result in poor performance. The bigger the chunk size your memory can handle, the faster the program will run.


