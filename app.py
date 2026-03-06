from flask import Flask, request, jsonify, abort
from schema import schema
from models import session, Bank, Branch

app = Flask(__name__)


@app.route("/gql", methods=["POST"])
def graphql_server():
    # Graphene expects a `context_value` that contains the DB session when
    # using SQLAlchemyConnectionField.
    data = request.get_json() or {}
    query = data.get("query")
    variables = data.get("variables")

    result = schema.execute(
        query,
        variable_values=variables,
        context_value={"session": session},
    )

    payload = {}
    if result.errors:
        # propagate errors in response body so clients can inspect
        payload["errors"] = [str(e) for e in result.errors]
    payload["data"] = result.data

    return jsonify(payload)


# simple REST endpoints for bonus points; they recycle the same session and
# models used by GraphQL
@app.route("/banks", methods=["GET"])
def get_banks():
    banks = session.query(Bank).all()
    return jsonify([{"id": b.id, "name": b.name} for b in banks])


@app.route("/branches/<int:branch_id>", methods=["GET"])
def get_branch(branch_id):
    branch = session.query(Branch).get(branch_id)
    if branch is None:
        abort(404)

    return jsonify({
        "id": branch.id,
        "branch": branch.branch,
        "ifsc": branch.ifsc,
        "address": branch.address,
        "bank": {"id": branch.bank.id, "name": branch.bank.name},
    })


if __name__ == "__main__":
    app.run(debug=True)