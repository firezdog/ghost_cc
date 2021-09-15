play:
	docker build -t wordgame:1.0 .;
	docker run -it wordgame:1.0;

clean:
	docker system prune

.PHONY: play clean