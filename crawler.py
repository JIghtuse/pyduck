#!/usr/bin/python

# TODO:
# * saving index to database (sqlite?)
#

def get_page(url):
    try:
        import urllib
        return urllib.urlopen(url).read()
    except:
        return ""

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

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
            index[keyword].append([url, 0])
    else:
        index[keyword] = [[url, 0]]

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
    index = {}
    while tocrawl and len(crawled) < max_pages:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            union(tocrawl, get_all_links(content))
            crawled.append(page)
    return index
