FROM postgres:15-bullseye

COPY ./compose/production/postgres/create-multiple-postgresql-databases.sh /docker-entrypoint-initdb.d/
RUN sed -i 's/\r$//g' /docker-entrypoint-initdb.d/create-multiple-postgresql-databases.sh
