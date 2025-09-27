FROM postgres:16

ENV POSTGRES_DB=medy_supply_db
ENV POSTGRES_USER=medy_supply_app
ENV POSTGRES_PASSWORD=medySupply123

COPY init.sql /docker-entrypoint-initdb.d/
