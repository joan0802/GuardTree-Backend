from app.db import database, form_entries_table
from datetime import datetime

class FormRepository:
    @staticmethod
    async def get_all():
        query = form_entries_table.select()
        return await database.fetch_all(query)

    @staticmethod
    async def get_by_id(row_id: int):
        query = form_entries_table.select().where(form_entries_table.c.id == row_id)
        return await database.fetch_one(query)

    @staticmethod
    async def create(data: dict):
        now = datetime.utcnow()
        data.update({"created_at": now, "updated_at": now})
        query = form_entries_table.insert().values(**data)
        record_id = await database.execute(query)
        return {**data, "id": record_id}

    @staticmethod
    async def delete(row_id: int):
        query = form_entries_table.delete().where(form_entries_table.c.id == row_id)
        return await database.execute(query)
