dump_api:
	python ./backend/manage.py dumpdata api > ./backend/fixtures/api.json

loaddata_api:
	python ./backend/manage.py loaddata ./backend/fixtures/api.json

# Установить стили для панели DRF
css_to_drf:
	cat ./backend/utils/css_base_drf.css > /usr/local/lib/python3.11/site-packages/rest_framework/static/rest_framework/css/default.css

_mv_dev_to_root:
	mv ./dev_conf/.env ./dev_conf/docker-compose_dev.yml ./dev_conf/Dockerfile_Django ./dev_conf/Dockerfile_Vue ./dev_conf/cors.conf .

_mv_root_to_dev:
	mv .env docker-compose_dev.yml Dockerfile_Django Dockerfile_Vue cors.conf ./dev_conf

build_dev:
	make _mv_dev_to_root ; docker-compose -f ./docker-compose_dev.yml build & sleep 5 && make _mv_root_to_dev

run_dev:
	make _mv_dev_to_root ; docker-compose -f ./docker-compose_dev.yml up & sleep 5 && make _mv_root_to_dev