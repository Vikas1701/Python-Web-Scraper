import requests
from googletrans import Translator
from google.cloud import translate_v2 as translate
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin

def text_translator(soup, tag, translator):
    for i in soup.find_all(tag):
        if i.string:
            print(str(i.string))
            print(type(str(i.string)))
            if str(i.string) != "\n":
                try:
                    translated = translator.translate(str(i.string), src='en', dest='hi')
                    i.string.replace_with(translated.text)
                except:
                    print("error")
            print(i.string)


url = "http://classcentral.com"
translator = Translator()

session = requests.Session()
session.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"

html = session.get(url).content
print(html)
soup = bs(html, "html.parser")
print("="*100)
script_files = []
print(soup)
for script in soup.find_all("script"):
    if script.attrs.get("src"):
        script_url = urljoin(url, script.attrs.get("src"))
        script_files.append(script_url)

css_files = []

for css in soup.find_all("link"):
    if css.attrs.get("href"):
        css_url = urljoin(url, css.attrs.get("href"))
        css_files.append(css_url)



for i in soup.find_all("a"):
    if i.string:
        print(str(i.string))
        print(type(str(i.string)))
        translated = translator.translate(str(i.string), src='en', dest='hi')
        i.string.replace_with(translated.text)
        print(i.string)

for i in ["h1","h2","h3","h4","h5","h6","p","span","a","button","strong"]:
    text_translator(soup,i,translator)

html_file = soup.prettify("utf-8")
with open("classcentral.html", "wb") as file:
    file.write(html_file)

http_links = []
count = 0
for link in soup.find_all("a"):
    if link.attrs.get("href"):
        link_url = urljoin(url, link.attrs.get("href"))
        http_links.append(link_url)

        if count:
            name = str(link.attrs.get("href")).replace("/", "")
            translators = Translator()
            html = session.get(link_url).content
            soup = bs(html, "html.parser")
            for i in ["h1", "h2", "h3", "h4", "h5", "h6", "p", "span", "a", "button", "strong"]:
                text_translator(soup, i, translators)

            html_file = soup.prettify("utf-8")
            # name = str(link).replace("http", "").replace(":", "").replace(".com", "")
            with open(name + ".html", "wb") as file:
                file.write(html_file)
        count += 1


print("Total script files in the page:", len(script_files))
print(script_files)
print("Total CSS files in the page:", len(css_files))
print(css_files)
print("Total Links in the page:", len(http_links))
print(http_links)