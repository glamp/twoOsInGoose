twoOsInGoose
============

It was actually about one and a half I think. It was one and a half. I've got a great Polaroid of it, and he's right there, must be one and a half. 


Execute in 2 windows:

python crawler.py
python printer.py

crawler will crawl urls and publish the word count for each url to redis
printer subscribes to the redis feed and will print the word count for each url