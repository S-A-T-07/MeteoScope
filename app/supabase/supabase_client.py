from supabase import create_client
from supabase._sync.client import SyncClient

from app.core.config import settings


class SupabaseClient:
    """
    creates a Singleton for the subabase client

    Returns:
        supabse_client_instanse: Client
    """

    _instance = None

    def __new__(cls) -> SyncClient:
        if cls._instance is None:
            url = settings.SUPABASE_URL
            key = settings.SUPABASE_KEY
            cls._instance = create_client(url, key)
        return cls._instance


# Usage
supabase_client = SupabaseClient()
