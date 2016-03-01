from riak.client import RiakClient
from riak.riak_error import RiakError
import sys
import time

client = RiakClient(host=sys.argv[1], pb_port=8087)
table_name = sys.argv[2]

table = client.table(table_name)

## Read row
print "Reading row..."
time1 = int(round(time.time() * 1000))
print "Read row return: ", str(client.ts_get(table, ['family1', 'series1', 1420113600000]).rows)
time2 = int(round(time.time() * 1000))
print "Time elapsed (ms): ", str(time2 - time1)
print "\n"

print "Reading rows..."
query = "select * from " + table_name + "  where myfamily = '1' and myseries = '1' and time >= 1420200000000 and time < 1420200001000"
print "Query: " + query
time1 = int(round(time.time() * 1000))
ts_obj = client.ts_query(table, query)
time2 = int(round(time.time() * 1000))
print "\n"
print ts_obj.rows
print "\n"
print "Row count: " + str(len(ts_obj.rows))
print "Time elapsed (ms): ", str(time2 - time1)
print "\n"

