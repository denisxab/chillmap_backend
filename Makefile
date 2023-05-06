dump_api:
	python manage.py dumpdata api > fixtures/api.json

loaddata_api:
	python manage.py loaddata fixtures/api.json

# Установить стили для панели DRF
css_to_drf:
	cat ./utils/css_base_drf.css > /usr/local/lib/python3.11/site-packages/rest_framework/static/rest_framework/css/default.css

build_dev:
	mv dev_conf/* . && docker-compose -f ./dev_conf/docker-compose.yml build

run_dev:
	docker-compose -f ./dev_conf/docker-compose.yml up