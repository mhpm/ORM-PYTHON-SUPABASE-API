import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


# import os
# from supabase import create_client, Client
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()


# def get_supabase_client() -> Client:
#     supabase_url = os.getenv("SUPABASE_URL")
#     supabase_key = os.getenv("SUPABASE_KEY")

#     # Debugging output
#     print(f"Supabase URL: {supabase_url}")
#     print(f"Supabase Key: {supabase_key}")

#     if not supabase_url or not supabase_key:
#         raise ValueError("Supabase credentials are not set in the environment")
#     return create_client(supabase_url, supabase_key)
