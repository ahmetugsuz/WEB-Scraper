import re
from urllib.parse import urljoin
from requesting_urls import get_html
## -- Task 2 -- ##


def find_urls(
    html: str,
    base_url: str = "https://en.wikipedia.org",
    output: str = None,
) -> set:
    """Find all the url links in a html text using regex
    Arguments:
        html (str): html string to parse
    Returns:
        urls (set) : set with all the urls found in html text
    """
    # create and compile regular expression(s)

    urls = set() # set of urls
    # 1. find all the anchor tags, then
    # 2. find the urls href attributes
    # anc_pat finds all the <anc alt="..." src="..."> snippets
    # this finds <a and collects everything up to the closing '>'
    anc_pat = re.compile(r"<a[^>]+>", flags=re.IGNORECASE)
    # href finds the text between quotes of the `href` attribute
    url_pat = re.compile(r'href="([^"]+)"', flags=re.IGNORECASE)
    # finding all the a tags
    for anc_tag in anc_pat.findall(html):
        anc_tags = url_pat.findall(anc_tag)
        addstring = ""
        # then find the attribute href of the ancor 
        for href_tekst in anc_tags: 
            addstring = re.sub(r'#[^>]+', '', href_tekst) #ignoring the the rest of the text when # appears
                    
            if href_tekst[0] == '/' and href_tekst[1] != '/': #if its only one /
                addstring = re.sub(r'^/', base_url+"/", addstring) # adding the base url
            elif href_tekst[0] == '/' and href_tekst[1] == '/': 
                addstring = re.sub(r'^//', "https://", addstring)
            
        #if the addstring is not empty, add to the set 
        if addstring != "":
            urls.add(addstring)



    # Write to file if requested
    if output:
        text_file = open(f"{output}", "w")
        print(f"Writing to: {output}")
        for tags in urls:
            print(f"{tags}", file=text_file)

    #returning the set of urls
    return urls

def find_articles(html: str, output=None) -> set:
    """Finds all the wiki articles inside a html text. Make call to find urls, and filter
    arguments:
        - text (str) : the html text to parse
    returns:
        - (set) : a set with urls to all the articles found
    """
    urls = find_urls(html) # calling the function find_urls to pick up all urls of the html we pass in
    pattern = re.compile(r'.*wikipedia.org/wiki.*$',  flags=re.IGNORECASE) # making a pattern to find the articles of the urls
    articles = set() # Set of Articles 
    # looping through all the urls
    for url in urls: 
        # finding the matching url, out of the pattern we have
        match_articles = pattern.findall(url)
        # for each aricle matching, adding to the set articles
        for article in match_articles:
            articles.add(article)

    
    # Write to file if wanted
    if output:
        text_file = open(f"{output}", "w")
        print(f"Writing to: {output}")
        for article in articles:
            print(f"{article}", file=text_file)

    #returning set of articles    
    return articles




## Regex example
def find_img_src(html: str):
    """Find all src attributes of img tags in an HTML string

    Args:
        html (str): A string containing some HTML.

    Returns:
        src_set (set): A set of strings containing image URLs

    The set contains every found src attibute of an img tag in the given HTML.
    """
    # img_pat finds all the <img alt="..." src="..."> snippets
    # this finds <img and collects everything up to the closing '>'
    img_pat = re.compile(r"<img[^>]+>", flags=re.IGNORECASE)
    # src finds the text between quotes of the `src` attribute
    src_pat = re.compile(r'src="([^"]+)"', flags=re.IGNORECASE)
    src_set = set()
    # first, find all the img tags
    for img_tag in img_pat.findall(html):
        # then, find the src attribute of the img, if any
        match = src_pat.search(img_tag)
        if match:
            src_set.add(match.group(1))
    return src_set
