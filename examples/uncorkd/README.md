# Uncorkd

Uncorkd is a backend for a hypothetical wine-centric social app modeled after UNTAPPD. It uses Riak KV for state-based object/document storage and Riak TS for event-based storage. It is written in Python. Check out the [slides](http://www.slideshare.net/clibou/riak-ts) from a recent SeaScale meetup.

## Setup and generate sample data

```bash
$ bash setup.sh Checkin Activity
$ python setup.py 127.0.0.1
$ python generate_checkins.py 127.0.0.1 Checkin Activity
```

## Query examples with riak-shell

### Open riak-shell

```bash
$ sudo riak-shell
```

### Queries

```bash
$ SELECT location, time FROM Checkin WHERE group_id = 1 AND wine = '2015_Talisman_PinotNoir' AND time >= 1451606400000 AND time <= 1451692800000;
```

