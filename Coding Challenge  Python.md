

### Coding Challenge / Python

#### Current Solution

This question's asking to build a scalable web crawler that can handle up to million-level urls. My solution is to use an asynchronous web crawler.  Therefore, `aiohttp` and `asyncio` were used. 

`parse` method is an asynchronous method where a given url is parsed and processed. It will store twitter handler, facebook id, android id and ios id into `res` array. 

In the code driver, I created a `loop` where a bunch of urls were created and executed asynchronously. 

#### To do:

1. Applying `multiprocessing`. This web crawler can be done using `multiprocessing` package. Once finished, we can create many jobs named as `parse(url)`  and push them into a pool. Every time a process is idle, a job will be pulled out from the pool. Theoretically, time complexity will be O(n/p), where p is the number of processes.











