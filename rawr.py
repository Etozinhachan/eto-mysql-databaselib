    
from databaselib import basemysqldatabaselib, databaseAbstractions
from databaselib.databaseDevFriendlyAbstraction import User

def main():
    basemysqldatabaselib.database = basemysqldatabaselib.Database("sql.freedb.tech", "freedb_SaDev", "h2@#Rz5SncUJ?QK", "freedb_coolDb")
    basemysqldatabaselib.conn = basemysqldatabaselib.connect()
    
    username:str = input("Insert your username: ")
    password:str = input("Insert your password: ")
    
    user:User = databaseAbstractions.loginUser(username, password)
    
    if user == None:
        print("Wrong password!")
        return
    
    print(user)

    new_username:str = input("Insert your new username: ")
    new_password:str = input("Insert your new password: ")

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