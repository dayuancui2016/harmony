# import library for dealing with JSON data
import json
# improt library for parsing timestamp strings
from dateutil import parser
# import library for reading command line arguments
import argparse

# create parser object
arg_parser = argparse.ArgumentParser()

# add argument
arg_parser.add_argument('file', type=argparse.FileType('r'))

# parse the passed command line arguments
args = arg_parser.parse_args()


# specify log file name
logfile = args.file.name#'log'

# initialize t1 and t2 total times
t1_total = 0
t2_total = 0

# initialize counter of valid block hashes
valid_block_hashes = 0

# open logfile
with open(logfile, 'r') as file:
    # initialize start flag to False
    start_flag = False

    # loop through each line in logfile
    for line in file:
        # feed each line to json parser
        data = json.loads(line)

        # parse the message and timestamp
        message = data['message']
        timestamp = parser.parse(data['time'])

        # start of block
        if message == "[Announce] Sent Announce Message!!":
            # get timestamp as t0 (starting point)
            t0 = timestamp
            
            # set the start flag
            start_flag = True

        # end of block
        elif message == "[OnCommit] Commit Grace Period Ended":
            # if block was already announced
            if start_flag:
                # make start flag false
                start_flag = False
                # increment counter of valid block hashes
                valid_block_hashes += 1

                # increment total times the values of current t1 and t2
                t1_total += t1
                t2_total += t2

            # if block was not announced
            else:
                print("Cannot commit block before announcing.")

        # T1
        elif message == "[OnPrepare] Sent Prepared Message!!" and start_flag:
            # get t1 time which is total time in seconds from current message to t0
            t1 = timestamp - t0
            t1 = t1.total_seconds()

        # T2
        elif message == "[finalCommit] Queued Committed Message" and start_flag:
            # get t2 time which is total time in seconds from current message to t0
            t2 = timestamp - t0
            t2 = t2.total_seconds()

# compute the averages
ave1 = t1_total / valid_block_hashes
ave2 = t2_total / valid_block_hashes

# print the results
print("ave1 = {} s\nave2 = {} s".format(ave1, ave2))