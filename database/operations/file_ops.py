from typing import Optional, List
from database.connection import db
from database.models.files import FileModel

class FileOperations:
    def __init__(self):
        self.collection_name = FileModel.COLLECTION_NAME
    
    async def create_file(self, file_data: dict) -> str:
        collection = db.get_collection(self.collection_name)
        result = await collection.insert_one(file_data)
        return str(result.inserted_id)
    
    async def get_file_by_unique_id(self, unique_id: str) -> Optional[dict]:
        collection = db.get_collection(self.collection_name)
        return await collection.find_one({"unique_id": unique_id})
    
    async def get_file_by_post_no(self, post_no: int) -> Optional[dict]:
        collection = db.get_collection(self.collection_name)
        return await collection.find_one({"post_no": post_no})
    
    async def check_post_no_exists(self, post_no: int) -> bool:
        collection = db.get_collection(self.collection_name)
        count = await collection.count_documents({"post_no": post_no})
        return count > 0
    
    async def get_all_files(self) -> List[dict]:
        collection = db.get_collection(self.collection_name)
        cursor = collection.find({})
        return await cursor.to_list(length=None)

file_ops = FileOperations()
