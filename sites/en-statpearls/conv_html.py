#!/usr/bin/python3
import os, string, sys
import copy
import json
import re
from urllib.parse import urljoin, urldefrag, urlparse
from bs4 import BeautifulSoup, Comment, SoupStrainer
import iiab.adm_lib as adm

site = 'www.statpearls.com'

orig_dir = '/articlelibrary/viewarticle/'
base_url = 'https://' + site + orig_dir
src_dir = 'raw/'
dst_dir = '/library/www/html/modules/en-statpearls/articles/'

# read urls
url_json_file = site + '_urls.json'
site_urls = adm.read_json(url_json_file)

def main(argv):
    # need site_urls for type of image - see below

    file_list = os.listdir(src_dir)
    #file_list = ['article-17922.html','article-41380.html','article-788.html', 'article-99590.html', 'article-29120.html', 'article-16989.html']
    for filename in file_list:
        print('Converting ' + filename)
        if not filename.endswith(".html"):
            print('Skippinging ' + filename)
            continue
        page = do_page(os.path.join(src_dir, filename))
        html_output = page.encode_contents(formatter='html')

        with open(dst_dir + filename, 'wb') as f:
            f.write(html_output)

def do_page(path):
    with open(path, 'r') as f:
        html = f.read()

    page = BeautifulSoup(html, "html5lib")
    #page = BeautifulSoup(html, "html.parser")

    css_files = page.find_all('link',{'rel':'stylesheet'})

    for link in css_files:
        link.extract()

    for s in page(["script", "style"]): # remove all javascript and stylesheet code
        s.extract()

    article_parts = page.find_all("div", {"class":"card"}) # there are 2
    article_text = article_parts[0]
    article_ref = article_parts[1]

    article_text = replace_links(article_text,"/pictures/getimagecontent", '../pictures/')
    article_ref = replace_links(article_ref,"/pictures/getimagecontent", '../pictures/')
    article_text = replace_links(article_text,"/media")
    article_ref = replace_links(article_ref,"/media")

    #logo_img = BeautifulSoup('<img src="../assets/stat-pearls-logo.png">', 'html.parser')
    #article_text.select('div', class_='card').append(logo_img)

    logo_img = page.new_tag("img", src="../assets/stat-pearls-logo.png")
    article_text.div.insert_before(logo_img)

    page.body.clear()
    page.body.append(article_text)
    page.body.append(article_ref)

    # convert picture links
    repl_pic_links(page)

    head_lines = BeautifulSoup(get_head_lines(), 'html.parser')

    #print(head_lines)
    bottom_lines = BeautifulSoup(get_bottom_lines(), 'html.parser')
    #print(bottom_lines)

    page.head.append(head_lines)
    page.body.append(bottom_lines)

    return page

def replace_links(tag, from_link, to_link=None):
    if not to_link:
        to_link = '..' + from_link
    if to_link[-1] != '/':
        to_link += '/'
    #print('tag before len: ',len(tag))
    #os.path.join(src_dir, filename)
    links = tag.find_all(href=re.compile(from_link))
    for link_tag in links:
        #print(link_tag)
        link = link_tag['href']
        #print(link)
        # make sure this is one of our target links
        parsed_link = urlparse(link)
        if parsed_link.netloc and parsed_link.netloc != site:
            continue
        url = urljoin(base_url, link)
        url = cleanup_url(url) # put url in same format as in json

        content_type = site_urls[url].get('content-type', '')
        content_type = content_type.strip()
        if content_type == 'image/jpeg':
            suffix = 'jpg'
        else:
            suffix = content_type.split('/')[1]
        if link[-1] == '/':
            link = link[:-1]
        filename = link.rsplit('/')[-1]
        if '.' not in filename[:-1]:
            filename += '.' + suffix
        if filename[-1] == '.':
            filename += suffix

        local_file = to_link + filename
        print(local_file)
        link_tag['href'] = link_tag['href'].replace(link, local_file)
        img_link = link_tag.find('img')
        #print(img_link)
        if img_link:
            img_url = img_link['src']
            img_link['src'] = img_link['src'].replace(img_url, local_file)
    #print('tag after len: ',len(tag))
    return tag

######## NOT USED ##################
def repl_pic_links(page):
    pix_links = page.body.find_all(href=re.compile("/pictures/getimagecontent"))
    for pix_link in pix_links:
        link = pix_link['href']
        pix_url = 'https://' + site + link
        content_type = site_urls[pix_url].get('content-type', '')
        content_type = content_type.strip()
        if link[-1] == '/':
            link = link[:-1]
        filename = link.rsplit('/')[-1]
        if content_type == 'image/jpeg':
            filename += '.jpg'
        else:
            filename += '.' + content_type.split('/')[1]
        local_file = '../pictures/' + filename
        #print(local_file)
        pix_link['href'] = pix_link['href'].replace(link, local_file)
        img_link = pix_link.find('img')
        img_url = img_link['src']
        img_link['src'] = img_link['src'].replace(img_url, local_file)

def cleanup_url(url): # in future this will be done in spider
        """
        Removes URL fragment that falsely make URLs look diffent.
        Subclasses can overload this method to perform other URL-normalizations.
        """
        url = urldefrag(url)[0]
        url_parts = urlparse(url)
        url_parts = url_parts._replace(path=url_parts.path.replace('//','/'))
        return url_parts.geturl()

def get_head_lines():
    head_lines = '''
    <link href="../assets/bootstrap.min.css" rel="stylesheet">
    <link href="../assets/style.css" rel="stylesheet">
    <link href="../assets/magnific-popup.min.css" rel="stylesheet">
    <link href="../assets/video-js.css" rel="stylesheet">
    <style>
        .h2Styled {
            color: #985735;
            border-bottom: 1px solid #97B0C8;
        }

        ul {
            padding-left: 40px;
        }

        ol {
            padding-left: 40px;
        }

        .newavailablecont h3 {
            text-align: center;
            color: #1e70bb;
            font-weight: 600;
            /*text-transform: capitalize;*/
            font-size: 24px;
            padding-bottom: 0px;
        }
    </style>
    '''
    return head_lines


def get_bottom_lines():
    bottom_lines = '''
    <script src="../assets/jquery.min.js"></script>
    <script src="../assets/bootstrap.min.js"></script>
    <script src="../assets/jquery.magnific-popup.min.js"></script>
    <script>
        $(document).ready(function () {
        $('.image-link').magnificPopup({ type: 'image' });
        });
    </script>
    '''
    return bottom_lines

if __name__ == "__main__":
    main(sys.argv)
