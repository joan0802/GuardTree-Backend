from supabase import create_client, Client
from dotenv import load_dotenv
import os
from typing import Dict, List, Optional, Any

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase: Client = create_client(
    supabase_url=os.getenv("SUPABASE_URL"),
    supabase_key=os.getenv("SUPABASE_KEY")
)

class SupabaseService:
    @staticmethod
    async def get_all(table: str) -> List[Dict[str, Any]]:
        """Fetch all records from a table"""
        response = supabase.table(table).select("*").execute()
        return response.data

    @staticmethod
    async def get_by_id(table: str, id: Any) -> Optional[Dict[str, Any]]:
        """Fetch a single record by ID"""
        response = supabase.table(table).select("*").eq("id", id).execute()
        return response.data[0] if response.data else None

    @staticmethod
    async def create(table: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new record"""
        response = supabase.table(table).insert(data).execute()
        return response.data[0] if response.data else None

    @staticmethod
    async def update(table: str, id: Any, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a record by ID"""
        response = supabase.table(table).update(data).eq("id", id).execute()
        return response.data[0] if response.data else None

    @staticmethod
    async def delete(table: str, id: Any) -> bool:
        """Delete a record by ID"""
        response = supabase.table(table).delete().eq("id", id).execute()
        return bool(response.data)

    @staticmethod
    async def query(
        table: str,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Query records with filters, ordering, and limit"""
        query = supabase.table(table).select("*")
        
        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)
        
        if order_by:
            query = query.order(order_by)
            
        if limit:
            query = query.limit(limit)
            
        response = query.execute()
        return response.data 
    
    @staticmethod
    async def query_field_by_conditions(
        table: str,
        filters: Dict[str, Any],
        field: str
    ) -> Optional[Any]:
        """Query a single field value with multiple conditions"""
        query = supabase.table(table).select(field)
        for key, value in filters.items():
            query = query.eq(key, value)
        response = query.execute()
        if response.data and field in response.data[0]:
            return response.data[0][field]
        return None
    
    @staticmethod
    async def query_multiple_fields_by_conditions(
        table: str,
        filters: Dict[str, Any],
        fields: List[str]
    ) -> Optional[Dict[str, Any]]:
        """Query multiple field values with multiple conditions"""
        query = supabase.table(table).select(",".join(fields))
        for key, value in filters.items():
            query = query.eq(key, value)
        response = query.execute()
        if response.data:
            return response.data[0]
        return None

