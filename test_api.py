import pytest
from app import app
from models import session, Bank, Branch, seed_data


@pytest.fixture(autouse=True)
def setup_database():
    """Clear tables and insert fresh sample data before every test."""
    # remove any existing rows
    session.query(Branch).delete()
    session.query(Bank).delete()
    session.commit()

    # populate with known values
    seed_data()
    yield
    # teardown: rollback any dangling transactions
    session.rollback()


def run_query(client, query, variables=None):
    return client.post("/gql", json={"query": query, "variables": variables})


def test_graphql_branches_structure():
    client = app.test_client()
    query = """
    query {
        branches {
            edges {
                node {
                    branch
                    ifsc
                    bank {
                        name
                    }
                }
            }
        }
    }
    """
    resp = run_query(client, query)
    assert resp.status_code == 200
    data = resp.get_json()
    # ensure the connection format is present
    assert "branches" in data["data"]
    edges = data["data"]["branches"]["edges"]
    assert len(edges) >= 1
    node = edges[0]["node"]
    assert node["branch"] == "Main" or node["branch"] == "West"
    assert node["bank"]["name"] == "Example Bank"


def test_rest_endpoints():
    client = app.test_client()
    resp = client.get("/banks")
    assert resp.status_code == 200
    banks = resp.get_json()
    assert isinstance(banks, list)
    assert banks[0]["name"] == "Example Bank"

    # check branch detail endpoint picks up a valid id
    branch_id = session.query(Branch).first().id
    resp = client.get(f"/branches/{branch_id}")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["bank"]["name"] == "Example Bank"

    # 404 for missing branch
    resp = client.get("/branches/999999")
    assert resp.status_code == 404
