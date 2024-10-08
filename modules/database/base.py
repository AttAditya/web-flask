from provider import mongo_db

class Base:
    def __init__(self, name: str) -> None:
        self.name = name
        self.data = mongo_db[name]

        print(f"Connected to {name} database")

    def get(self, key: str) -> dict:
        return self.data.find_one({
            "_id": key
        })

    def put(self, data: dict, key: str = None) -> None:
        self.delete(key)
        
        if key:
            data["_id"] = key
        
        self.data.insert_one(data)

    def get_all(self) -> list:
        return list(self.data.find())

    def delete(self, key: str) -> None:
        self.data.delete_one({
            "_id": key
        })

