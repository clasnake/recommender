import sqlite3 as sqlite
import os


class db:
    def setdb(self, dbfile):
        self.con = sqlite.connect(dbfile)
        self.con.execute('create table if not exists item(id,title)')
        self.con.execute('create table if not exists data(user,movieid,rating,ts)')
        self.curs = self.con.cursor()

    def insertItem(self, path=os.getcwd() + '//ml-100k'):
        try:
            for line in open(path + '/u.item'):
                (theid, thetitle) = line.split('|')[0:2]
                query = 'insert into item values("%s","%s")' % (theid, thetitle)
                print query
                self.curs.execute(query)
            self.con.commit()
        except Exception:
            print 'insert failed'


    def dump(self):
        try:
            self.curs.execute('delete from item')
            self.con.commit()
            print 'dump succeed'
        except Exception:
            print 'dump failed'

    def select(self):
        try:
            self.curs.execute('select * from item ')
            for row in self.curs:
                print row[0]
            print 'select succeed'
        except Exception:
            print 'select failed'


DB = db()
DB.setdb('MovieLensDB.db')
#DB.dump()
#DB.insertItem()
#DB.select()
