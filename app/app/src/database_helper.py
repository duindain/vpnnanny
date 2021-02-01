import databases
import sqlalchemy
from sqlalchemy.sql import exists
from sqlalchemy.sql import func
from sqlalchemy.sql import asc
from sqlalchemy import func

# Configuration from environment variables or '.env' file.
config = Config('.env')
DATABASE_URL = config('DATABASE_URL')

# Database table definitions.
metadata = sqlalchemy.MetaData()

vpns = sqlalchemy.Table(
    "vpns",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("name", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("path", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("score", sqlalchemy.Integer, default=0),
    sqlalchemy.Column("upload", sqlalchemy.Float, default=0),
    sqlalchemy.Column("download", sqlalchemy.Float, default=0),
    sqlalchemy.Column("createdOn", sqlalchemy.DateTime(timezone=True), server_default=func.now()),
    sqlalchemy.Column("updatedOn", sqlalchemy.DateTime(timezone=True), onupdate=func.now()),
)

activeVpn = sqlalchemy.Table(
    "activeVpn",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("vpnid", sqlalchemy.Integer, nullable=False),
    sqlalchemy.Column("score", sqlalchemy.Integer, default=0),
    sqlalchemy.Column("upload", sqlalchemy.Float, default=0),
    sqlalchemy.Column("download", sqlalchemy.Float, default=0),
    sqlalchemy.Column("smallDownloadCount", sqlalchemy.Integer, default=0),
    sqlalchemy.Column("onlyUploadCount", sqlalchemy.Integer, default=0),
    sqlalchemy.Column("createdOn", sqlalchemy.DateTime(timezone=True), server_default=func.now()),
    sqlalchemy.Column("updatedOn", sqlalchemy.DateTime(timezone=True), onupdate=func.now()),
)

database = databases.Database(DATABASE_URL)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)

async def populate_table():
    vpnScriptPaths = get_filepaths(config('VPNPath'), config('VPNFileExtension'))
    for f in vpnScriptPaths:
        print(f)

async def upsert_vpn(data):
    vpn = vpns.query.filter_by(id == data['id']).first() if data['id'] > 0 else null
    if vpn == null:
        query = vpns.insert().values(
           name=data["name"],
           path=data["path"])
    else:
       query = vpns.update().values(
           score=data["score"],
           upload=data["upload"],
           download=data["download"]).where(id == vpn.id)

    await database.execute(query)
    return True

async def upsert_active_vpn(data):
    currentVpn = activeVpn.query.filter_by(id == data['id']).first() if data['id'] > 0 else null
    if currentVpn == null:
        query = activeVpn.insert().values(
           name=data["name"],
           vpnid=data['vpnid'])
    else:
       query = activeVpn.update().values(
           score=data["score"],
           upload=data["upload"],
           download=data["download"],
           smallDownloadCount=data["smallDownloadCount"],
           onlyUploadCount=data["onlyUploadCount"]).where(id == currentVpn.id)

    await database.execute(query)
    return True

async def get_vpns():
    query = vpns.select().order_by(asc(vpns.c.updatedOn))
    results = await database.fetch_all(query)
    content = [
        {
            column_name: column_value
        }
        for row in results
            for column_name, column_value in row.items()
    ]
    return content

async def has_vpns():
    return database.query(vpns).first() is not None

async def active_vpn():
    currentVpn = database.query(activeVpn).first()
    if currentVpn is None
        currentVpn = get_random_vpn
        upsert_active_vpn({'id'=> 0, 'vpnid'=>currentVpn.id})
        return await active_vpn()
    return currentVpn

async def get_random_vpn():
    stmt = database.query(vpns).order_by(func.random())
    return stmt.first()

async def clear_active_vpn():
    database.query(activeVpn).truncate()
