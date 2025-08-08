import asyncio
from config import get_supabase_client
from helper_functions import show_message



async def fetch_loads(user_id, page, error_snackbar):
    try:
        supabase = get_supabase_client()
        response = await supabase.table("Loads").select("*").eq("dispatcher_name", user_id).order('date', desc=True).limit(10).execute()
        loads_data = response.data
        return loads_data
    except Exception as e:
        print(f"Error fetching loads: {e}")
        show_message(page, error_snackbar, f'Fetch error: {e}')
        return []