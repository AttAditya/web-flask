from provider import mongo_db

class Drive:
    def __init__(self, name: str) -> None:
        self.name = name
        self.data = mongo_db[name]

        print(f"Connected to {name} database")

    def get(self, filename: str) -> dict:
        content = self.data.find_one({
            "_id": filename
        })

        if not content: return None

        class File:
            def read(self):
                return content["content"]
        
        return File()

    def put(self, filename: str, data: str) -> None:
        self.delete(filename)

        save_data = {
            "_id": filename,
            "content": data
        }

        self.data.insert_one(save_data)

    def delete(self, filename: str) -> None:
        self.data.delete_one({
            "_id": filename
        })

