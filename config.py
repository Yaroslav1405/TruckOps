import os
from supabase import create_client, Client
from dotenv import load_dotenv
from supabase._sync.client import SupabaseException

load_dotenv()
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client | None = None
db_init_successful = False

if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        db_init_successful = True
    except SupabaseException as e:
        db_init_successful = False
    except Exception as e:
        db_init_successful = False
else:
    db_init_successful = False