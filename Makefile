

build:
	docker build -t crack .

run:
	docker run --rm -it -p 8501:8501 crack

build-run: build run


release-google:
	gcloud builds submit --tag gcr.io/lofty-psyche-337800/crack