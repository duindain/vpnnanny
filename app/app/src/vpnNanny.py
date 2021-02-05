import os
import databases
import sqlalchemy
from sqlalchemy.sql import exists
from sqlalchemy.sql import func
from sqlalchemy.sql import asc
from . import file_helper
from . import database_helper
from starlette.config import Config

# Configuration from environment variables or '.env' file.
config = Config('.env')

if has_vpns():
    activeVpn = active_vpn()
else:
    print("Database is empty, scanning for vpn scripts")
    populate_table()
    activeVpn = active_vpn()

if activeVpn is not null:
    (evaluated_usage, activeVpn) = evaluate_usage(activeVpn)
    if evaluated_usage.action == 'keep':
        activeVpn.score++;
        record_usage(activeVpn)
    else:
        activeVpn.score--;
        rotate_or_remove_vpn(activeVpn)

async def populate_table():
    vpnScriptPaths = get_filepaths(config('VPNPath'), config('VPNFileExtension'))
    for f in vpnScriptPaths:
        print(f)
        upsert_vpn({'id':0, 'name':os.path.basename(f), 'path':f});

async def record_usage(activeVpn):
    upsert_active_vpn({'id':activeVpn.id, 'path':activeVpn.path, 'score':activeVpn.score, 'upload':activeVpn.upload, 'download':activeVpn.download, 'smallDownloadCount':activeVpn.smallDownloadCount, 'onlyUploadCount':activeVpn.onlyUploadCount})

async def evaluate_usage(activeVpn):
    # run vpn stats script
    results = subprocess.run('./vpnUsage.sh', shell=True, universal_newlines=True, check=True)
    print(results.stdout)
    evaluated_usage = {'upload':50, 'download':75, 'score':5, 'action':''}
    if evaluated_usage.upload > 5 && evaluated_usage.download == 0:
        activeVpn.onlyUploadCount++;
        if activeVpn.onlyUploadCount >= 3:
            evaluated_usage.action = 'rotate'
        else:
            evaluated_usage.action = 'keep'
    else if evaluated_usage.download > 5 && evaluated_usage.download < 10:
        activeVpn.smallDownloadCount++;
        if activeVpn.smallDownloadCount >= 3:
            evaluated_usage.action = 'rotate'
        else:
            evaluated_usage.action = 'keep'
    else:
        evaluated_usage.action = 'keep'

    activeVpn.upload += evaluated_usage.upload
    activeVpn.download += evaluated_usage.download
    return (evaluated_usage, activeVpn)

async def rotate_or_remove_vpn(activeVpn):
    upsert_vpn({'id':activeVpn.id, 'score':activeVpn.score, 'upload':activeVpn.upload, 'download':activeVpn.download})
    clear_active_vpn()
    if activeVpn.score <= 3:
        # retire script
        results = subprocess.run('./retireActiveVpn.sh ' + activeVpn.path, shell=True, universal_newlines=True, check=True)
        print(results.stdout)
    activeVpn = active_vpn()
    results = subprocess.run('./activateActiveVpn.sh ' + activeVpn.path, shell=True, universal_newlines=True, check=True)
    print(results.stdout)
