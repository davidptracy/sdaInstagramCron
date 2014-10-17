# Script to run for Instagram queries via cron Job on remote server. 
# Written by David Tracy for Social Data Analysis Club @ ITP @ NYU 
# Last updated: 10/17/2014
# based on code by Gilad Lotan

# import libraries
import pickle
from urlparse import urlparse
from instagram.client import InstagramAPI

# Instagram API - get client_id, client_secret - for your app
# go here to register your application - http://instagram.com/developer/
# pip install python-instagram
# full documentation here - https://github.com/Instagram/python-instagram
client_id = 'YOUR_INSTAGRAM_API_CLIENT_ID'
client_secret = 'YOUR_INSTAGRAM_API_CLIENT_SECRET'

api = InstagramAPI(client_id=client_id, client_secret=client_secret)

# try to load the last max id from your directory
# if it doesn't load, set max tag id to 0
try:
	max_tag_id = pickle.load(open(path+'last_max_id.p','rb'))
	max_tag_id = max_tag_id - 1
except:
	max_tag_id = 0

# the search query you'd like to grab
used_tag = 'YOUR_SEARCH_QUERY'

# if this is the first set of data, grab an initial set of 33 results
# add those results to an array called all_media
# then grab the max_tag_id by parsing the url returned by the query
# then do the search 100 more times!
# after its done, save out a file containing the results and another file with the max_id
if max_tag_id == 0:

	ans = api.tag_recent_media(33, max_tag_id, used_tag)
	all_media = []

	for m in ans[0]:
	    all_media.append(m)

	parsed = urlparse(ans[1])
	params = {a:b for a,b in [x.split('=') for x in parsed.query.split('&')]}


	iterations = 100

	for i in range(iterations):
	    max_tag_id = int(params['max_tag_id'])
	    ans = api.tag_recent_media(33, max_tag_id-1, used_tag)
	    
	    # show the length of results from each loop
	#     print len(ans[0])
	    
	    # add every media object to an array
	    for m in ans[0]:
	        all_media.append(m)

	    # get next max_tag_id
	    parsed = urlparse(ans[1])
	    params = {a:b for a,b in [x.split('=') for x in parsed.query.split('&')]}
		    
	path = ''
	pickle.dump(all_media, open(path+'%s_pickle.p' % max_tag_id,'wb'))
	pickle.dump(max_tag_id, open(path+'last_max_id.p', 'wb'))


# if this is NOT the first set of data, grab the next 100 iterations of the search
# add those results to an array called all_media
# then grab the max_tag_id by parsing the url returned by the query
# after its done, save out a file containing the results and another file with the max_id
else:

	iterations = 100

	for i in range(iterations):
	    max_tag_id = int(params['max_tag_id'])
	    ans = api.tag_recent_media(33, max_tag_id-1, used_tag)
	    
	    # show the length of results from each loop
	#     print len(ans[0])
	    
	    # add every media object to an array
	    for m in ans[0]:
	        all_media.append(m)

	    # get next max_tag_id
	    parsed = urlparse(ans[1])
	    params = {a:b for a,b in [x.split('=') for x in parsed.query.split('&')]}
		    
	path = ''
	pickle.dump(all_media, open(path+'%s_pickle.p' % max_tag_id,'wb'))
	pickle.dump(max_tag_id, open(path+'last_max_id.p', 'wb'))



