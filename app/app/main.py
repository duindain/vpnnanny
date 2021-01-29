from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
import databases
import sqlalchemy
from starlette.config import Config
from starlette.routing import Route
from ./src/ import database_helper

async def list_vpns(request):
    return JSONResponse(await get_vpns())

async def add_vpn(request):
    data = await request.json()

    return JSONResponse({
        "completed": await upsert_vpn(data)
    })

routes = [
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
