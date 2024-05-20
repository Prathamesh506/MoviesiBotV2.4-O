import motor.motor_asyncio
from info import DATABASE_NAME
DATABASE_URI = "mongodb+srv://MoviesiBotV6:MoviesiBotV5@cluster0.zs9smub.mongodb.net/?retryWrites=true&w=majority"
from datetime import datetime, timedelta
import pymongo
import pytz

class Database:
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.verif_col = self.db.verification_counts
        self.timezone = pytz.timezone('Asia/Kolkata') 
        self.col = self.db.users
        self.grp = self.db.groups
        self.search_col = self.db.search_data
        self.user_data_col = self.db.user_data 
        try:
            self.search_col.drop_index("timestamp_1")
        except pymongo.errors.OperationFailure as e:
            print(f"Error dropping index 'timestamp_1'")
        try:
            self.search_col.create_index("timestamp", expireAfterSeconds=6000)
        except pymongo.errors.OperationFailure as e:
            print(f"Error creating index 'timestamp': {e}")

    async def store_search(self, user_id, search_query):
        search_data = {
            'user_id': user_id,
            'search_query': search_query,
            'timestamp': datetime.utcnow()
        }
        await self.search_col.insert_one(search_data)

    async def retrieve_latest_search(self, user_id):
        result = await self.search_col.find_one({'user_id': user_id}, sort=[('timestamp', pymongo.DESCENDING)])
        latest_search = result.get('search_query') if result else None
        return latest_search

    def new_user(self, id, name):
        return dict(
            id = id,
            name = name,
            ban_status=dict(
                is_banned=False,
                ban_reason="",
            ),
        )

    def new_group(self, id, title):
        return dict(
            id = id,
            title = title,
            chat_status=dict(
                is_disabled=False,
                reason="",
            ),
        )
    
    async def update_verification(self, id, date, time):
        status = {
            'date': str(date),
            'time': str(time)
        }
        await self.col.update_one({'id': int(id)}, {'$set': {'verification_status': status}})

    async def get_verified(self, id):
        default = {
            'date': "1999-12-31",
            'time': "23:59:59"
        }
        user = await self.col.find_one({'id': int(id)})
        if user:
            return user.get("verification_status", default)
        return default
    
    async def add_user(self, id, name):
        user = self.new_user(id, name)
        await self.col.insert_one(user)
    
    async def is_user_exist(self, id):
        user = await self.col.find_one({'id':int(id)})
        return bool(user)
    
    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        return self.col.find({})
    
    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

    async def get_banned(self):
        users = self.col.find({'ban_status.is_banned': True})
        chats = self.grp.find({'chat_status.is_disabled': True})
        b_chats = [chat['id'] async for chat in chats]
        b_users = [user['id'] async for user in users]
        return b_users, b_chats
    
    async def get_username_by_id(self, user_id):
        user = await self.col.find_one({'id': int(user_id)})
        return user.get('name') if user else None

    async def add_chat(self, chat, title):
        chat = self.new_group(chat, title)
        await self.grp.insert_one(chat)
    
    async def get_chat(self, chat):
        chat = await self.grp.find_one({'id':int(chat)})
        return False if not chat else chat.get('chat_status')
    
    async def re_enable_chat(self, id):
        chat_status=dict(
            is_disabled=False,
            reason="",
            )
        await self.grp.update_one({'id': int(id)}, {'$set': {'chat_status': chat_status}})
        
    async def update_settings(self, id, settings):
        await self.grp.update_one({'id': int(id)}, {'$set': {'settings': settings}})
    
    async def get_user_data(self, user_id):
        user_data = await self.user_data_col.find_one({'user_id': user_id})
        if user_data:
            return {
                'language': user_data.get('language'),
                'quality': user_data.get('quality'),
                'subtitles': user_data.get('subtitles'),
                'last_search': user_data.get('last_search')
            }
        else:
            return None
   
    async def update_user_data(self, user_id, language=None, quality=None, subtitles=None, watch_list=None, last_search=None):
        update_fields = {}

        if language == "all":
            update_fields['$set'] = {'language': None}
        elif language is not None:
            update_fields['$set'] = {'language': language}

        if quality == "all":
            update_fields['$set'] = {'quality': None}
        elif quality is not None:
            update_fields['$set'] = {'quality': quality}

        if subtitles == "all":
            update_fields['$set'] = {'subtitles': None}
        elif subtitles is not None:
            update_fields['$set'] = {'subtitles': subtitles}

        if last_search is not None:
            update_fields['$set'] = {'last_search': last_search}

        if update_fields:
            await self.user_data_col.update_one(
                {'user_id': int(user_id)},
                update_fields,
                upsert=True
            )

    async def total_chat_count(self):
        count = await self.grp.count_documents({})
        return count
    
    async def get_all_chats(self):
        return self.grp.find({})

    async def get_db_size(self):
        return (await self.db.command("dbstats"))['dataSize']

    #VERIFICATION COUNT 
    async def count_verify(self, date_str=None):
        """
        Records a verification for the given date.
        
        Args:
            date_str (str): Date in "YYYY-MM-DD" format.
        """
        if date_str is None:
            # Get current date in Indian Calcutta timezone
            current_date = datetime.now(self.timezone)
            date_str = current_date.strftime("%Y-%m-%d")

        await self.verif_col.update_one({"date": date_str}, {"$inc": {"count": 1}}, upsert=True)

    async def get_verify_count(self, date_str=None):
        """
        Retrieves the verification count for a specific date.
        If no date is provided, retrieves the verification count for the present day in Indian Calcutta time.
        
        Args:
            date_str (str, optional): Date in "YYYY-MM-DD" format. Defaults to None.
        
        Returns:
            int: Verification count for the specified day.
        """
        if date_str is None:
            # Get current date in Indian Calcutta timezone
            current_date = datetime.now(self.timezone)
            date_str = current_date.strftime("%Y-%m-%d")
        
        document = await self.verif_col.find_one({"date": date_str})
        return document["count"] if document else 0

    async def get_month_verify_count(self, year=None, month=None):
        """
        Retrieves the verification counts for a specific month.
        
        Args:
            year (int): Year.
            month (int): Month.
        
        Returns:
            dict: Dictionary containing verification counts for each day in the month.
        """
        if year is None or month is None:
            # Get current year and month
            current_date = datetime.now(self.timezone)
            year = current_date.year if year is None else year
            month = current_date.month if month is None else month

        start_date = datetime(year, month, 1).strftime("%Y-%m-%d")
        end_date = (datetime(year, month, 1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        end_date_str = end_date.strftime("%Y-%m-%d")
        
        cursor = self.verif_col.find({
            "date": {"$gte": start_date, "$lte": end_date_str}
        })
        
        verification_counts = {}
        async for document in cursor:
            verification_counts[document["date"]] = document["count"]
        return verification_counts

db = Database(DATABASE_URI, DATABASE_NAME)
