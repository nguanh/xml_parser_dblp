import urllib.request


url1 = 'http://dblp.uni-trier.de/xml/dblp.xml.gz'
url2 = 'http://dblp.uni-trier.de/xml/dblp.dtd'
url3 = 'http://dblp.uni-trier.de/xml/docu/Person.java'


def progress_bar(blocks_transferred, block_size, total_size):
    """
    Function for displaying progress on currently downloaded file
    :param blocks_transferred:
    :param block_size:
    :param total_size:
    :return:
    """
    currentPercentage = min((blocks_transferred*block_size)*100//total_size,100)
    previousPercentage = 0
    if blocks_transferred > 0:
        previousPercentage = ((blocks_transferred-1)*block_size)*100//total_size

    # only print progress if percentage value has changed
    if currentPercentage-previousPercentage > 0:
        print("{}% downloaded".format(currentPercentage))


def download_file(file_url, storage_path):
    """
    :param file_url:
    :param storage_path:
    :return:
    """
    try:
        local_filename, headers = urllib.request.urlretrieve(file_url, storage_path, reporthook=progress_bar)
    except ValueError:
        print("Invalid URL")
    else:
        print(local_filename)
        print(headers)

'''
TODO
user agent
exception handling
return values
Check content type
'''
url = url2
storagePath = 'dblp.dtd'

download_file(url, storagePath)


