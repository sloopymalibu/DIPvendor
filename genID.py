# A script to log and generate Vendor IDs for C.H.I.P. DIP add-on boards
# Script by Peter Nyboer peter@nextthing.co

# TO DO:
# Add a 'delete' or 'delete last' ID function

import sys
import random
import json
import re

def makeid(email,vendorname,preferredID=None):
    prefID = ''
    if preferredID:
        prefID = preferredID.lower()
    else:
        prefID = hex(random.randrange(0,2147483647))
    # read json of existing IDs
    jsonfile = open('DIP_vendors.json')
    jsondata = jsonfile.read()
    print jsondata
    vendorDB = json.loads(jsondata)
    # parse existing IDs into list to use to check uniqueness:
    currentIDs = list()
    for key, data in vendorDB.iteritems():
        for vid,vinfo in data.iteritems():
            print 'VID: '+str(vid)
            currentIDs.append(vid)
    # make sure JSON is ok
    if not preflight(currentIDs):
        print 'The JSON file does not have contain all unique vendor IDs. Please Fix DIP_vendors.json'
        quit()
    else:
        # if the desired ID matches an existing ID, generate a new one
        if prefID in currentIDs:
            print ' :( Your chosen Vendor ID '+prefID+' is already taken.'
            choice = raw_input(' > Type "e" to exit or "g" to generate a new ID: ')
            if choice == 'g':
                while prefID in currentIDs:
                    prefID = hex(random.randrange(0,2147483647))
                print ' + Your new vendor ID is: '+prefID
            else:
                print 'quit'
                quit()
        # add info to JSON file
        newvendor = { prefID: {"vendor": vendorname,"contact": email} }
        vendorDB['vendorIDs'].update(newvendor)
        with open('DIP_vendors.json','w') as writejson:
            json.dump(vendorDB,writejson)
        print ' :) vendorDB updated'

# simple regex check of email format.
def valid_email(email):
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
    if match:
        return match
    else:
        print ' ! email not valid format. Call script with 3 arguments (last is optional):\n  $ python genID.py person@dipmaker.com "DIP Makers Inc." 0x00000001'
        quit()

# test out the vendor IDs to make sure they are unique. Unfortunately, json.loads() will filter out exactly matched keys, so we can't do much about that.
def preflight(x):
    print '-- preflight --'
    seen = set()
    # http://stackoverflow.com/questions/5278122/checking-if-all-elements-in-a-list-are-unique
    test = not any( i.lower() in seen or seen.add(i.lower() ) for i in x)
    print '>> preflight result '+str(test)
    return test

# TO DO - insert preflight on JSON to make sure it is OK
# test arguments sys.argv to make sure all is good, then call makeid.
if len(sys.argv) < 3:
    print ' ! Call genID.py with at least email and vendorname arguments.\n  Optional 3rd argument is desired ID, e.g.:\n     $ python genID.py person@dipmaker.com "DIP Makers Inc." 0x00000001'
elif len(sys.argv) == 3:
    if valid_email(sys.argv[1]):
        makeid(sys.argv[1],sys.argv[2])
elif len(sys.argv) == 4:
    if valid_email(sys.argv[1]):
        makeid(sys.argv[1],sys.argv[2],sys.argv[3])
