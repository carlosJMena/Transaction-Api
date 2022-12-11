# Transaction Api

## Requirements

- Docker

## Usage

Run server
`sh run.sh`

Stop server
`sh stop.sh`

Run tests
`sh run-tests.sh`

The app will be running at localhost:8080  

## Endpoints
swagger in http://localhost:8080/swagger/
### User

**POST**/**GET** `/user/`

**GET** `/user/{user_id}`

### Account Summary
**GET** `/user/{user_id}/account-summary/`

**GET** `/user/{user_id}/account-summary/?date_from=2021-01-01&date_to=2021-02-01`

### Category Summary
**GET** `/user/{user_id}/category-summary/`


### Transaction
**POST** `/transaction/`





