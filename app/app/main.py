from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
import databases
import sqlalchemy
from starlette.config import Config
from starlette.routing import Route
from sqlalchemy.sql import exists
from sqlalchemy.sql import func
from sqlalchemy.sql import asc
import file_helper

# Configuration from environment variables or '.env' file.
config = Config('.env')
DATABASE_URL = config('DATABASE_URL')
VPN_DIR = config('VPNPath')

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

database = databases.Database(DATABASE_URL)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)

if database.query(vpns).first() is None:


async def list_vpns(request):
    query = vpns.select().order_by(asc(vpns.c.updatedOn))
    results = await database.fetch_all(query)
    content = [
        {
            column_name: column_value
        }
        for row in results
            for column_name, column_value in row.items()
    ]
    return JSONResponse(content)

async def add_vpn(request):
    data = await request.json()

    vpn = vpns.query.filter_by(id == data['id']).first()
    if vpn == null:
        query = vpns.insert().values(
           name=data["name"],
           path=data["path"],
           score=data["score"],
           upload=data["upload"],
           download=data["download"]
           )
    else:
       query = vpns.update().values(
           score=data["score"],
           upload=data["upload"],
           download=data["download"]).where(id == vpn.id)

    await database.execute(query)
    return JSONResponse({
        "completed": True
    })

async def populate_table():
    vpnScriptPaths = get_filepaths(config('VPNPath'), config('VPNFileExtension'))
    for f in vpnScriptPaths:
        print f

routes = [
    #Mount('/', app=StaticFiles(directory='/app/app/src/site/index.html'), name="index"),
    Mount('/site', app=StaticFiles(directory='/app/app/src/site'), name="site"),
    Route("/vpns", endpoint=list_vpns, methods=["GET"]),
    Route("/vpn", endpoint=add_vpn, methods=["POST"]),
]

app = Starlette(
    debug=True,
    routes=routes,
    on_startup=[database.connect],
    on_shutdown=[database.disconnect]
)
