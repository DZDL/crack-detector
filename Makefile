

build:
	docker build -t crack .

run:
	docker run --rm -it -p 8501:8501 crack

build-run: build run