


dump:
	python manage.py dumpdata > fixtures/base_test_data.json

loaddata:
	python manage.py loaddata fixtures/base_test_data.json