import redis

# the database class using Redis
# Redis is a lightwieght database framework primarly holding data as key:value pairs in memory rather than disk
# disk writing is available if you want to provided using the appendonlyfile .aof
# memory file listed as the dum.rdp
# this uses static only methods to maintain a single connection at a time and there doesn't need to be more than one instance of the class during operation
# thje class will utilize basic CRUD operations and the primary objects to hold will be pathing data and Pi status via timestamps

class database:
    
    @staticmethod
    def startCon():
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)

    def grab(key):
        # method to pull a key from memory store
        pass
    def appendTo(key,value):
        pass
        # add a value to a key

    def writeTo(key):
        pass
        # write to disk
    def remove(key):
        pass
        # remove a key from the file
    def update(key,value,new_val):
        pass
        # update a value in a key


