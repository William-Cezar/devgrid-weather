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
        "user_defined_id": "<id_here>"
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

