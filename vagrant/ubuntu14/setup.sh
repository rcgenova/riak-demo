#!/bin/bash

set -e

echo "Installing dependencies..."
sudo apt-get update
sudo apt-get install -y curl

# Python

echo "Installing Python dependencies..."
sudo apt-get install -y python-setuptools python-dev libffi-dev libssl-dev
sudo easy_install pip

echo "Installing Riak Python client..."
sudo pip install riak

# Riak

echo "Fetching Riak..."
wget http://s3.amazonaws.com/private.downloads.basho.com/riak_ts/99a7df/1.2/1.2.0/ubuntu/trusty/riak-ts_1.2.0-1_amd64.deb

echo "Installing Riak..."
sudo dpkg -i riak-ts_1.2.0-1_amd64.deb

echo "Set Riak to start on boot"
sudo update-rc.d riak defaults

echo "Setting ulimit..."
echo 'riak soft nofile 65536' | sudo tee --append /etc/security/limits.conf
echo 'riak hard nofile 65536' | sudo tee --append /etc/security/limits.conf
echo "$USER soft nofile 65536" | sudo tee --append /etc/security/limits.conf
echo "$USER hard nofile 65536" | sudo tee --append /etc/security/limits.conf
echo "session required pam_limits.so" | sudo tee --append /etc/pam.d/common-session

echo "Starting Riak..."
sudo riak start
sudo riak ping
