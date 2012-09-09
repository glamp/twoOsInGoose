import redis
import json
import operator

r = redis.StrictRedis()
pubsub = r.pubsub()
pubsub.subscribe("wordcount")

total_wc = {}

for msg in pubsub.listen():

    # make sure that the data we're getting from redis is a string
    if isinstance(msg['data'], str):

        data = json.loads(msg['data'])

        # keeping track of the total word count
        for word in data:
            total_wc[word] = total_wc.get(word, 0.0) + 1
            data[word] = (data[word] / sum(data.values())) / (total_wc[word] / sum(total_wc.values()))

        # sorts the word count data from redis and puts it into a list of tuples (word, count of words on page)
        sorted_data = sorted(data.iteritems(), key=operator.itemgetter(1), reverse=True)

        # create a template for each row
        row = "|%s|%s|"
        # print the top of the table
        print "_"*36
        # print the table headers
        print row % ("Word".center(20), "Relative Freq".center(13))

        # print the top 20 words by word count
        for word, count in sorted_data[:20]:
            # center the strings
            word = word.center(20)
            count = str(int(count)).center(13)
            print "-"*36
            print row % (word, count)
        # print the bottom of the table
        print "-"*36
            
        # print a seperator
        print "*"*80


