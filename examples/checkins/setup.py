from riak.riak_error import RiakError
from riak.client import RiakClient
from riak.datatypes import Map
import sys
import time
import random

client = RiakClient(host=sys.argv[1], pb_port=8087)

bucket_type_default = client.bucket_type("bucket_type_default")
bucket_type_map = client.bucket_type("bucket_type_map")

def create_users(user_bucket, friends_bucket):

    with open("users.txt") as f:

        users = f.read().splitlines()
	user_set = set(users) # remove dupes
	user_list = list(user_set)

	# Add user
        for user in user_list:
	    user = user.strip()
            record = user_bucket.new(user, data={})
            print "User " + user + " added... " + str(record.store())

	    # Add 10 random friends
	    for i in range(10):
		friend = user_list[random.randint(0, len(user_list) - 1)].strip()
		if friend != user:

    		    friends_list = Map(friends_bucket, user)
    		    friends_list.sets['friends'].add(friend)
    		    print "Friend " + friend + " added to user " + user + "... " + str(friends_list.store(return_body=False))

def create_locations(location_bucket):

    with open("locations.txt") as f:

        field_names = ['name', 'street', 'city', 'state', 'zip', 'lat', 'long']
    
        for i, line in enumerate(f):
	    field_values = line.split(',')
	    field_values[6] = field_values[6].strip()
	
	    object = dict(zip(field_names, field_values))
	    key = field_values[0].replace(" ", "_")
	    print key, object

	    record = location_bucket.new(key, data=object)
	    print record.store()

def create_wines(wine_bucket):

    with  open("wines.txt") as f:

        field_names = ['year', 'producer', 'style']

        for i, line in enumerate(f):
	    field_values = line.split(',')
	    field_values[2] = field_values[2].strip()
	
	    object = dict(zip(field_names, field_values))
	    key = '_'.join(field_values).replace(" ", "")
	
	    print key, object

	    record = wine_bucket.new(key, data=object)
	    print record.store()

if __name__ == "__main__":

    print "\n"
    # create_users(bucket_type_default.bucket('user2'), bucket_type_map.bucket('friends'))
    # print "\n"
    # create_locations(bucket_type_default.bucket('location2'))
    # print "\n"
    create_wines(bucket_type_default.bucket('wine2'))
    print "\n"



