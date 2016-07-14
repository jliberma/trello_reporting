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
### api_key and api_secret are your Trello API credentials
client = TrelloClient(
    api_key=strapi_key, api_secret=strapi_secret, token=strtoken
)

# Store date from 7 days ago
today = datetime.date.today()
strToday = today.strftime('%m/%d/%Y')
lastdate = today - timedelta(days=daystoreport)

# remove comments and format output to XML or something else
for b in client.list_boards():
  if b.name == strboardname:
    for l in b.all_lists():
      if l.name == 'Information':
        continue
      print l.name
      for c in l.list_cards():
	# list card members
        c.fetch()
	# get 5 most recent comments
        members = ''
        for m in c.member_id:
          member = client.get_member(m)
          if members == '':
            members += member.full_name
          else:
            members += ", "
            members += member.full_name
        print "\t", c.name, "(", members, ")"
	# add description to the card that includes openstack version
	print "\t","Description: ",c.description
	# add a timestamp to the 5 most recent comments
	print "Comments:"
	for comment in c.comments:
          commentdatetime = datetime.datetime.strptime(comment['date'], '%Y-%m-%dT%H:%M:%S.%fZ')
          commentdate = commentdatetime.strftime('%m/%d/%Y %H:%M')
	  print commentdate,comment['data']['text']
	print "##########"
