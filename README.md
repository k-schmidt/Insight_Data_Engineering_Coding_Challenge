# Fansite Analytics Challenge

Kyle Schmidt: <kyle.a.schmidt@gmail.com>

## Table of Contents
1. [Program Execution](README.md#program-execution)
2. [Challenge Summary](README.md#challenge-summary)
3. [Feature Explanations](README.md#feature-explanations)

## Program Execution
```bash
# Functionality was written and tested using Python 3.4

# Run the tests by invoking ./run_tests.sh from the current directory
./run_tests.sh

# Run the main function by invoking ./run.sh from the current directory
./run.sh
```


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

### Additional Features
1. Most popular 60 minute window where only one timestamp can be the representative of a window.
2. Most popular hour of the day.
3. Most popular day of the week.

## Feature Explanations

### Feature 1:
For this feature, I chose to use a Trie coupled with a heap in order to maintain the top 10 host/IP addresses.
I am storing a boolean within the last node 'character' of the host/IP address to tell me when that host/IP address is in the heap.
I am also storing a ```count``` attribute as an indicator of that host/IP priority.
If the host/IP address is in the heap then I perform a linear search for that node and update its priority indicator.
If the node is not in the heap but has achieved a greater priority than the minimum element in the heap, then I push the new node onto the heap and pop the minimum from the heap.
Afterwards, I re-heapify the heap to to maintain its invariant.


I am storing additional data in the last node of each host/IP address which kind of defeats the purpose of the Trie but I am doing this in order to save space since there are potentially 340 trillion trillion trillion different IP addresses (not counting hosts).
It may be more efficient to put all of the host/IP address into a dictionary as keys and the counts as their values.
I could then iterate through the dictionary and append the host/IP address to the heap at the very end.
Nonetheless, I am currently performing a linear search for an element if it is in the heap which isn't the most efficient but I chose a heap for easy access to the minimum host/IP node.
Furthermore, each call to ```heapq.heapify``` is linear according the python implementation.

### Feature 2:
I solved this feature similarly to feature 1.
I am storing each character of a resource into a Trie and incrementing their priority by the number of bytes sent in that line of the log into an attribute called ```count```.
I used a Trie because the resources could potentially reuse certain parts i.e. ```www.google.com``` and ```www.google.com/mail```, thereby saving space by reusing ```www.google.com```.


Similarly to feature 1, if the node is not in the heap but has achieved a greater priority than the minumum element in the heap, then I push the new node onto the heap and pop the minimum from the heap.
If the node is already in the heap then I perform a linear search for that resource and update its priority. I then reheapify the heap in order to maintain the heap invariant.

### Feature 3:
I used two queues and a heap to solve this challenge.
Queue1 contains all timestamps within the provided time range.
Queue2 contains all timestamps that fall outside of the provided time range.
At first, I thought that all max time ranges **could not** fall within the same hour.
My first pass at this solution recorded the max time for a given hour and tried to append it to the heap.
I ran the test suite for Insight and found that maxes **can** occur within the same hour and revised my solution.
The length of Queue1 represents the observations within that given hour.
If we observe a timestamp a timestamp that falls outside of that range then we append it to Queue2, record the length of Queue1, and pop the first element of Queue1.
The length represents the count (priority) for the popped element.
We then attempt to add the popped element and its priority to the heap.

### Feature 4:
I used two dictionaries for this challenge.
The first dictionary ```blocked_users``` is used to record users who have been blocked for five minutes.
The second dictionary ```user_dict``` is used to record consecutive failed login attempts with 20 seconds using a queue.
For every observation I assess whether the user is in ```blocked_users``` and see if their timestamp is less than 5 minutes ago - if it is then I log the observation.
If the person is in ```blocked_users``` and their timestamp is greater than 5 minutes ago then I remove them from blocked users.
If the status is 401 then I add the host to the ```user_dict```.
If a user in ```user_dict``` amasses 3 consecutive failed logins then they are popped from the ```user_dict``` and added to ```blocked_users```.
If the observed status is not 401 then I remove them from ```user_dict``` effectively restarting their accumulated failed logins.

### Feature 5
I had accidentally solved feature 3 using feature 5 at first and decided to keep the implementation as an additional feature.
I solved this feature using two queues, 1 heap, and an additional variable to keep track of the top representative of a 60 minute window.
I then log the top 10 representatives in a heap and output the result to a file called ```non_consecutive.txt```.

### Feature 6
Log the count of each hour accessed and output the results in descending order.
This gives an idea of what times of days the website is the busiest which might help to inform the company if servers need to be scaled up or down.

For this feature, I parse the hour from the timestamp and increment a counter for that key in the dictionary.

### Feature 7
Log the count of each day accessed and output the results in descending order.
This feature notifies if there is a day that has higher traffic than the others.
However both this feature and feature 6 aren't helpful if the site made a big press release (for example) on a given Tuesday at 1:00pm.
This record would skew the results and not provide an accurate measure of habitual website habits.

For this feature, I parse the day from the timestamp and increment a counter for that key in the dictionary.
