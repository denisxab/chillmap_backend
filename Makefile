dump_api:
	python manage.py dumpdata api > fixtures/api.json

loaddata_api:
	python manage.py loaddata fixtures/api.json

# Установить стили для панели DRF
css_to_drf:
	cat ./utils/css_base_drf.css > /usr/local/lib/python3.11/site-packages/rest_framework/static/rest_framework/css/default.css

_mv_dev_to_root:
	mv dev_conf/.env dev_conf/docker-compose.yml dev_conf/Dockerfile_Django dev_conf/Dockerfile_Vue .

_mv_root_to_dev:
	mv .env docker-compose.yml Dockerfile_Django Dockerfile_Vue dev_conf

build_dev:
	make _mv_dev_to_root && docker-compose -f ./dev_conf/docker-compose.yml build & _mv_root_to_dev

run_dev:
	make _mv_dev_to_root && docker-compose -f ./dev_conf/docker-compose.yml up & _mv_root_to_dev