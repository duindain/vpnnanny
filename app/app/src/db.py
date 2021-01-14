import sqlite3
from sqlite3 import Error

class Vpn:
    def __init__(self, id, name, file, score, upload, download, lastUsed, updatedOn, createdOn):
        self.id, self.name, self.file, self.score, self.upload, self.download, self.lastUsed, self.updatedOn, self.createdOn = id, name, file, score, upload, download, lastUsed, updatedOn, createdOn

def adapt_point(point):
    return "%f;%f" % (point.x, point.y)

def create_connection:
    """ create a database connection to the SQLite database
        specified by the db_file
        :param db_file: database file
        :return: Connection object or None
    """
    connection = None
    try:
        connection = sqlite3.connect('vpnNanny.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        # Access columns by index or name
        connection.row_factory = sqlite3.Row
    except Error as e:
        print(e)

    return conn

def getVpns():
    """
    get all vpns ordered by updatedOn
    :param conn:
    :param task:
    :return: project id
    """
    connection = getConnection()
    cur = conn.cursor()
    cur.executeMany("select * from Vpns ORDER BY updatedOn DESC")
    connection.close()

def upsert_task(vpn):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """

    sql = ''' insert into vpns (id, name, file, score, upload, download, lastUsed, updatedOn)
              values (?,?,?,?,?,?,?,(datetime('now','localtime'))
              On CONFLICT(name)
              DO UPDATE
              SET id=? name=?, file=?, score=?, upload=?, download=?, lastUsed=?, updatedOn=(datetime('now','localtime')'''
    connection = getConnection()
    cur = conn.cursor()
    cur.execute(sql, vpn)
    connection.commit()
    connection.close()

def createDb():
    """
    create table for Vpn if it doesnt already exist
    :param conn:
    :return: project id
    """
    connection = getConnection()
    c = conn.cursor()

    # Create table
    c.execute('''
        CREATE TABLE IF NOT EXISTS vpns
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name text NOT NULL UNIQUE,
            file TEXT NOT NULL UNIQUE,
            score integer DEFAULT 0,
            upload real DEFAULT 0,
            download real DEFAULT 0,
            lastUsed date,
            createdOn date DEFAULT (datetime('now','localtime'),
            updatedOn date DEFAULT (datetime('now','localtime')
        )''')

    connection.close()
