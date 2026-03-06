# Bank API

Simple Python API server providing both GraphQL and REST interfaces for bank and branch data. Uses Flask, SQLAlchemy and Graphene.

## Features

- **GraphQL endpoint** at `/gql` (supports relay-style connections)  
  Example query:
  ```graphql
  query {
    branches {
      edges {
        node {
          branch
          ifsc
          bank { name }
        }
      }
    }
  }
  ```

- **REST endpoints**
  - `GET /banks` – list all banks
  - `GET /branches/<id>` – branch details including bank name

- Database seeded automatically when empty (see `models.seed_data`).
- Tests using `pytest` demonstrate functionality.
- Configurable via `DATABASE_URL` environment variable.

## Getting started

1. Create & activate a virtual environment:
   ```sh
   python -m venv venv
   .\venv\Scripts\activate   # Windows
   # source venv/bin/activate  # Unix
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Seed the database (optional; happens automatically when the app runs):
   ```python
   from models import seed_data
   seed_data()
   ```

4. Run the server:
   ```sh
   python app.py
   ```
   Server will be available at `http://localhost:5000`.

5. Run tests:
   ```sh
   pytest -q
   ```

## Deployment (Heroku example)

1. Ensure Heroku CLI is installed and you are logged in.
2. Create a new Heroku app:
   ```sh
   heroku create my-bank-api
   ```
3. Set the buildpacks (Python is automatic) and push:
   ```sh
   git add .
   git commit -m "prepare for deployment"
   git push heroku main
   ```
4. The `Procfile` will start `gunicorn app:app`.  Heroku will provide a `DATABASE_URL` for a Postgres database.
5. Run migrations/seed if necessary:
   ```sh
   heroku run python -c "from models import seed_data; seed_data()"
   ```

## Code quality & extensions

- Clean modular code with SQLAlchemy models and a GraphQL schema.
- Tests cover key API paths.
- To extend, add mutations, filtering, additional REST resources, or integrate authentication.

---

Feel free to reach out if you'd like help deploying or adding features!