build:
	docker build -t app .

run:
	docker run -p 8000:8000 app