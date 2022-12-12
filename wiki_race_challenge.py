from typing import List  # isort:skip
from filter_urls import find_articles, find_urls
from requesting_urls import get_html
import re
from urllib.parse import urljoin
import time
from multiprocessing import Pool
def find_en_articles(html: str):
    """Finds all the wiki articles inside a html text. Make call to find urls, and filter
    arguments:
        - text (str) : the html text to parse
    returns:
        - (set) : a set with urls to all the articles found
    """
    urls = find_urls(
        html)  # calling the function find_urls to pick up all urls of the html we pass in
    # making a pattern to find the articles of the urls
    pattern = re.compile(r'.*en.wikipedia.org/wiki.*$',  flags=re.IGNORECASE)
    articles = set()  # Set of Articles
    # looping through all the urls
    for url in urls:
        # finding the matching url, out of the pattern we have
        match_articles = pattern.findall(url)
        # for each aricle matching, adding to the set articles
        for article in match_articles:
            articles.add(article)

    # returning set of articles
    return articles

visited = []
def next_article_bfs(start: str, finish: str):
    tree = {}
    queue = []
    queue.append(start)
    while (len(queue) > 0):
        current = queue.pop(0)
        print(current)
        html = get_html(current)
        articles = find_en_articles(html)
        for url in articles:
            if url not in visited:
              tree[url] = current
              visited.append(url)
              queue.append(url)
            """
            elif url in visited:
              parent = current
              while parent != start and parent != "" and tree[current]:
                child = tree[parent]
                parent = child
                if parent == start:
                  return tree
            """
            if url == finish:
              print("found it")
              return tree


    return tree


def find_path(start: str, finish: str) -> List[str]:
    """Find the shortest path from `start` to `finish`

    Arguments:
      start (str): wikipedia article URL to start from
      finish (str): wikipedia article URL to stop at

    Returns:
      urls (list[str]):
        List of URLs representing the path from `start` to `finish`.
        The first item should be `start`.
        The last item should be `finish`.
        All items of the list should be URLs for wikipedia articles.
        Each article should have a direct link to the next article in the list.
    """
    path = []
    start_timer = time.time()
    graphtree = next_article_bfs(start, finish)
    end_timer = time.time()
    print(f"Total time used: {end_timer-start_timer}s")
    parent = finish
    path.append(parent)
    while parent != start:
      child = graphtree[parent]
      parent = child
      path.append(parent)
    path.reverse()


    assert path[0] == start
    assert path[-1] == finish
    return path


if __name__ == "__main__":
    start = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    finish = "https://en.wikipedia.org/wiki/Peace"
    path = find_path(start, finish)
    """
    pool = Pool(processes=1) 
    p = pool.apply_async(path)
    pool2 = Pool(processes=1) 
    path2 = pool2.apply_async(path)
    """
    print(path)