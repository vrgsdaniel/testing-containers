# testing-containers
Sample project to test an application with external service dependencies

When developing a new application, often enough we need external services such as databases, message brokers, cache memory, or APIs to other micro-services.

One way to conduct these tests is by running the dependencies as containers that communicate with the application in an environment similar to production.
This repo illustrates how to run these type of tests in a CI pipeline using Github actions in a small python application with access to a postgres database to create and select users.
The tests use pytest, the database will be run as a postgres docker container, and the tests will be coordinated with tox. 
