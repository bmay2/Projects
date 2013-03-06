from imapclient import IMAPClient
import smtplib

def send(gmail_user, gmail_pwd, recipient, message_body):

	smtpserver = smtplib.SMTP("smtp.gmail.com",587)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo
	smtpserver.login(gmail_user, gmail_pwd)

	header = 'To:' + recipient + '\n' + 'From: ' + gmail_user + '\n' + "Subject: Today's workout \n"
	msg = header + "\n" + message_body

	smtpserver.sendmail(gmail_user, recipient, msg)
	print 'done!'
	smtpserver.close()

def receive(username, password, sender):
	HOST = 'imap.gmail.com'
	ssl = True

	server = IMAPClient(HOST, use_uid=True, ssl=ssl)
	server.login(username, password)
	select_info = server.select_folder('INBOX')
	messages = server.search(['FROM "%s"' % sender])

	# print '%d messages in INBOX' % select_info['EXISTS']
	# print "%d messages that aren't deleted" % len(messages)

	response = server.fetch(messages, ['FLAGS', 'RFC822.SIZE', 'BODY[TEXT]', 'INTERNALDATE'])
	mostrecent = max(response.keys(), key=int)
	return response[mostrecent]['BODY[TEXT]']