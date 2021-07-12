TAG?=latest

################################# DOCKER #################################

docker-compose-rebuild: clean
	docker-compose down && docker-compose up -d --build

docker-build: clean
	docker build -t natanael/sword:$(TAG) .

############################# APP SETUP #################################

create-super-user:
	echo "from django.contrib.auth import get_user_model; User = get_user_model(); user = User.objects.create_superuser('sword', 'sword@sword.com', 'sword123', role=1); print(user)" | python manage.py shell

create-manager:
	echo "from apps.authentications.factories import UserFactory; manager = UserFactory(role=1); print(manager)" | python manage.py shell

create-technician:
	echo "from apps.authentications.factories import UserFactory; technician = UserFactory(role=2); print(technician)" | python manage.py shell

setup:
	docker exec -it sword_rest make migrate
	### "Creating Super-User (Manager)..."
	docker exec -it sword_rest make create-super-user
	### "Creating Technician..."
	docker exec -it sword_rest make create-technician

################################# LINT #################################

lint:
	PYTHONPATH=. python -m black ./

################################# TESTS #################################

test: clean
	PYTHONPATH=. python manage.py test

################################# DATABASE MIGRATION #################################

makemigrations:
	PYTHONPATH=. python manage.py makemigrations

migrate:
	PYTHONPATH=. python manage.py migrate


################################# CLEANER #################################

.clean-python: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '*.py.bak' -exec rm --force {} +
	find . -name '__pycache__' -exec rm -fr {} +

.clean-lib: ## remove lib artifacts
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr reports/
	rm -fr .pytest_cache/
	rm -fr .mypy_cache/

clean: .clean-python .clean-lib
