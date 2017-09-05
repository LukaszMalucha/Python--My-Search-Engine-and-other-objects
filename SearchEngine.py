## >>>Search Engine with description<<<


def get_page(url):
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ""


## >>>Web Crawling Procedure<<<

def get_next_target(page):
    start_link = page.find('<a href=')
    ## If the link tag sequence is not found, find will return "-1"
    if start_link == -1:
        ## Returns None and 0 as an error message
        return None, 0

    ## Procedure marks where url links starts and ends
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]

    ## Url and starting point for the next loop (end_quote) is returned
    return url, end_quote

## >>>URL Collector that puts all the links in a list<<<

def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)


## >>>Crawl procedure that creates two lists - crawled pages and to be crawled.<<<

def crawl_web(seed,max_depth):
    tocrawl = [seed]
    crawled = []
    index = {}
    graph = {}                             #3# variable created to rank pages - list of linked pages
    while tocrawl:
        page = tocrawl.pop()             ## pops out the last link from 'tocrawl' and adds it to...
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            outlinks = get_all_links(content)
            graph[page] = outlinks
            union(tocrawl, outlinks)
            crawled.append(page)       ##...crawled list
    return index, graph

## >>>Now, let's create index that will store all the crawled data<<<

def add_to_index(index, keyword, url):           ## Three variables: stored index, search keyword and associated url
    if keyword in index:
        index.[keyword].append(url)
    else:                                        ## if not found
        index[keyword] = [url]

def lookup(index, keyword):                      ## lookup function
    if keyword in index:
        return index[keyword]
    else:
        return None

def add_page_to_index(index, url, content):      ## indexing page content
    words = content.split()
    for word in words:
        add_to_index(index, word, url)


## >>>Procedure for ranking pages<<<

def compute_ranks(graph):
    d = 0.8                                     ## damping factor (may vary)
    numloops = 10                               ## Looping (may vary)

    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 /npages

    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1-d) / npages
            for node in graph:
                if page in graph[node]:
                    newrank = newrank + d* (ranks[node] / len(graph[node])
            newranks[page] = newrank
        ranks = newranks
    return ranks