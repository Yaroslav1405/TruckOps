import flet as ft
from datetime import datetime

class SessionManager:
    def __init__(self):
        self.page = None
        
    @staticmethod
    def get_user_id(page: ft.Page) -> str:
        """Retrieve the user ID from the session."""
        return page.session.get('user_id')
    
    @staticmethod
    def get_access_token(page: ft.Page) -> str:
        """Retrieve the access token from the session."""
        return page.session.get('access_token')
    
    @staticmethod
    def get_refresh_token(page: ft.Page) -> str:
        """Retrieve the refresh token from the session."""
        return page.session.get('refresh_token')
    
    @staticmethod
    async def logout(page: ft.Page, supabase=None):
        """Clear the session and redirect to the login page."""
        try:
            if supabase:
               await supabase.auth.sign_out()
               with open('storage/session.txt', 'w') as f:
                   pass
               print("User logged out successfully.")
            else: 
                print("Supabase client not provided for logout.")
        except Exception as e:
            print(f"Error during logout: {e}")
            
        page.session.clear()
        page.go('/')
    
    @staticmethod
    def get_user_data(page) -> dict:
        if not page:
            print('Session.py - No user data found.')
            return {}
        
        return {
            'user_id': page.session.get('user_id'),
            'access_token': page.session.get('access_token'),
            'refresh_token': page.session.get('refresh_token'),
        }
    
    @staticmethod
    def require_auth(page: ft.Page):
        """Check if the user is authenticated."""
        user_id = SessionManager.get_user_id(page)
        if not user_id:
            print("User is not authenticated, redirecting to login.")
            page.go('/')
            return False
        return True
    
    
    # TEMP SOLLUTION
    def retrieve_session_data(page: ft.Page):
        with open('storage/session.txt', 'r') as f:
            try: 
                access_tkn = f.readline().split('=')[1].strip()
                refresh_tkn = f.readline().split('=')[1].strip()
                u_id = f.readline().split('=')[1].strip()
                
                if access_tkn and refresh_tkn and u_id:
                    page.session.set('access_token', access_tkn)
                    page.session.set('refresh_token', refresh_tkn)
                    page.session.set('user_id', u_id)
                    print(f"✅ Previous session data retrieved successfully")
                    # page.go('/dashboard')
                    f.close()
                    return True
                else:
                    print(f'No previous session data found, proceeding with login...')
                    # page.go('/')
                    f.close()
                    return False
            except:
                print('File is empty, proceeding with login...')
                f.close()
                return False
        
        