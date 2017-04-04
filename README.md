# Fansite Analytics Challenge
Author:
Kyle Schmidt: <kyle.a.schmidt@gmail.com>

## Challenge Summary

Picture yourself as a backend engineer for a NASA fan website that generates a large amount of Internet traffic data. Your challenge is to perform basic analytics on the server log file, provide useful metrics, and implement basic security measures.

The desired features are described below:

### Feature 1:
List the top 10 most active host/IP addresses that have accessed the site.

### Feature 2:
Identify the 10 resources that consume the most bandwidth on the site

### Feature 3:
List the top 10 busiest (or most frequently visited) 60-minute periods

### Feature 4:
Detect patterns of three failed login attempts from the same IP address over 20 seconds so that all further attempts to the site can be blocked for 5 minutes. Log those possible security breaches.

## Feature Descriptions

### Feature 1:
For this feature, I chose to use a Trie coupled with a
