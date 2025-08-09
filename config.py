import os
from supabase import acreate_client, AsyncClient
from dotenv import load_dotenv
from supabase._sync.client import SupabaseException

load_dotenv()


supabase: AsyncClient | None = None
db_init_successful: bool = False

def reload_env():
    load_dotenv(override=True)

async def create_supabase(force_reload_env: bool = False):
    # Define global variables
    global supabase, db_init_successful
    
    # Reload environment variables if requested
    if force_reload_env:
        reload_env()
    
    SUPABASE_URL: str = os.environ.get("SUPABASE_URL")
    SUPABASE_KEY: str = os.environ.get("SUPABASE_KEY")
    
    # Check for environment variables
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Supabase URL or Key not set in environment variables.")
        supabase = None
        db_init_successful = False
        return
    
    # Initialize Supabase client
    try:
        supabase = await acreate_client(SUPABASE_URL, SUPABASE_KEY)
        db_init_successful = True
        print("Supabase client created successfully.")
        return supabase
    except SupabaseException as e:
        db_init_successful = False
    except Exception as e:
        db_init_successful = False
        
def get_supabase_client():
    return supabase

async def reinitialize_supabase():
    return await create_supabase(force_reload_env=True)
        