# Open Weather API

This API collects weather data from the OpenWeatherMap API and provides endpoints for retrieving that data. The current API is hosted for testing purposes at the following domain:

**API Base URL**: https://weather-challenge.ctdevelopers.solutions

## API Documentation

You can access the API documentation and test the endpoints via Swagger:

**Swagger UI**: https://weather-challenge.ctdevelopers.solutions/swagger/

## Usage

### Collect Weather Data

To collect weather data for a specific user-defined ID, use the following `curl` command:

```
curl --request POST \
  --url https://weather-challenge.ctdevelopers.solutions/collect/ \
  --header 'Content-Type: application/json' \
  --data '{
        "user_defined_id": <id_here>
}'
```

#### Check Progress
To check the progress of data collection for a specific user-defined ID, use the following `curl` command:

```
curl -L --request GET \
  --url https://weather-challenge.ctdevelopers.solutions/progress/<id_here>
```

## Local Installation
If you want to run the application locally, follow the steps below:

* Clone the repository to your local machine.
* Navigate to the project directory.
* Rename the .env_example file to .env and insert your Open Weather API Key where indicated.
* Build and run the application using Docker: docker compose up --build

## API Documentation
Swagger and ReDoc

Swagger: Access at localhost:8007/swagger
ReDoc: Access at localhost:8007/redoc

## Endpoints Usage

### Collect Weather Data (POST)
Initiate the data collection process by specifying a user_defined_id.


```
curl --request POST \
  --url http://localhost:8007/collect/ \
  --header 'Content-Type: application/json' \
  --data '{
        "user_defined_id": <id_here>
}'
```
### Monitor Collection Progress (GET)
Monitor the progress of a previously initiated data collection

```
curl -L --request GET \
  --url http://localhost:8007/progress/<id_here>
```

## Testing

### Setting Up the Test Environment:
Navigate to the root directory of the Django project.
Activate your virtual environment.
Install the required testing packages:
pip install -r requirements.txt
Running the Tests:
To execute all tests:
```
python3 manage.py test open_weather_api --settings=open_weather_project.test_settings
```
For investigating the testing coverage, run the following command:
```
coverage run --source=open_weather_api manage.py test open_weather_api --settings=open_weather_project.test_settings
```
and then
```
coverage report
```