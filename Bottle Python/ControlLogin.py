import sqlite3

connectdb = sqlite3.connect('database.db')

vt = connectdb.cursor()

def Control_Session(username):
    sonuc = vt.execute("SELECT count(*) FROM Session where Username = '"+username+"'")
    for row in sonuc.fetchall():
        data = row[0]
    if data != 0:
        return True
    else:
        return False

def Log_History(username):
    vt.execute("INSERT INTO LogHistory (SessionId,username,LoginTime) SELECT SessionId, username, LoginTime FROM Session WHERE username = '"+username+"'")
    connectdb.commit()
    vt.execute("DELETE FROM Session WHERE username = '"+username+"'")
    connectdb.commit()


def check_Login(username,password):
    sonuc = vt.execute("""Select count(*) from Users where username = ? and password = ? """,(username,password))
    for row in sonuc.fetchall():
        veri = row[0]
    if veri == 1:
        return True
    else:
        return False

def Login(SessionId, username, LoginTime):
    if Control_Session(username):
        Log_History(username)
    vt.execute('''insert into Session (SessionId,Username,LoginTime) values (?, ?, ?)''',(SessionId, username,LoginTime))
    connectdb.commit()

def Logout( username, LogoutTime):
    Log_History(username)
    vt.execute("UPDATE LogHistory SET LogoutTime = ? where Username = ? ",(LogoutTime,username))
    connectdb.commit()

def controlLogin(username):
    sonuc = vt.execute("SELECT count(*) FROM Session where Username = '" + username + "'")
    for row in sonuc.fetchall():
        data = row[0]
    if data != 0:
        return True
    else:
        return False

def get_role(username):
    sonuc = vt.execute("select role from Users where Username = '"+username+"'")
    for row in sonuc.fetchall():
        data = row[0]
    return data

