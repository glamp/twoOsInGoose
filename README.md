### "There are 2 Os in Goose, boys"
#### It was actually about one and a half I think. It was one and a half. I've got a great Polaroid of it, and he's right there, must be one and a half. 
============

Execute in 2 windows:

``` shell
  python crawler.py
```

``` shell
  python printer.py
```

* crawler will crawl urls and publish the word count for each url to a redis channel
* printer is a sample client subscriber illustrating how to subscribe
