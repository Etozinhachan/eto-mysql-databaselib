from databaselib import basemysqldatabaselib, databaseAbstractions
from databaselib.databaseDevFriendlyAbstraction import User


basemysqldatabaselib.database = basemysqldatabaselib.Database("sql.freedb.tech", "freedb_SaDev", "h2@#Rz5SncUJ?QK", "freedb_coolDb")
basemysqldatabaselib.conn = basemysqldatabaselib.connect()

user = databaseAbstractions.registerUser("meowzer2", "1234")

if user == None:
    user = databaseAbstractions.loginUser("meowzer2", "1234")

print(user)

print(databaseAbstractions.editUser(user, "meowzer3"))