import smtplib
import MimeWriter
import mimetools
import cStringIO


f = open("file.html", 'r')
html = f.read()
f.close()
print("HTML Input read from file.html")
subject = raw_input("Input Subject : ")
from1 = raw_input("Input From : ")
to = raw_input("Input To : ")

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
server.sendmail(from1, to, msg)
server.quit()