# a script to do python based access to the mongodb
# step 6 - Let's do a useful search

print("Demonstration python based mongodb access");


import pymongo              # for mongodb access
import pprint               # for pretty printing db data

# Let's get the user object from the db

# Establish connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Create a database
db = client.classDB


# Creating a database that contains following's follower Count and repo count


with open('data.csv', 'w') as f:
    f.write('User,Followers,RepoCount\n')
    dct = db.githubuser.find({'user': {'$exists': True}})
    for user in dct:
        pprint.pprint(user)
        print()
        f.write(user['user'] + ',' + str(user['followers']) + ',' + str(user['public_repos']) +'\n')
