dump:
	python manage.py dumpdata > fixtures/base_test_data.json

loaddata:
	python manage.py loaddata fixtures/base_test_data.json

# Установить стили для панели DRF
css_to_drf:
	cat "./utils/css_base_drf.css" > "./venv/lib/python3.11/site-packages/rest_framework/static/rest_framework/css/default.css" 


build_dev:
	sudo docker-compose build

run_dev:
	docker-compose up