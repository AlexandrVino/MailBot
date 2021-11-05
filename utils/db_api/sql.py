import asyncio
import json
import logging
from dataclasses import dataclass

import asyncpg

# set logging format
logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    # level=logging.DEBUG
                    )


# class, which will keep data for connection with your database
@dataclass
class DBData:
    user: str
    password: str
    database: str
    host: str
    port: int
    path: str


# class, which will interact with your database
class DBSession(DBData):
    def __init__(self, **kwargs):
        super(DBSession, self).__init__(**kwargs)
        self.pool = None
        self.COMMANDS: dict = {}
        self.extra_attributes = ['path', 'COMMANDS', 'pool', 'extra_attributes']

    async def to_dict(self, extra_keys=None) -> dict:
        if extra_keys is None:
            extra_keys = []
        return {key: value for key, value in self.__dict__.items() if key not in self.extra_attributes + extra_keys}

    async def start(self):
        try:
            # trying connect to database
            self.pool = await asyncpg.create_pool(**await self.to_dict())
        except asyncpg.exceptions.ConnectionDoesNotExistError as err:
            # this error will be thrown if the database isn't created
            await create_db(self)  # create database
            logging.error(err)
            self.pool = await asyncpg.create_pool(**await self.to_dict())

        # create table, which will keep info about users
        await self.create_table()

        # taking sql commands from txt file
        with open(self.path + 'db/commands.txt') as sql_file:
            self.COMMANDS = {key: value for key, value in [item.split('==') for item in sql_file.readlines()]}

    async def create_table(self) -> None:
        """
        :param:
        :returns None:
        function, which will be create sql table
        """

        with open(self.path + 'db/create_table.sql', 'r') as sql_file:
            sql_create_table = sql_file.read()
        conn: asyncpg.Connection = await asyncpg.connect(**await self.to_dict())
        await conn.execute(sql_create_table)
        logging.info('Table has been created successfully.')
        await conn.close()

    async def add_user(self, **kwargs) -> None:
        """
        :param kwargs: list with user data (id, language)
        :returns asyncpg.Record:
        function, which will be register user
        """
        await self.pool.execute(self.COMMANDS['ADD_NEW_USER'], *kwargs.values())

    async def get_user(self, chat_id: int) -> asyncpg.Record:
        """
        :param chat_id: user id
        :returns asyncpg.Record:
        function, which will be return user by id
        """
        return await self.pool.fetchrow(self.COMMANDS['SELECT_USER'], chat_id)

    async def get_user_or_create(self, **kwargs):
        user = await self.get_user(kwargs['chat_id'])
        if user is None:
            await self.add_user(**kwargs)
            user = await self.get_user(kwargs['chat_id'])
        return user

    async def update_user_mails(self, **kwargs) -> asyncpg.Record:
        """
        :param kwargs: dict with user data (id, user_pc)
        :returns asyncpg.Record:
        function, which will be updating user pc
        """
        return await self.pool.execute(self.COMMANDS['UPDATE_USER_MAILS'], kwargs['mails'], kwargs['chat_id'])

    async def get_user_mails(self, **kwargs) -> str:
        """
        :param kwargs: dict with user data (id, language and etc)
        :returns asyncpg.Record:
        function, which will return user pc
        """
        user = await self.get_user_or_create(**kwargs)
        return user.get('mails') if user is not None and user.get('mails') is not None else '[]'

    async def delete_user_computer(self, **kwargs) -> asyncpg.Record:
        """
        :param kwargs: dict with user data (id, language and etc)
        :returns asyncpg.Record:
        function, which will return user pc
        """
        user_pc: dict = json.loads(await self.get_user_mails(**kwargs))
        if user_pc.get(kwargs['name']) is not None:
            del user_pc[kwargs['name']]
            await self.update_user_mails(**{'chat_id': kwargs['chat_id'], 'mails': json.dumps(user_pc)})

        return await self.get_user(kwargs['chat_id'])


async def create_db(database: DBSession):
    """
    :param database: exemplar DBSession
    :returns None:
    function, which will be create sql database
    """
    with open(database.path + 'db/create_db.sql', 'r') as sql_file:
        sql_create_db = sql_file.read()
    conn: asyncpg.Connection = await asyncpg.connect(**await database.to_dict(extra_keys=['database']))
    try:
        await conn.execute(sql_create_db)
        logging.info('DataBase has been created successfully.')
    except asyncpg.exceptions.DuplicateTableError as err:
        logging.info(err)
    await conn.close()


async def create_pool(**kwargs) -> DBSession:
    """
    :param kwargs: data for connect to database
    :returns None:
    function, which will return DBSession
    """
    db = DBSession(**kwargs)
    await db.start()
    await asyncio.sleep(10)
    return db
