# DJANGO
run:
	docker-compose up

migrate:
	docker-compose exec django python manage.py migrate

loadinitialdata:
	docker-compose exec django python manage.py loaddata fixtures/initial.json

createsuperuser:
	docker-compose run --rm django \
		bash -c "echo \"from django.contrib.auth import get_user_model; \
		get_user_model().objects.create_superuser('admin', 'admin@example.com', 'admin')\" \
		| python manage.py shell"

init: migrate loadinitialdata

# DB
dropdb:
	docker-compose run --rm psql dropdb postgres
createdb:
	docker-compose run --rm psql createdb postgres
resetdb: dropdb createdb

# TOOLS
test:
	docker-compose run --rm django python manage.py test