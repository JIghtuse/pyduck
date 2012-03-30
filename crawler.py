#!/usr/bin/python
import urllib

# TODO:
# * saving index to database (sqlite?)
#

def lucky_search(index, ranks, keyword):
    if keyword not in index:
        return None
    search = index[keyword][0]
    for page in index[keyword]:
        if ranks[page] > ranks[search]:
            search = page
    return search

def get_page(url):
    try:
        return urllib.urlopen(url).read()
    except:
        return ""

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_url = page.find('"', start_link)
    end_url = page.find('"', start_url + 1)
    return page[start_url + 1:end_url], end_url

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)

def get_all_links(page):
    links = []
    while True:
        url,endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)

def add_to_index(index, keyword, url):
    if index.has_key(keyword):
        if url not in index[keyword]:
            index[keyword].append(url)
    else:
        index[keyword] = [url]

def record_user_click(index, keyword, url):
    for entry in index[keyword]:
        if entry[0] == url:
            entry[1] += 1

def lookup(index, keyword):
    if index.has_key(keyword):
        return index[keyword]
    return None

def crawl_web(seed, max_pages=1000):
    tocrawl = [seed]
    crawled = []
    graph = {}
    index = {}
    while tocrawl and len(crawled) < max_pages:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            outlinks = get_all_links(content)
            graph[page] = outlinks
            union(tocrawl, outlinks)
            crawled.append(page)
    return index, graph

def compute_ranks(graph):
    d = 0.8
    numloops = 10
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages

    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for node in graph:
                if page in graph[node]:
                    newrank += d * (ranks[node] / len(graph[node]))
            newranks[page] = newrank
        ranks = newranks
    return ranks
