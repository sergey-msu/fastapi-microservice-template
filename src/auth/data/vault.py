'''
    Mongo valult for store users tokens
'''
from motor.motor_asyncio import AsyncIOMotorClient


class Vault:
    '''
        Mongo valult for store users tokens
    '''
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        tokens_db: str,
        tokens_coll: str,
    ):
        self.tokens_db_name = tokens_db
        self.tokens_coll_name = tokens_coll
        self.db_url: str = f'mongodb://{username}:{password}@{host}:{port}/'

        self.tokens_db = None
        self.tokens_coll = None
        self.client = None

    def open(self):
        self.client = AsyncIOMotorClient(self.db_url)
        self.tokens_db = self.client[self.tokens_db_name]
        self.tokens_coll = self.tokens_db[self.tokens_coll_name]

    def close(self):
        self.client.close()
        self.client = None

    async def save_refresh_token(self, user_id: str, refresh_token: str) -> bool:
        '''
            Save (upsert) new mapping user_id:refresh_token into DB
        '''

        fltr = {'user_id': user_id}
        update = {'$set': {'user_id': user_id, 'refresh_token': refresh_token}}
        result = await self.tokens_coll.update_one(fltr, update, upsert=True)

        return result.upserted_id is not None

    async def remove_refresh_token(self, user_id: str):
        '''
            Delete user_id:refresh_token mapping from DB
        '''
        await self.tokens_coll.delete_many({'user_id': user_id})

    async def get_refresh_token(self, user_id: str) -> str:
        '''
            Get user refresh token from DB
        '''
        token_data = await self.tokens_coll.find_one({'user_id': user_id})
        return token_data['refresh_token'] if token_data else None
