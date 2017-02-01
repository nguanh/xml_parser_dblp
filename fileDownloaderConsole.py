import sys
from fileDownloader.fileDownloader import download_file

url = sys.argv[1]
storagePath = sys.argv[2]
download_file(url, storagePath)