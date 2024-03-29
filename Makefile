include .env

PYTHONPATH := $(shell pwd):${PYTHONPATH}

migrate:
	PYTHONPATH=$(shell pwd):${PYTHONPATH} alembic upgrade head

migration:
	PYTHONPATH=$(shell pwd):${PYTHONPATH} alembic revision --autogenerate -m "${message}"

setup:
	PYTHONPATH=$(shell pwd):${PYTHONPATH} pip install -r requirements.txt