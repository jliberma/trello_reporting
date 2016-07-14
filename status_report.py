#!/usr/bin/python

import datetime
from datetime import timedelta
import ConfigParser
from trello import TrelloClient, Unauthorized, ResourceUnavailable

# Read Config
Config = ConfigParser.ConfigParser()
Config.read("status_report.conf")
strapi_key = Config.get("DEFAULT", "api_key")
strapi_secret = Config.get("DEFAULT", "api_secret")
strtoken = Config.get("DEFAULT", "token")
strboardname = Config.get("DEFAULT", "board_name")
daystoreport = int(Config.get("DEFAULT", "days_to_report"))


# Setup client 
### token & token_secret come from 3-legged OAuth process
### api_key and api_secret are your Trello API credentials
client = TrelloClient(
    #api_key='your-key', api_secret='your-secret', token='your-oauth-token-key', token_secret='your-oauth-token-secret'
    api_key=strapi_key, api_secret=strapi_secret, token=strtoken
)

# Store date from 7 days ago
today = datetime.date.today()
strToday = today.strftime('%m/%d/%Y')
lastdate = today - timedelta(days=daystoreport)

# Open File
f = open("status.html", "wb")

# HTML Header
f.write("<HTML><HEAD><TITLE>" + strboardname + " - " + strToday + "</TITLE></HEAD><BODY><H1>" + strboardname + " - " + strToday + "</H1>")

print "Finding Board"
for b in client.list_boards():
  #print b
  if b.name == strboardname:
    print "Found Board - " + strboardname
    for l in b.all_lists():
      if l.name == 'Information':
        print l.name
        continue
      f.write("<H2><U>" + l.name + "</U></H2>")
      #print l.name
      for c in l.list_cards():
        c.fetch()
        print c.name
        print c.id
        print "Fetching Card Comments -", c.name
        members = ''
        for m in c.member_id:
          member = client.get_member(m)
          if members == '':
            members += member.full_name
          else:
            members += ", "
            members += member.full_name
        print "\t", c.name, "(", members, ")"
        f.write("<H3>" + c.name + "(" + members + ")</H3>")
        f.write("<UL>")
 
        for comment in c.comments:
           #print "\t\t", c.comments
           commentdatetime = datetime.datetime.strptime(comment['date'], '%Y-%m-%dT%H:%M:%S.%fZ')
           commentdate = commentdatetime.strftime('%m/%d/%Y %H:%M')
           if lastdate <= commentdatetime.date() <= today:
              #print commentdate, comment['data']['text']
              f.write("<LI><PRE><B>" + commentdate + " - </B>" + comment['data']['text'] + "</PRE></LI>")
        
        f.write("</UL>")

# Write Footer
f.write("</BODY></HTML>")

# Close File 
f.close()



