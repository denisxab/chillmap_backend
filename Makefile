_mv_dev_to_root:
	mv ./dev_conf/.env ./dev_conf/docker-compose_dev.yml ./dev_conf/Dockerfile_Django ./dev_conf/Dockerfile_Vue ./dev_conf/cors.conf .

_mv_root_to_dev:
	mv .env docker-compose_dev.yml Dockerfile_Django Dockerfile_Vue cors.conf ./dev_conf

build_dev:
	make _mv_dev_to_root ; docker-compose -f ./docker-compose_dev.yml build & sleep 5 && make _mv_root_to_dev

run_dev:
	make _mv_dev_to_root ; docker-compose -f ./docker-compose_dev.yml up & sleep 5 && make _mv_root_to_dev

down_dev:
	make _mv_dev_to_root ; docker-compose -f ./docker-compose_dev.yml down & sleep 5 && make _mv_root_to_dev
