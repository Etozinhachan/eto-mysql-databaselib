# eto-mysql-databaselib

# OK SO MOST IMPORTANT THING, IF YOU WANNA USE THIS LIB YOU NEED TO HAVE A MYSQL DATABASE ONLINE,THEN, THE MOST IMPORTANT STUFF TO DO IS THIS ( IF YOU DON'T DO THIS AND TRY TO USE ANY OTHER THING IN THE PACKAGE, IT WILL NOT WORK, SINCE THE basemysqldatabaselib module IS THE BASE MODULE OF THE PROJECT, EVERYTHING DEPENDS ON IT ):


```py
def main():
    from databaselib import basemysqldatabaselib, databaseAbstractions

    basemysqldatabaselib.database = basemysqldatabaselib.Database("your host here", "your database username here", "your database password here", "your database name here")
    basemysqldatabaselib.conn = basemysqldatabaselib.connect()
    

if __name__ == "__main__":
    main()
```


## LIBRARY USAGE EXAMPLES

Register example

```py

from databaselib import basemysqldatabaselib, databaseAbstractions
from databaselib.databaseDevFriendlyAbstraction import User

def main():
    
    basemysqldatabaselib.database = basemysqldatabaselib.Database("your host here", "your database username here", "your database password here", "your database name here")
    basemysqldatabaselib.conn = basemysqldatabaselib.connect()
    
    username:str = input("Insert your username: ")
    password:str = input("Insert your password: ")
    
    user:User = databaseAbstractions.registerUser(username, password)
    
    if user == None:
        print("User with that username already exists!")
        return
    
    print(user)

if __name__ == "__main__":
    main()
```

Login example

```py

from databaselib import basemysqldatabaselib, databaseAbstractions
from databaselib.databaseDevFriendlyAbstraction import User

def main():    

    basemysqldatabaselib.database = basemysqldatabaselib.Database("your host here", "your database username here", "your database password here", "your database name here")
    basemysqldatabaselib.conn = basemysqldatabaselib.connect()
    
    username:str = input("Insert your username: ")
    password:str = input("Insert your password: ")
    
    user:User = databaseAbstractions.loginUser(username, password)
    
    if user == None:
        print("Wrong password!")
        return
    
    print(user)

if __name__ == "__main__":
    main()

```

User edit example

```py
    
from databaselib import basemysqldatabaselib, databaseAbstractions
from databaselib.databaseDevFriendlyAbstraction import User

def main():
    basemysqldatabaselib.database = basemysqldatabaselib.Database("your host here", "your database username here", "your database password here", "your database name here")
    basemysqldatabaselib.conn = basemysqldatabaselib.connect()
    
    username:str = input("Insert your username: ")
    password:str = input("Insert your password: ")
    
    user:User = databaseAbstractions.loginUser(username, password)
    
    if user == None:
        print("Wrong password!")
        return
    
    print(user)

    new_username:str = input("Insert your new username")
    new_password:str = input("Insert your new password")

    # edits both the username and the password
    edited_user = databaseAbstractions.editUser(user, new_username, new_password)

    if edited_user == None:
        print("Something went wrong while editing the user!")
        return
    
    print(edited_user)
    # only edits the username
    #edited_user = databaseAbstractions.editUser(user, new_username=new_username)
    
    # only edits the password
    #edited_user = databaseAbstractions.editUser(user, new_password=new_password)

if __name__ == "__main__":
    main()
```

OR

```py

from databaselib import basemysqldatabaselib, databaseAbstractions
from databaselib.databaseDevFriendlyAbstraction import User

def main():
    basemysqldatabaselib.database = basemysqldatabaselib.Database("your host here", "your database username here", "your database password here", "your database name here")
    basemysqldatabaselib.conn = basemysqldatabaselib.connect()
    
    username:str = input("Insert your username: ")
    password:str = input("Insert your password: ")
    
    user:User = databaseAbstractions.loginUser(username, password)
    
    if user == None:
        print("Wrong password!")
        return
    
    print(user)

    new_username:str = input("Insert your new username ( it needs to be different than the current one ): ")
    new_password:str = input("Insert your new password ( it needs to be different than the current one ): ")

    # edits the username
    user.username = new_username

    if new_username == username:
        print("Something went wrong while editing the user's username!")
        return

    # edits the password
    user.password = new_password

    if new_password == password:
        print("Something went wrong while editing the user's password!")
        return
    
    print(user)
if __name__ == "__main__":
    main()

```