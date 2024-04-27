import databaselib.etodatabaselib as mycooldatabase
import databaselib.etohashlib as mycoolhashlib

idColumnName = "id"
usernameColumnName = "username"
passwordColumnName = "password"
saltColumnName = "salt"
usersTableName = "users"

class User():
    def __init__(self, id:int, username:str, password_hashed:str):
        
        self._id = id
        self._username = username
        self._password = password_hashed

    def __repr__(self):

        return f"\nUser Info:\n{"":->20}\nId: {self.id}\nUsername: {self.username}\nPassword: {self.password}\n{"":->20}"

    # Getters

    @property
    def id(self):
        return self._id
    
    @property
    def username(self):
        return self._username
    
    @property
    def password(self):
        return self._password
    
    # Setters

    @username.setter
    def username(self, new_username):
        
        editionSucceeded:bool = mycooldatabase.edit_rows(usersTableName, {f"{usernameColumnName}": f"{new_username}"}, f"{idColumnName} = {self.id}", [f"{usernameColumnName}"])
        if editionSucceeded:
            self._username = new_username

    @password.setter
    def password(self, new_password):
        (hashed_password, salt) = mycoolhashlib.generateSaltHash(new_password)
        editionSucceeded:bool = mycooldatabase.edit_rows(usersTableName, {f"{passwordColumnName}": f"{hashed_password}", f"{saltColumnName}": f"{salt}"}, f"{idColumnName} = {self.id}")
        #print(editionSucceeded)
        if editionSucceeded:
            self._password = hashed_password

class LoginError(Exception):
   pass


def userExists(username: str) -> bool:
    usernameColumnResults = mycooldatabase.get_rows(usersTableName, [f"{usernameColumnName}"])
    dictionaryToCompare = {f"{usernameColumnName}": f"{username}"}
    if usernameColumnResults == None:
        return False
    if not dictionaryToCompare in usernameColumnResults:
        return False
    return True

def registerUser(username:str, password:str) -> User:
    try:
        global usernameColumnName
        global passwordColumnName
        global usersTableName
        global saltColumnName
        (hashed_password, salt) = mycoolhashlib.generateSaltHash(password)
        mycooldatabase.createTable(usersTableName, {f"{idColumnName}": "INT PRIMARY KEY NOT NULL AUTO_INCREMENT", f"{usernameColumnName}": "VARCHAR(100) NOT NULL", f"{passwordColumnName}": "VARCHAR(150) NOT NULL", f"{saltColumnName}": "VARCHAR(150) NOT NULL"}, True)

        rows_inserted:bool = mycooldatabase.insert_rows(usersTableName, {f"{usernameColumnName}": f"{username}", f"{passwordColumnName}": f"{hashed_password}", f"{saltColumnName}": f"{salt}"}, [f"{usernameColumnName}"])
        if rows_inserted:
            notStructuredUser = mycooldatabase.get_rows(usersTableName, [f"{idColumnName}", f"{usernameColumnName}", f"{passwordColumnName}"], f"{usernameColumnName} = '{username}'")  
            notStructuredUser = notStructuredUser[0]

            return User(notStructuredUser.get(f'{idColumnName}'), notStructuredUser.get(f'{usernameColumnName}'), notStructuredUser.get(f'{passwordColumnName}'))
        return None
    except ValueError:
        #print('rawr')
        pass

def loginUser(username:str, password:str) -> User:
    try:
        global usernameColumnName
        global passwordColumnName
        global usersTableName
        global saltColumnName
        if not userExists(username):
            return None
        passwordSalt = mycooldatabase.get_rows(usersTableName, [f"{passwordColumnName}", f"{saltColumnName}"], f"{usernameColumnName} = '{username}'")
        if passwordSalt == None:
            return None
        usablePasswordSalt = passwordSalt[0]

        if mycoolhashlib.checkPassword(usablePasswordSalt.get(f'{passwordColumnName}'), password, usablePasswordSalt.get(f'{saltColumnName}')):
            notStructuredUser = mycooldatabase.get_rows(usersTableName, [f"{idColumnName}", f"{usernameColumnName}", f"{passwordColumnName}"], f"{usernameColumnName} = '{username}'")
            
            notStructuredUser = notStructuredUser[0]

            return User(notStructuredUser.get(f'{idColumnName}'), notStructuredUser.get(f'{usernameColumnName}'), notStructuredUser.get(f'{passwordColumnName}'))
        return None
    except ValueError:
        #print('login rawr :c')
        pass

def editUser(user_to_update:User, new_username:str = None, new_password:str = None) -> User:
    try:
        if not userExists(user_to_update.username):
            return None
        if new_username == None and new_password == None:
            return user_to_update
        
        username_column_update_string = None if new_username == None else usernameColumnName
        username_value_update_string = None if new_username == None else new_username

        password_column_update_string = None if new_password == None else passwordColumnName
        password_value_update_string = None if new_password == None else new_password
        (hashed_password, salt) = (None, None)
        salt_column_update_string = None
        if not password_column_update_string == None:
            (hashed_password, salt) = mycoolhashlib.generateSaltHash(password_value_update_string)
            salt_column_update_string = saltColumnName

        edition_suceedeed = mycooldatabase.edit_rows(usersTableName, {username_column_update_string: username_value_update_string, password_column_update_string: hashed_password, salt_column_update_string: salt}, f"{idColumnName} = {user_to_update.id}", [f"{usernameColumnName}"])
        if edition_suceedeed:
            notStructuredUser = mycooldatabase.get_rows(usersTableName, [f"{idColumnName}", f"{usernameColumnName}", f"{passwordColumnName}"], f"{idColumnName} = '{user_to_update.id}'")  
            notStructuredUser = notStructuredUser[0]

            return User(notStructuredUser.get(f'{idColumnName}'), notStructuredUser.get(f'{usernameColumnName}'), notStructuredUser.get(f'{passwordColumnName}'))
        return None
    except ValueError:
        #print('edit rawr :c')
        pass