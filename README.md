# yiff.party-media-scraper
This is a python code to scrape contents from the site yiff.party.

All you need to do,is give the yiff.party url of the creator.
All the available contents will be downloaded in 'YIFF' folder in 'Downloads'.

You have to run this code in the intrpreter and interact accordingly.

The URL should be of the form: https://yiff.party/patreon/XYZ; where XYZ is the user code on the site.

Options Available:

DOWNLOAD: Downloads the content of that user.

If there already exists a directory for the user,then the program will ask you if you want to re-download all the contents from the user, or just update it.

RE-DOWNLOAD:  Pressing 'd' will lead to re-download.It will do the same stuff as download all over again. If any file is missing or corrupted,then you should use this option.

UPDATE: Pressing 'u' will lead to updating of the current folder. It will start downloading content from the most recent post and continue to older posts until it finds a file that already exists.

There is a sleep time between downloading content from each post, which is in place to not overuse the resources of the site,and also to delay or avoid being detected as an automated service.
