
# a script to do python based access to the github api

print("Data");


from github import Github   # github api access
import json                 # for converting a dictionary to a string
import pymongo              # for mongodb access


# Load the faker and its providers
from faker import Faker     # for anonymising names
from collections import defaultdict
faker  = Faker()
names  = defaultdict(faker.name)






#we initialise a PyGithub Github object with our access token.
#      
# 
with open('/Users/Ailbhe/Documents/PersonalAccessToken.txt') as f:
    key = f.readline()
g = Github(key)

#Let's get the user object and build a data dictionary
usr = g.get_user()

dct = {'user':         names[usr.login].replace(" ", ""), # anonymising
       'fullname':     names[usr.name],  # anonymising
       'location':     usr.location,
       'company':      usr.company,
       'public_repos': usr.public_repos,
       'followers':    usr.followers
              }

print ("dictionary is " + json.dumps(dct))


for k, v in dict(dct).items():
    if v is None:
        del dct[k]

print ("cleaned dictionary is " + json.dumps(dct))

# now let's store the data.

# Establish connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Creating a database
db = client.classDB

db.githubuser.insert_many([dct])


fc = usr.following
print ("following: " + str(fc))

# now lets get those followings
fl = usr.get_following()

for f in fl:
    dct = {'user':         names[f.login].replace(" ",""), # anonymising
           'fullname':     names[f.name], # anonymising
           'location':     f.location,
           'company':      f.company,
           'public_repos': f.public_repos,
           'followers':    f.followers
                      }
    for k, v in dict(dct).items():
        if v is None:
            del dct[k]
        
    print("following: " + json.dumps(dct))
    db.githubuser.insert_many([dct])    