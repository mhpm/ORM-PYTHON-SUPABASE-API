from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from app.supabase_client import supabase
import logging

# Blueprint setup
users_bp = Blueprint("users", __name__)
logging.basicConfig(level=logging.INFO)


# Helper: Centralized error handling
def handle_supabase_error(response):
    if "errors" in response and response["errors"]:
        return {"error": response["errors"][0]["message"]}, 400
    return None


def handle_exception(e):
    logging.error(f"Error: {str(e)}")
    return {"error": "Internal server error"}, 500


# GET all users
@users_bp.route("/users", methods=["GET"])
def get_users():
    try:
        # Query parameters for pagination
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        offset = (page - 1) * limit

        if page < 1 or limit < 1:
            raise ValueError("Pagination parameters must be positive integers.")

        # Fetch total count of users
        total_response = supabase.table("users").select("*", count="exact").execute()
        error_response = handle_supabase_error(total_response)
        if error_response:
            return jsonify(error_response), 400

        total_count = total_response.count

        # Fetch users with pagination
        response = (
            supabase.table("users")
            .select("*")
            .range(offset, offset + limit - 1)
            .order("id", desc=True)
            .execute()
        )
        error_response = handle_supabase_error(response)
        if error_response:
            return jsonify(error_response), 400

        if not response.data:
            return {"message": "No users found"}, 404

        return {
            "users": response.data,
            "page": page,
            "limit": limit,
            "total": total_count,
        }, 200

    except ValueError as e:
        logging.warning(f"Invalid pagination: {str(e)}")
        return {"error": "Invalid pagination parameters"}, 400
    except Exception as e:
        return handle_exception(e)


# GET a specific user by ID
@users_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    try:
        response = supabase.table("users").select("*").eq("id", user_id).execute()
        error_response = handle_supabase_error(response)
        if error_response:
            return jsonify(error_response), 400

        if not response.data:
            return {"error": "User not found"}, 404

        return response.data[0], 200

    except Exception as e:
        return handle_exception(e)


# POST create a new user
@users_bp.route("/users", methods=["POST"])
def create_user():
    try:
        new_user = request.get_json()

        # Validate input
        required_fields = ["first_name", "last_name", "email", "password"]
        missing_fields = [field for field in required_fields if field not in new_user]
        if missing_fields:
            return {"error": f"Missing fields: {', '.join(missing_fields)}"}, 400

        hashed_password = generate_password_hash(new_user["password"])

        user_data = {
            "first_name": new_user["first_name"],
            "last_name": new_user["last_name"],
            "email": new_user["email"],
            "password": hashed_password,
            "role": new_user.get("role", "user"),
            "avatar": new_user.get(
                "avatar",
                "https://avatars.githubusercontent.com/u/273650",
            ),
        }

        response = supabase.table("users").insert(user_data).execute()
        error_response = handle_supabase_error(response)
        if error_response:
            return jsonify(error_response), 400

        return {
            "message": "User created successfully",
            "user_id": response.data[0]["id"],
        }, 201

    except Exception as e:
        return handle_exception(e)


# PUT update an existing user
@users_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        updated_user = request.get_json()
        if not updated_user:
            return {"error": "No update data provided"}, 400

        response = (
            supabase.table("users").update(updated_user).eq("id", user_id).execute()
        )
        error_response = handle_supabase_error(response)
        if error_response:
            return jsonify(error_response), 400

        if not response.data:
            return {"error": "User not found"}, 404

        return {"message": "User updated successfully"}, 200

    except Exception as e:
        return handle_exception(e)


# DELETE a user
@users_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        response = supabase.table("users").delete().eq("id", user_id).execute()
        error_response = handle_supabase_error(response)
        if error_response:
            return jsonify(error_response), 400

        if not response.data:
            return {"error": "User not found"}, 404

        return {"message": "User deleted successfully"}, 200

    except Exception as e:
        return handle_exception(e)
