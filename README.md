## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/jbrun0r/api-flask.git
   cd api-flask
   ```

2. Create and activate a virtual environment:

   ```shell
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the required packages:

   ```shell
   pip install -r requirements.txt
   ```

4. Set up the database:

   - Make sure you have a PostgreSQL server running.
   - Create a new PostgreSQL database for the API.

   ```shell
   psql -U your_username -c "CREATE DATABASE api"
   ```

## Usage

To start the API, run the following command:

```shell
export FLASK_APP=api
flask setup_api_database
python3 api.py
```

The API will be available at `http://localhost:5000`.

## API Endpoints

The API provides the following endpoints:

- `/auth` - Authentication endpoints
- `/error` - API Error management endpoints
- `/user` - User management endpoints

Please refer to the API documentation or Postman collection for detailed information about the available endpoints, request payloads, and responses.

## Credits

The API is developed and maintained by João Bruno.
