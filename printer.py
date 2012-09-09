import redis
import json

r = redis.StrictRedis()
pubsub = r.pubsub()
pubsub.subscribe("wordcount")

total_wc = {}

for msg in pubsub.listen():
    if not isinstance(msg['data'], long):
        print "*"*80
        data = json.loads(msg['data'])
        for word in data:
            print '\t',word, data[word]
            total_wc[word] = total_wc.get(word, 0) + 1

        print "*"*80