# SWORD tech test

### Quickstart

Build the app container

```shell
docker-compose up -d --build
````

Setup the database and create a super user (manager) and a technician

- username: sword
- password: sword123 (both super user's and technician)

```shell
make setup
```

---

### How to use it

You can browse http://127.0.0.1:8000/admin to manage tasks and users like a human

##### User role as 1 is MANAGER, 2 is TECHNICIAN

Get super-user (manager) token with

```shell
curl http://127.0.0.1:8000/api-token-auth/ -H "Content-Type: application/json" -d '{"username": "sword", "password": "sword123"}'
```

Create a task for user with id 2 (the one created with the super-user)

```shell
curl http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -H "Authorization: Token <manager-token>" -d '{"user": 2, "summary": "Code like you know it"}'
```

List the task you just assigned technician with id 2 to

```shell
curl http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -H "Authorization: Token <manager-token>"
```

Set the task with id 1 as finished

```shell
curl http://127.0.0.1:8000/tasks/1 -H "Content-Type: application/json" -H "Authorization: Token <tech-token>" -XPATCH -d '{"performed_at": "2021-07-12"}'
```

At this point you show have logged at the sword_consumer container the message displaying the performed task

You can also browse at http://127.0.0.1:8000/tasks for the API browsable site (needs Authorization: "Token <token>"

### Requirements

You are developing a software to account for maintenance tasks performed during a working day. This application has two
types of users (Manager, Technician).

The technician performs tasks and is only able to see, create or update his own performed tasks.

The manager can see tasks from all the technicians, delete them, and should be notified when some tech performs a task.

A task has a summary (max: 2500 characters) and a date when it was performed, the summary from the task can contain
personal information.

### Notes

- If you don’t have enough time to complete the test you should prioritize complete features ( with tests) over many
  features. We’ll evaluate security, quality and readability of your code
- This test is suitable for all levels of developers, so make sure to prove yours

### Development Features

- Create API endpoint to save a new task
- Create API endpoint to list tasks
- Notify manager of each task performed by the tech (This notification can be just a print saying “The tech X performed
  the task Y on date Z”)
- This notification should not block any http request

### Tech Requirements

- Use any language to develop this HTTP API (we use Go, Node and PHP)
- Create a local development environment using docker containing this service and a MySQL database
- Use MySQL database to persist data from the application
- Features should have unit tests to ensure they are working properly

### Bonus:

- Use a message broker to decouple notification logic from the application flow
- Create Kubernetes object files needed to deploy this application

---

# Solution

### Tests

```shell
make test
```

Django creates a test database, applies all migrations and then run tests
This is not unit test, but it tests a whole more
The unit tests I made are for business rules (in test_models.py and test_validations.py)

### TODO

- Mock call to publish

### Notes

- It was not specified an endpoint to create users. Django Admin is used instead

- A manager is able to assign a task to another manager!
- Returning 404 when a technician tries to GET an existing TASK not their own

- Technician cannot update their task user
- Task summary should be updatable?

- For the sake of simplicity the performed task is going through the queue (not just its id)
