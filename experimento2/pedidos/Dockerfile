FROM postgres:16

ENV POSTGRES_DB=medy_supply
ENV POSTGRES_USER=medy_supply_app
ENV POSTGRES_PASSWORD=postgres

COPY init.sql /docker-entrypoint-initdb.d/
