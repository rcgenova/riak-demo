#!/bin/bash

echo "Creating Riak KV default bucket type..."

sudo riak-admin bucket-type create bucket_type_default
sudo riak-admin bucket-type activate bucket_type_default

echo "Creating Riak KV map bucket type..."

sudo riak-admin bucket-type create bucket_type_map '{"props":{"datatype":"map"}}'
sudo riak-admin bucket-type activate bucket_type_map

echo "Creating TS Checkin table: $1..."

sudo riak-admin bucket-type create $1 '{"props":{"table_def": "CREATE TABLE '"$1"' (group_id sint64 not null, wine varchar not null, time timestamp not null, location varchar not null, location_lat double not null, location_long double not null, user varchar not null, rating sint64, comment varchar, PRIMARY KEY ((group_id, wine, quantum(time, 14, 'd')), group_id, wine, time))"}}'

sudo riak-admin bucket-type activate $1

echo "Creating TS Activity table: $2..."

sudo riak-admin bucket-type create $2 '{"props":{"table_def": "CREATE TABLE '"$2"' (group_id sint64 not null, user varchar not null, time timestamp not null, type varchar not null, wine varchar not null, location varchar not null, location_lat double not null, location_long double not null, rating sint64, comment varchar, friend varchar, PRIMARY KEY ((group_id, user, quantum(time, 14, 'd')), group_id, user, time))"}}'

sudo riak-admin bucket-type activate $2
