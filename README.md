# HealthBuddy

Dashboard

## Getting Started

### running the project
- Create a file called `.env` at the root of the project.

### Set environment variable
The following variables can be configured on your `.env`, however, are not necessary to run the project:
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`

- `DEBUG`
- `SECRET_KEY`

- `SENDGRID_API_KEY`

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_STORAGE_BUCKET_NAME`
- `AWS_S3_REGION_NAME`

- `DEFAULT_FROM_EMAIL`

- `TOKEN_ORG_RAPIDPRO`


### Docker
Enter the `docker/` directory using this command in the project root:
```shell script
$ cd docker/
```
It is possible for an error to occur when trying to run the entire application at once, the database may not have started 100% and when the application tries to run migrations it returns an error. To avoid this problem, execute for first the database using:
```shell script
$ docker-compose up -d db
```
And later:
```shell script
$ docker-compose up --build
```
