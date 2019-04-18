import requests
import re
import os
from bs4 import BeautifulSoup
import itertools
from tqdm import tqdm
import time


# get list of urls from sitemap here
# https://www.team-andro.com/sitemap-google.xml
# Download sitemap xmls?

def read_sitemap(url):
    top_sitemap = requests.get(url)
    # print(url)
    sitemap = BeautifulSoup(top_sitemap.text, "lxml-xml")
    sitemaps = list(map(lambda x: x.getText(), sitemap.find_all("loc")))

    return sitemaps


def read_sitemap_xml():
    for sitemap in os.listdir("andro_sitemaps"):

        path = os.path.join("andro_sitemaps", sitemap)
        print(path)

        with open(path) as xml:
            sitemap = BeautifulSoup(xml.read(), "lxml-xml")
            links = list(map(lambda x: x.getText(), sitemap.find_all("loc")))

            test = set()
            for link in tqdm(links):
                read_forum_page(link)


def read_forum_page(url):
    if "phpBB3" in url:
        text = requests.get(url).text
        soup = BeautifulSoup(text, "html.parser")

        m = re.search(r"-(t\d+)", url)
        if m:
            thread_id = m.group(1)
        else:
            thread_id = "t0000"

        posts = soup.find_all("div", id=re.compile(r"p\d+"))
        navlinks = soup.find("ul", class_="linklist navlinks").find_all("a")
        navlinks = [x.getText().replace(" ", "_") for x in navlinks]
        navlinks.append(thread_id)
        path = os.path.join("andro_text", *navlinks)

        if not os.path.exists(path):
            os.makedirs(path)

        for post in posts:
            post_id = post.get("id")
            text = post.find("div", class_="content").getText()
            user_block = post.find("a", href=re.compile(r"team-andro.com/my/.+-u\d+"))

            if not user_block:
                user_url = "user_deleted"
            else:
                user_url = user_block.get("href")

            # print("############")
            # print(user_url)
            # print(post_id)
            # print(url+"#"+post_id)
            # print(text)

            filepath = os.path.join(path, post_id)
            if not os.path.exists(filepath):
                with open(filepath, "w") as post_textfile:
                    post_textfile.write(text)




    #     Necessary info_
    # link title
    # username or user profile id="profile\d+"
    # post id? id="p\d+"

    # threadstruktur über Ordner, jeder post als einzelne textdatei
    # mongodb -> metadaten (post id usw + link zur textdatei oder zum post?)

    else:
        pass


def get_all_andro_pages():
    top_sitemaps = read_sitemap("https://www.team-andro.com/sitemap-google.xml")
    all_sites = itertools.chain([read_sitemap(url) for url in top_sitemaps])


def get_andro_sitemaps_as_files():
    top_sitemaps = read_sitemap("https://www.team-andro.com/sitemap-google.xml")

    for sm in top_sitemaps:
        print(sm)
        filename = "andro_sitemaps/" + sm.split("/")[-1]
        text = requests.get(sm).text
        with open(filename, "w") as file:
            file.write(str(text))


def crawl_andro():
    url = "https://www.team-andro.com/phpBB3/smartphone-handy-kaufberatung-und-talk-t295707.html"
    page = requests.get(url)

    text = page.text

    # print(text)

    soup = BeautifulSoup(text, "html.parser")

    # print(soup.head)
    # print(soup.title)

    # For TA forum
    posts = soup.find_all("div", ["post bg1", "post bg2"])

    print(posts[0].find("div", class_="content").getText())

    # For TA news


def create_folders():
    for file in os.listdir("andro_sitemaps"):
        name = os.path.splitext(file)[0]
        print(name)
        os.mkdir(os.path.join("andro_text", name))


if __name__ == '__main__':
    read_sitemap_xml()
