from riak.client import RiakClient
import sys
import time
import datetime
import random

from checkin import Checkin
checkin = Checkin(sys.argv[1], sys.argv[2], sys.argv[3])

f = open("users.txt")
users = f.read().splitlines()
user_set = set(users) # remove dupes
user_list = list(user_set)
user_count = len(user_list)
f.close()

f = open("wines.txt")
wines = f.read().splitlines()
wine_count = len(wines)
f.close()

f = open("locations.txt")
locations = f.read().splitlines()
location_count = len(locations)
f.close()

# Insert 31 days worth of checkins, starting on 2016-01-01 00:00:00
# 'checkin_probability' above used to weight the daily distribution on an hourly basis
for t in range(1451606400000, 1454198400000, 60000):
    hour = int(time.strftime('%H', time.gmtime(t / 1000)))
    if random.randint(0, 100) < checkin_probability[hour]:
        print "hour: " + str(hour) + ", time: " + str(t)

	wine_fields = wines[random.randint(0, len(wines) - 1)].split(',')
        wine_fields[2] = wine_fields[2].strip()
	wine = '_'.join(wine_fields).replace(" ", "")

	location = locations[random.randint(0, len(locations) - 1)].split(',')[0].replace(" ", "_")
	location_object = location_bucket.get(location)
	lat = float(location_object.data['lat'])
	long = float(location_object.data['long'])

	user = user_list[random.randint(0, len(user_list) - 1)]
	rating = random.randint(1, 5)
	comment = rating_comment[rating]

	print wine, t, location, lat, long, user, rating, comment
	checkin.checkin(wine, t, location, lat, long, user, rating, comment)
	print "\n"

