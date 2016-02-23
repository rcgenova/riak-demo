from riak.client import RiakClient
from riak.riak_error import RiakError
from riak.datatypes import Map
import sys
import time

class Checkin:

    def __init__(self, host, checkin_table, activity_table):
	self.client = RiakClient(host=host, pb_port=8087)
	self.checkin_table = checkin_table
	self.activity_table = activity_table

    def checkin(self, wine, timestamp, location, location_lat, location_long, user, rating=0, comment=""):

        bucket_type_default = self.client.bucket_type("bucket_type_default")
        bucket_type_map = self.client.bucket_type("bucket_type_map")

        friends_bucket = bucket_type_map.bucket('friends')
        checkin_table = self.client.table(self.checkin_table)
        activity_table = self.client.table(self.activity_table)

        # Insert Checkin
        rows=[]
        rows.append([1, wine, timestamp, location, location_lat, location_long, user, rating, comment])
        ts_object = checkin_table.new(rows)
	print rows
        print "Checkin stored: ", str(ts_object.store())

        # Update Activity feeds
        rows=[]
        rows.append([1, user, timestamp, "Checkin", wine, location, location_lat, location_long, rating, comment, ""])

        # Get friends list
        friends_list = Map(friends_bucket, user)
        friends_list.reload()

        # Fan out checkin to friends activity feeds
        for friend in friends_list.sets['friends']:
            rows.append([1, friend, timestamp, "FriendCheckin", wine, location, location_lat, location_long, rating, comment, user])

        # Batch write activities
        ts_object = activity_table.new(rows)
        print "Activities stored: ", str(ts_object.store())

        # Update location daily counter
        counter = time.strftime('%Y-%m-%d', time.gmtime(timestamp))
        self.update_stats(location, counter)

        # Update location monthly counter
        counter = time.strftime('%Y-%m', time.gmtime(timestamp))
        self.update_stats(location, counter)

    def update_stats(self, key, counter):

	bucket_type_map = self.client.bucket_type("bucket_type_map")
        wine_stats = bucket_type_map.bucket('wine_stats')
        location_stats = bucket_type_map.bucket('location_stats')

        kv_object = Map(location_stats, key)
        kv_object.counters[counter].increment()
        print "Counter updated: ", str(kv_object.store(return_body=False))

