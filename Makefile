SHELL := /bin/bash
.DEFAULT_GOAL := build

.EXPORT_ALL_VARIABLES:
RUNTIME_LOG ?= runtime.log
MAX_CONTENT_LENGTH ?= 2

serve:
	python server.py

lint:
	pylama server.py src

setup:
	python -m pip install -r requirements.txt

test:
	python -m unittest discover src/tests -v

deploy:
	docker build -t {your-dockerhub-username}/charging-process-rating .
	docker run -p 5000:5000 -d {your-dockerhub-username}/charging-process-rating
