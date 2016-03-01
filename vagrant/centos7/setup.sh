#!/bin/bash
set -e

echo "Installing dependencies..."
sudo yum install -y wget

# Python

echo "Installing Python dependencies..."
sudo yum install -y python-setuptools gcc python-devel libffi-devel openssl-devel
sudo easy_install pip

echo "Installing Riak Python client..."
sudo pip install riak

# Riak

echo "Fetching Riak..."
wget http://s3.amazonaws.com/private.downloads.basho.com/riak_ts/99a7df/1.2/1.2.0/rhel/7/riak-ts-1.2.0-1.el7.centos.x86_64.rpm

echo "Installing Riak..."
sudo yum install -y riak-ts-1.2.0-1.el7.centos.x86_64.rpm

echo "Set Riak to start on boot"
sudo /sbin/chkconfig riak on

echo "Setting ulimit..."
echo 'riak soft nofile 65536' | sudo tee --append /etc/security/limits.conf
echo 'riak hard nofile 65536' | sudo tee --append /etc/security/limits.conf
echo "$USER soft nofile 65536" | sudo tee --append /etc/security/limits.conf
echo "$USER hard nofile 65536" | sudo tee --append /etc/security/limits.conf

echo "Starting Riak..."
sudo riak start
sudo riak ping
