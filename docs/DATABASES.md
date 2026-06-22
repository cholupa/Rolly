---
layout: page
title: Database Enhancement
---

# Databases

## Original Artifact
  
  There was no original artifact for this enhancement. No previous project seemed to fit the bill in how I wanted the database to work in this project. The database needed be lightweight, with only a few needed functions. The modeling for previous projects also would not make sense for the current project due to becoming too complex for saving only a few values. Because of this, this is from the ground up enhancement/creation. The database used is Redis, which is and is not an actual database schema. The basis of redis is to only have objects stored mainly in RAM and write to the disk occasionally if wanted or necessary.

## Enhancement

  I decided to create this enhancement from scratch because the whole project is almost completely from scratch. The previous enhancements did have some conceptual aspect to work off of, but this is a new component to the project. Essentially this database is a single Python file that contains a few methods to create, delete, and read records. There is no update involved in this to maintain simplicity with the system, but possibly be implemented in the future. Using Redis was a good choice instead of an SQL schema or MongoDB. Mainly it is because of performance and space. MongoDB would have been the alternative choice because of the document design you can do with it, but Redis already does this as well within basic structures and little overhead on storage.

  > The CREATE method for adding in a new step to the path
```python
@staticmethod
    def create(con, pathNum, stepNum, distance, turn, stamp):
        key = f'P{pathNum}:S{stepNum}'
        con.hset(key,mapping={f'step:{stepNum}':stepNum,'distance':distance,'turn':turn, 'timestamp':stamp})
        con.set(f'P{pathNum}:latest', stepNum)
        con.sadd('INDEX', key)
        return con.hgetall(key)
```



## Outcome

  As simple databases are in concept, they are a difficult software to become efficient in. I believe in this enhancement I was able to develop code that is on par with best practices and maintaining adequate security. The Redis software is a perfect tool for this type of project and I maintained security by keeping a separation of concerns with database interactions. The simplest security is to prevent injections by never hardcoding values. It is also because this project is a local project on a physical device, there is inherent security in actually having hands on the product.
 
  As always with a project, learning new frameworks is a grinding process. I was constantly rereading documentation and dealing with errors in setting up the data in the creation side of the records for Redis. It is actually very simple but sometimes when these things are deceptively easy, they can be tough at times. That was the main challenge encountered and it has been overcome. There’s plenty more to learn from using Redis, but I do not know if any more is strictly necessary in this project. Any more work will be a combination of the algorithm of pathfinding and altering how the data is added. I did learn that database work is especially difficult at first, but it is one of those things where it needs to be hammered into the brain.
