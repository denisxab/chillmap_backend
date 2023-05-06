dump_api:
	python ./backend/manage.py dumpdata api > fixtures/api.json

loaddata_api:
	python ./backend/manage.py loaddata fixtures/api.json

# Установить стили для панели DRF
css_to_drf:
	cat ./utils/css_base_drf.css > /usr/local/lib/python3.11/site-packages/rest_framework/static/rest_framework/css/default.css

_mv_dev_to_root:
	mv dev_conf/.env dev_conf/docker-compose_dev.yml dev_conf/Dockerfile_Django dev_conf/Dockerfile_Vue .

_mv_root_to_dev:
	mv .env docker-compose_dev.yml Dockerfile_Django Dockerfile_Vue dev_conf

build_dev:
	make _mv_dev_to_root && docker-compose -f ./docker-compose_dev.yml build ; make _mv_root_to_dev

run_dev:
	make _mv_dev_to_root && docker-compose -f ./docker-compose_dev.yml up ; make _mv_root_to_dev