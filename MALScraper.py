"""
A simple web scraper that scrapes the top manga from MyAnimeList.net and outputs the results to a text file.
Also filters out any manga that has more than 5 volumes.
"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
import sys

# TODO: filter out light novels

counter = [0]

def fetch_page(url):
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    return soup

def get_manga(soup):
    soup_text = soup.get_text().splitlines()
    for tag in soup_text:
        if "vols" in tag and "Manga" in tag:
            tag_check = tag[-8:]
            tag_check = tag_check.replace(" ", "")
            tag_check = tag_check.replace("vols", "")
            tag_check = tag_check.replace("(", "")
            tag_check = tag_check.replace(")", "")
            if len(tag_check) > 3:
                print("Error: " + tag_check)
                quit()
            try:
                length = int(tag_check)
                if length < 6:
                    title = soup_text[soup_text.index(tag)-2]
                    print(title)
                    print(tag[8:])
                    counter[0] += 1

                    # Find the url associated with the manga:

                    links = soup.find_all('a')
                    for link in links:
                        if title in link.get_text():
                            url = link.get('href')
                            break
                    print(url + " \n\n")

                    if tag in soup_text:
                        soup_text.remove(tag)

            except ValueError:
                pass

def main():

    original_stdout = sys.stdout

    with open('mangat.txt', 'w') as f:
        sys.stdout = f

        url = "https://myanimelist.net/topmanga.php"

        soup = fetch_page(url)
        get_manga(soup)

        # 1-180 max
        page_number = 1
        for i in range(1, 19):
            soup = fetch_page(url + "?limit=" + str(i*50))
            get_manga(soup)
            page_number += 1

        print("Pages scraped: " + str(page_number))
        print("Total number of manga found: " + str(counter[0] - 1))

    sys.stdout = original_stdout

if __name__ == "__main__":
    main()