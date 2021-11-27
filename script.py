
# a script to do python based access to the github api
# step 4 - Let's store our data in a mongodb
# remember to pip install pymongo

print("Demonstration python based github api access");


from github import Github   # github api access
import json                 # for converting a dictionary to a string
import pymongo              # for mongodb access
import os

# Load the faker and its providers
from faker import Faker     # for anonymising names
from collections import defaultdict
faker  = Faker()
names  = defaultdict(faker.name)




#to shuffle move ascii value of every char
# ef shift_ascii(name_string):
#     newname_list =  [chr(ord(name_string[i])+2) for i in range(len(name_string))]
#     newname_string = ''.join(newname_list)
#     return  newname_string

#we initialise a PyGithub Github object with our access token.
#     note that this token is ours, and now deleted. You must 
#     crete your own access token and use here instead. 
tk = os.getenv('GITHUB_PAT')
g = Github(tk)

#Let's get the user object and build a data dictionary
usr = g.get_user()

dct = {'user':         names[usr.login].replace(" ", ""), # anonymising
       'fullname':     names[usr.name],  # anonymising
       'location':     usr.location,
       'company':      usr.company,
       'public_repos': usr.public_repos
       }

print ("dictionary is " + json.dumps(dct))

# now let's store the dictionary in a mongodb

# first we need to remove null fields from the dictionary, because
# if we don't we'll end up with null fields in the db. This will cause us
# lots of debugging problems later. The convention is only store actual data
# in the database.

for k, v in dict(dct).items():
    if v is None:
        del dct[k]

print ("cleaned dictionary is " + json.dumps(dct))

# now let's store the data.

# Establish connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Create a database
db = client.classDB

db.githubuser.insert_many([dct])

# now for demo purposes we'll get some data. We'll get the accounts followers
# and for each of them we'll get and add a count of the number of repos they have
fc = usr.followers
print ("followers: " + str(fc))

# now lets get those followers
fl = usr.get_followers()

for f in fl:
    dct = {'user':         names[f.login].replace(" ",""), # anonymising
           'fullname':     names[f.name], # anonymising
           'location':     f.location,
           'company':      f.company,
           'public_repos': f.public_repos
           }
    for k, v in dict(dct).items():
        if v is None:
            del dct[k]
        
    print("follower: " + json.dumps(dct))