#!/bin/sh

# Replaced by default postgis docker image setup which create default user, db from .env values
#psql -U $POSTGRES_USER -c "CREATE USER $POSTGRES_USER PASSWORD '$POSTGRES_PASSWORD'"

# Used for our application tests
psql -U $POSTGRES_USER -c "CREATE DATABASE $POSTGRES_TEST_DB OWNER $POSTGRES_USER"
psql -U $POSTGRES_USER -c "GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_TEST_DB TO $POSTGRES_USER"
psql -d $POSTGRES_TEST_DB -U $POSTGRES_USER -c "CREATE EXTENSION IF NOT EXISTS postgis"
