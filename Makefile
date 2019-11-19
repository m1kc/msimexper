lint:
	flake8 --select=C,F,E101,E112,E502,E72,E73,E74,E9,W291,W6


docker:
	docker build -t 'm1kc/msimexper' .

dockerrun:
	docker run -ti -p 3218:3218 m1kc/msimexper
