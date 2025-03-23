from PIL import Image
import os
import hashlib
import mysql.connector

cnx = mysql.connector.connect(user='root', password='savage1',
                              host='127.0.0.1',database='picturelib')

cursor = cnx.cursor()

def md5sum(filename, blocksize=65536):
    hash = hashlib.md5()
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            hash.update(block)
    return hash.hexdigest()

def get_date_taken(path):
	try:	
    		return Image.open(path)._getexif()[36867]
	except:
		return ""

sql = "DROP TABLE IF EXISTS images"
cursor.execute(sql)
cnx.commit()
print 'dropped table'

# create table
sql = "CREATE TABLE images ( imageID int NOT NULL, imagePath varchar(255), imageName varchar(255), imageCS varchar(255), imageDate timestamp, PRIMARY KEY (imageID) )"
cursor.execute(sql)
print 'created table'


# start writing to the database
id = 1
start_path = '.' # current directory
for path,dirs,files in os.walk(start_path):
    for filename in files:
	if filename.endswith('.JPG'):
		print filename
       		try:
                	im=Image.open(os.path.join(path,filename))			 
			#os.path.join(path,filename)
			try: 
				im.verify()
	        		CS = md5sum(os.path.join(path,filename))
        			mydate = get_date_taken(os.path.join(path,filename))
				cursor.execute("""INSERT INTO images  VALUES (%s,%s,%s,%s,%s)""",(id,path,filename,CS, mydate))
				id = id + 1
				cnx.commit()

			except IOError:
				print "No date"
       		except IOError:
			print "Not Image"
		print id, filename
#		if id >> 10:
#			exit()

cursor.close()
cnx.close()	
