Database Enhancement
  There was no original artifact for this enhancement. No previous project seemed to fit the bill in how I wanted the database to work in this project. The database should be lightweight, with only a few needed functions. The modeling for previous projects also would not make sense for the current project due to becoming too complex for saving only a few values. Because of this, this is from the ground up enhancement/creation. The database used is Redis, which is and is not an actual database schema. The basis of redis is to only have objects stored mainly in RAM and write to the disk occasionally if wanted or necessary.
  I decided to create this enhancement from scratch because the whole project is almost completely from scratch. The previous enhancements did have some conceptual aspect to work off of, but this is a new component to the project. Essentially this database is a single Python file that contains a few methods to create, delete, and read records. There is no update involved in this to maintain simplicity with the system, but possibly be implemented in the future. Using Redis was a good choice instead of an SQL schema or MongoDB. Mainly it is because of performance and space. MongoDB would have been the alternative choice because of the document design you can do with it, but Redis already does this as well within basic structures and little overhead on storage.
  The original plan for the database was to store mapping routes on objects from the echo sensor, but now it is more of a holder for paths of travel from the robot class. The structure is a key:value pair capable of having “nested” values via formatted strings. In this respect I have completed the task I had in mind, but there is still much to do. 
```
Connected to redis Server
Current Step 1
idle
Connected
Current Step 1
sensing
Entering moving Forward
forward
reading distance: 39.220523834228516
reading distance: 39.23279047012329
reading distance: 38.82390260696411
reading distance: 39.20416831970215
reading distance: 39.20007944107056
reading distance: 39.20007944107056
reading distance: 39.20007944107056
reading distance: 39.245057106018066
reading distance: 39.085590839385986
reading distance: 39.220523834228516
reading distance: 39.20416831970215
reading distance: 39.245057106018066
reading distance: 38.766658306121826
reading distance: 104.8265814781189
reading distance: 104.99831438064575
reading distance: 39.216434955596924
reading distance: 29.709792137145996
reading distance: 104.88791465759277
reading distance: 104.88382577896118
reading distance: 104.91653680801392
reading distance: 29.41948175430298
reading distance: 105.24773597717285
reading distance: 32.31849670410156
reading distance: 104.79387044906616
reading distance: 104.80204820632935
reading distance: 59.52180624008179
reading distance: 50.61622858047485
reading distance: 104.7775149345398
reading distance: 42.85144805908203
reading distance: 104.76933717727661
reading distance: 35.96986532211304
reading distance: 34.67777967453003
reading distance: 33.348894119262695
reading distance: 30.51121234893799
reading distance: 29.21912670135498
reading distance: 29.44401502609253
reading distance: 29.182326793670654
reading distance: 31.545698642730713
reading distance: 29.99192476272583
reading distance: 29.472637176513672
reading distance: 29.44401502609253
reading distance: 30.257701873779297
reading distance: 23.633718490600586
Current Step 1
moving
STOPPING
Current Step 1
FORWARD
packaction returned - turn0, distance - 23.633718490600586
23.633718490600586
0
Current Step 2
idle
Current Step 2
sensing
Current Step 2
sweeping
Entering a turn
Current Step 2
turning
Exiting a turn
Entering moving Forward
forward
reading distance: 48.95205497741699
reading distance: 43.91864538192749
reading distance: 104.76115942001343
reading distance: 104.83067035675049
reading distance: 49.549031257629395
reading distance: 43.9145565032959
reading distance: 43.53837966918945
reading distance: 43.951356410980225
reading distance: 48.6985445022583
reading distance: 50.06422996520996
reading distance: 50.043785572052
reading distance: 42.91278123855591
reading distance: 42.91278123855591
reading distance: 104.8265814781189
reading distance: 104.83475923538208
reading distance: 43.677401542663574
reading distance: 43.30531358718872
reading distance: 43.28078031539917
reading distance: 43.32166910171509
reading distance: 44.69553232192993
reading distance: 43.12540292739868
reading distance: 45.34975290298462
reading distance: 44.50335502624512
reading distance: 35.96986532211304
reading distance: 35.965776443481445
reading distance: 31.807386875152588
reading distance: 29.99192476272583
reading distance: 28.593528270721436
Current Step 2
moving
STOPPING
Current Step 2
FORWARD
packaction returned - turn0, distance - 28.593528270721436
28.593528270721436
0
Current Step 3
idle
Current Step 3
sensing
Current Step 3
sweeping
blocked
Current Step 3
idle
Current Step 3
sensing
Entering moving Forward
forward
reading distance: 104.69982624053955
reading distance: 50.415873527526855
reading distance: 49.912941455841064
reading distance: 49.87205266952515
reading distance: 49.88023042678833
reading distance: 48.13019037246704
reading distance: 48.57996702194214
reading distance: 48.96841049194336
reading distance: 50.26867389678955
reading distance: 51.826536655426025
reading distance: 50.235962867736816
reading distance: 49.87205266952515
reading distance: 49.8965859413147
reading distance: 49.90885257720947
reading distance: 49.912941455841064
reading distance: 49.87205266952515
reading distance: 104.38498258590698
reading distance: 45.934462547302246
reading distance: 37.14337348937988
reading distance: 31.28809928894043
reading distance: 26.26286745071411
Current Step 3
moving
STOPPING
Current Step 3
FORWARD
packaction returned - turn0, distance - 26.26286745071411
26.26286745071411
0
Current Step 4
idle
Current Step 4
sensing
Current Step 4
sweeping
Entering a turn
Current Step 4
turning
Exiting a turn
Entering moving Forward
forward
Current Step 4
moving
STOPPING
Current Step 4
action packed
packaction returned - turn90, distance - 0
0
90
Current Step 5
idle
Current Step 5
sensing
Current Step 5
sweeping
Entering a turn
Current Step 5
turning
Exiting a turn
Entering moving Forward
forward
reading distance: 35.96168756484985
reading distance: 35.96168756484985
reading distance: 35.98213195800781
reading distance: 35.97804307937622
reading distance: 35.96168756484985
reading distance: 35.97804307937622
reading distance: 36.00257635116577
reading distance: 35.97804307937622
reading distance: 37.127017974853516
reading distance: 36.18248701095581
reading distance: 104.81022596359253
reading distance: 22.488832473754883
Current Step 5
moving
STOPPING
Current Step 5
FORWARD
packaction returned - turn0, distance - 22.488832473754883
22.488832473754883
0
Current Step 6
idle
Current Step 6
sensing
Entering moving Forward
forward
reading distance: 36.194753646850586
reading distance: 36.20293140411377
reading distance: 36.22746467590332
reading distance: 36.17839813232422
reading distance: 36.21928691864014
reading distance: 36.20293140411377
reading distance: 36.21110916137695
reading distance: 36.23155355453491
reading distance: 35.986220836639404
reading distance: 105.2722692489624
reading distance: 21.176302433013916
Current Step 6
moving
STOPPING
Current Step 6
FORWARD
packaction returned - turn0, distance - 21.176302433013916
21.176302433013916
0
Current Step 7
idle
Current Step 7
sensing
Entering moving Forward
forward
reading distance: 35.97804307937622
reading distance: 35.96986532211304
reading distance: 35.98213195800781
reading distance: 36.1375093460083
reading distance: 35.99439859390259
reading distance: 35.95350980758667
reading distance: 35.97395420074463
reading distance: 35.97395420074463
reading distance: 36.010754108428955
reading distance: 35.93306541442871
reading distance: 35.986220836639404
reading distance: 36.90212965011597
reading distance: 32.87867307662964
reading distance: 36.21110916137695
Current Step 7
moving
STOPPING
Current Step 7
FORWARD
packaction returned - turn0, distance - 36.21110916137695
36.21110916137695
0
Current Step 8
idle
Current Step 8
sensing
Entering moving Forward
forward
reading distance: 36.19884252548218
reading distance: 35.16026735305786
reading distance: 31.271743774414062
reading distance: 35.72044372558594
reading distance: 34.416091442108154
reading distance: 23.64189624786377
reading distance: 37.84257173538208
reading distance: 36.215198040008545
Current Step 8
moving
STOPPING
Current Step 8
FORWARD
packaction returned - turn0, distance - 36.215198040008545
36.215198040008545
0
Current Step 9
idle
Current Step 9
sensing
Entering moving Forward
forward
reading distance: 29.14961576461792
reading distance: 29.190504550933838
reading distance: 35.95759868621826
reading distance: 35.99439859390259
reading distance: 35.98213195800781
reading distance: 21.84278964996338
reading distance: 22.648298740386963
reading distance: 35.97804307937622
reading distance: 35.945332050323486
reading distance: 21.52385711669922
Current Step 9
moving
STOPPING
Current Step 9
FORWARD
packaction returned - turn0, distance - 21.52385711669922
21.52385711669922
0
Current Step 10
idle
Current Step 10
sensing
Entering moving Forward
forward
reading distance: 33.10356140136719
reading distance: 29.73841428756714
reading distance: 32.33485221862793
reading distance: 31.26765489578247
reading distance: 30.224990844726562
reading distance: 30.01236915588379
reading distance: 29.98783588409424
reading distance: 26.136112213134766
reading distance: 35.97395420074463
reading distance: 35.990309715270996
reading distance: 35.98213195800781
reading distance: 35.97395420074463
reading distance: 35.96168756484985
reading distance: 35.96986532211304
Current Step 10
moving
STOPPING
Current Step 10
FORWARD
packaction returned - turn0, distance - 35.96986532211304
35.96986532211304
0
Current Step 11
{'step:2': '2', 'distance': '23.633718490600586', 'turn': '0', 'timestamp': 'Jun 21 17:11:05'}

```
  I have met the outcome of using standard techniques in implementing the database by creating a class to contain the basic functions necessary. The main database functions used are create and read. Delete and update are almost unnecessary in this instance because of how the interface is with the robot. Anything that isn’t needed can be plain removed by console. But, the read and create are finished and operate with a separation from the main file which is a best practice of separation of concerns. The data itself is only a few floats and integers that are fed to the server in intervals of steps taken by the robot, which the server does not need any more information than that. More work is needed to clean up the code a little bit, but the fundamentals are there.
  As always with a project, learning new frameworks is a grinding process. I was constantly rereading documentation and dealing with errors in setting up the data in the creation side of the records for Redis. It is actually very simple but sometimes when these things are deceptively easy, they can be tough at times. That was the main challenge encountered and it has been overcome. There’s plenty more to learn from using Redis, but I do not know if any more is strictly necessary in this project. Any more work will be a combination of the algorithm of pathfinding and altering how the data is added. I did learn that database work is especially difficult at first, but it is one of those things where it needs to be hammered into the brain.
