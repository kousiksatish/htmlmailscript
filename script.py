import smtplib
import MimeWriter
import mimetools
import cStringIO
import MySQLdb

HOST = 'localhost'
USER = 'root'
PASS = 'kousiksatish'
DB = 'email'

db=MySQLdb.connect(HOST, USER, PASS, DB);
cur=db.cursor() 
cur.execute("SELECT email_id FROM email")
data = cur.fetchall()
to = ""
for dat in data:
	to += dat[0]
	to+=", "

to = to[:-2]
rec_list = to.split(", ")
cur.close()
db.close()

f = open("file.html", 'r')
html = f.read()
f.close()
print("HTML Input read from file.html")
subject = raw_input("Input Subject : ")
#to = raw_input("Input To : ")
#to = "ssundarraj@gmail.com, 106113051@nitt.edu, 106113077@nitt.edu"
#recepients_list = []

out = cStringIO.StringIO()
writer = MimeWriter.MimeWriter(out)
writer.addheader("Subject", subject)
writer.addheader("MIME-Version", "1.0")
writer.startmultipartbody("alternative")
writer.flushheaders()

subpart = writer.nextpart()
subpart.addheader("Content-Transfer-Encoding", "quoted-printable")

htmlin = cStringIO.StringIO(html)
pout = subpart.startbody("text/html", [("charset", 'us-ascii')])
mimetools.encode(htmlin, pout, 'quoted-printable')
htmlin.close()

writer.lastpart()

msg = out.getvalue()
out.close()

print msg

server = smtplib.SMTP("localhost")
for mail in rec_list:
	server.sendmail('kousiksatih@gmail.com', mail, msg)
	print "Mail sent to " + mail
server.quit()