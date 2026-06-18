import redis

# the database class using Redis
# Redis is a lightwieght database framework primarly holding data as key:value pairs in memory rather than disk
# disk writing is available if you want to provided using the appendonlyfile .aof
# memory file listed as the dum.rdp
# this uses static only methods to maintain a single connection at a time and there doesn't need to be more than one instance of the class during operation
# thje class will utilize basic CRUD operations and the primary objects to hold will be pathing data and Pi status via timestamps

class database:

    writable = False
    
    @staticmethod
    def startCon():
        try:
            r = redis.Redis(host='localhost', port=6379, decode_responses=True)
            print("Connected to redis Server")
            return r
        except:
            print("Unable to connect")
    
    @staticmethod
    def create(con, pathNum, stepNum, distance, turn, stamp):
        key = f'P{pathNum}:S{stepNum}'
        con.hset(key,mapping={f'step:{stepNum}':stepNum,'distance':distance,'turn':turn, 'timestamp':stamp})
        con.set(f'P{pathNum}:latest', stepNum)
        con.sadd('INDEX', key)
        return con.hgetall(key)
    
    @staticmethod
    def getLatest(con, pathNum):
        latest = con.get(f'P{pathNum}:latest')
        if not latest:
            return None
        return con.hgetall(f'P{pathNum}:S{latest}')

    # get a specific path using path number and step number
    @staticmethod
    def read(con, pathNum, stepNum=None):
        if stepNum is not None:
            return con.hget(f'P{pathNum}:S{stepNum}')
        else:
            keys = con.smembers('INDEX')
            fullPath = [k for k in keys if k.startswith(f'P{pathNum}:'}]
            return {key: con.hgetall(key) for key in sorted(fullPath)}
    
    # delete a key from the db, two deletes must hapopen since the data and key are stored differently
    @staticmethod
    def delete(con, key):
        if con.exists(key):
            con.delete(key)
            con.srem('INDEX',key)

    


