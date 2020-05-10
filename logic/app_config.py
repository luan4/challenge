# Parameters to enable Flask app to connect to the containerized database.
# These values must match the ones defined in database.conf

import os

user = "test"
password = "password"
host = "localhost"
database = "example"
port = "5432"

DATABASE_CONNECTION_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
