import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
import init
start_time = time.clock()

def dekstop_url_sitemap(url):
    req = requests.get(url, headers=init.headers_dekstop)
    soup = BeautifulSoup(req.text, "lxml")
    sitemapTags = soup.find_all("loc")
    urls = []
    for loc in sitemapTags:
        data = sitemapTags.index(loc) + 1, loc.text
        urls.append(data[1])
    df_dekstop = pd.DataFrame(urls, columns=['Page URL'])
    df_dekstop = df_dekstop['Page URL'].apply(lambda x: x if x.endswith('/') else x + '/')
    df_dekstop.to_excel(init.writer, sheet_name="Dekstop", index=False)

def mobile_url_sitemap(url):
    req = requests.get(url, headers=init.headers_mobile)
    soup = BeautifulSoup(req.text, "lxml")
    sitemapTags = soup.find_all("loc")
    urls = []
    for loc in sitemapTags:
        data = sitemapTags.index(loc) + 1, loc.text
        urls.append(data[1])
    df_mobile = pd.DataFrame(urls, columns=['Page URL'])
    df_mobile = df_mobile['Page URL'].apply(lambda x: x if x.endswith('/') else x + '/')
    df_mobile.to_excel(init.writer, sheet_name="Mobile", index=False)

if __name__ == '__main__':
    dekstop_url_sitemap(init.url_dekstop)
    mobile_url_sitemap(init.url_mobile)
    init.writer.save()
    init.writer.close()
    print("--- %s seconds ---" % (time.clock() - start_time))

