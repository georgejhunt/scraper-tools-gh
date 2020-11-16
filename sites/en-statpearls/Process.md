## Processing StatPearls.com

1. Run scan-statpearls.py This will analyze the site to determine the size of various types of content and download any html to the raw subdirectory.
It will also create json files will all pages, urls, and other statistics.
2. Run dnload_images.py and dnload_media.py to get the image and video files.
3. Run conv_html.py. This will fix up urls and simplify all the html pages.
4. Run make-zim.sh. This will create a zim file.
5. Add the zim to library.xml using iiab-make-kiwix-lib and use the resulting xml for iiab-library.xml
