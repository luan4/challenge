## Index
1. Installing dependencies.
2. Build docker containing the database.
3. Launching the Flask app.
4. Launching main function and checking results.
5. Configuration options.

### The answer to the excersise can be found on challenge/teo/excersise.txt

### 1. Installing dependencies

* Python >= 3.7 is required.
* docker
* libpq-dev (required to install psycopg2)
* docker-compose (optional)
	

The following python packages, which can be installed via pip are required:

* aiohttp
* sqlalchemy
* flask
* flask\_sqlalchemy
* psycopg2

### 2. Build docker containing the database
To build the container, after cloning the repository run
```sh
$ cd ./challenge/
$ docker-compose up --build -d
```
This uses the **docker-compose.yml** configuration file to set the container's parameters.
In case you do not want to install docker-compose, you could just run:
```
$ docker volume create --name db_volume
$ docker run -d --name postgres -p 5432:5432 \
	   --env-file database.conf \
	   -v db_volume:/var/lib/postgresql postgres:latest
```
### 3. Launching the Flask app
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

### 4. Launching main function and checking results

If you access
```
http://localhost:5000
```
on your browser, you should see links to the three endpoints the Flask app provides:

The main function (get item info from APIs and upload it to the containerized database) is mapped to the _/gather_and_upload_ endpoint.
```
http://localhost:5000/gather_and_upload
```

You can check the database now holds the information by accessing 

```
http://localhost:5000/print_table
```

which returns everything on the table.
The information on the database is configured to persist even when the container is stopped and restarted. If you want to empty the table, you can access
```
http://localhost:5000/delete_all
```
### 5. Configuration options

#### Read and parse options
To specify read options such as which file to read from and its formatting, edit the file
```
challenge/configs/read_config.json
```
the file you want to read from must be stored in:
```
challenge/data/
```

The file
```
challenge/configs/parse_config.json
```
contains two options: _chunk\_size_ and _secure\_mode_. 

_chunk\_size_ specifies the amount of items from the file to be held in memory at the same time.
Keep in mind that the main bottleneck in the program's speed is fetching lines from the file stored in the hard drive, so setting the chunk size to a low value will result in poor performance. The bigger the chunk size your memory can handle, the faster the program will run.

If _secure\_mode_ is set to false, the changes to the database will be commited only once, after all lines have been added. This is much faster than commiting every line but if the function fails for any reason, nothing will be held in the database.
If _secure\_mode_ is set to true, the program will commit after adding every line to the database. 

#### Docker config
The file
```
challenge/docker-compose.yml
```
Contains the configuration options to run the container. The line
```
volumes: - db_volume:/var/lib/postgresql
```
tells docker to mount a volume at the specified location so that data persists even when the container is killed.
```
env_file: database.conf
```
tells the container to set its environment variables to match the ones specified in database.conf. These will be needed to connect to the database using the Flask app, as well with the ports, specified in:
```
ports:
  - 5432:5432
```
