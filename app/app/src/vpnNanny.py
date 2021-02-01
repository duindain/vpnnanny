import os
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
    activeVpn = active_vpn()

if activeVpn is not null
    (evaluated_usage, activeVpn) = evaluate_usage(activeVpn)
    record_usage(activeVpn)

async def populate_table():
    vpnScriptPaths = get_filepaths(config('VPNPath'), config('VPNFileExtension'))
    for f in vpnScriptPaths:
        print(f)
        upsert_vpn({'id'=> 0, 'name'=>os.path.basename(f), 'path'=>f, 'score'=>0, 'upload'=>0, 'download'=>0});

async def record_usage(activeVpn):
    upsert_vpn({'id'=> activeVpn.id, 'score'=>activeVpn.score, 'upload'=>activeVpn.upload, 'download'=>activeVpn.download})

async def evaluate_usage(activeVpn):
    # run vpn stats script
    evaluated_usage = {'upload'=>50, 'download'=>75, 'score'=>5, 'state'=>empty}
    if evaluated_usage.upload > 5 && evaluated_usage.download == 0:
        evaluated_usage.state = onlyUpload
        activeVpn.score++;
    else if evaluated_usage.download > 5 && evaluated_usage.download < 10:
        evaluated_usage.state = smallDownload
        activeVpn.score++;
    else if evaluated_usage.download > 10:
        evaluated_usage.state = normalDownload
        activeVpn.score++;
    else
        evaluated_usage.state = swap
        activeVpn.score--;

    activeVpn.upload += evaluated_usage.upload
    activeVpn.download += evaluated_usage.download
    return (evaluated_usage, activeVpn)
