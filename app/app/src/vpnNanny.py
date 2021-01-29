import databases
import sqlalchemy
from sqlalchemy.sql import exists
from sqlalchemy.sql import func
from sqlalchemy.sql import asc
from . import file_helper
from . import database_helper

# Configuration from environment variables or '.env' file.
config = Config('.env')

if has_vpns():
    activeVpn = active_vpn()
else if
    print("Database is empty, scanning for vpn scripts")
    populate_table()

async def populate_table():
    vpnScriptPaths = get_filepaths(config('VPNPath'), config('VPNFileExtension'))
    for f in vpnScriptPaths:
        print(f)
