import asyncpg
import json
from config_data.config import Config, load_config
import asyncio

config: Config = load_config()

async def prepare_database() -> None:
    print("CONF")
    conn = await asyncpg.connect(
        "postgresql://{}:{}@{}/{}".format(
            config.db_config.username, 
            config.db_config.password,
            config.db_config.host, 
            config.db_config.dbname
        )
    )
    await conn.set_type_codec(
            'json',
            encoder=json.dumps,
            decoder=json.loads,
            schema='pg_catalog'
        )
    try:
        await conn.execute('''
            CREATE TABLE properties(
                    cid serial,
                    data json
            )
        ''')
    except:
        pass

# async def main():
#     await prepare_database()

# asyncio.run(main())