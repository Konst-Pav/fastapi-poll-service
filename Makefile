exec_db_container:
	docker exec -it poll-service-pg-1 psql -U user poll_app_db

run_db_container:
	docker compose up -d pg

stop_db_container:
	docker stop poll-service-pg-1
