dump_api:
	python manage.py dumpdata api --indent 4 > ./fixtures/api.json

loaddata:
	python manage.py loaddata ./fixtures/api.json ./fixtures/user.json

# Установить стили для панели DRF
css_to_drf:
	cat ./utils/css_base_drf.css > /usr/local/lib/python3.11/site-packages/rest_framework/static/rest_framework/css/default.css

runserver:
	python manage.py runserver 0.0.0.0:8181

migrate:
	python manage.py makemigrations && python manage.py migrate;
