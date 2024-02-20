# eto-mysql-databaselib

# OK SO MOST IMPORTANT THING, IF YOU WANNA USE THIS LIB YOU NEED TO HAVE A MYSQL DATABASE ONLINE,THEN, THE MOST IMPORTANT STUFF TO DO IS THIS ( IF YOU DON'T DO THIS AND TRY TO USE ANY OTHER THING IN THE PACKAGE, IT WILL NOT WORK, SINCE THE basemysqldatabaselib module IS THE BASE MODULE OF THE PROJECT, EVERYTHING DEPENDS ON IT ):


```py
    from databaselib import basemysqldatabaselib, databaseAbstractions

    basemysqldatabaselib.database = basemysqldatabaselib.Database("your host here", "your database username here", "your database password here", "your database name here")
    basemysqldatabaselib.conn = basemysqldatabaselib.connect()
```