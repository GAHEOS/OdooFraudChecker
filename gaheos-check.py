import csv
import os
import hashlib
import requests
import datetime
from difflib import SequenceMatcher

REPOS = []
REPO_MD5 = {}
ANALYZED_DB = [
    'https://octupustech.com',
    'http://elbdarnel-2036481962.us-east-1.elb.amazonaws.com'
]


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def similarity(file1, file2):
    text1 = open(file1, 'rb').read()
    text2 = open(file2, 'rb').read()
    try:
        m = SequenceMatcher(None, text1, text2)
        return m.ratio()
    except Exception:
        return "SKIP"


if __name__ == '__main__':
    print("##################################################")
    print("#############     gaheos-check.py    #############")
    print("#############  %s   #############" % datetime.datetime.now().strftime('%Y-%m-%d %T'))
    print("##################################################")
    print('MD5-src.tsv hash: ', md5('MD5-src.tsv'))
    with open('MD5-src.tsv', 'r') as fp:
        for file_path, url_path, file_md5 in csv.reader(fp, delimiter='\t'):
            REPO_MD5[url_path] = [file_path, file_md5]
    with open('MD5-check.tsv', 'w') as fp:
        writer = csv.writer(fp, delimiter='\t')
        writer.writerow(["URL", "File Path", "GAHEOS MD5", "Analyzed MD5", "RESULT", "SIMILARITY", "SERVER DATE",
                         "SERVER LAST MODIFIED"])
        for url in ANALYZED_DB:
            for url_path, [file_path, md5_hash] in REPO_MD5.items():
                response = requests.get(f'{url}/{url_path}')
                if response.status_code == 200:
                    with open('md5-target', 'wb') as tmp:
                        tmp.write(response.content)
                    row = [url,
                           url_path,
                           md5(file_path),
                           md5('md5-target'),
                           "Identico" if md5(file_path) == md5('md5-target') else "Similar",
                           similarity(file_path, 'md5-target'), response.headers['Date'],
                           response.headers['Last-Modified']]
                    writer.writerow(row)
    print('MD5-check.tsv hash: ', md5('MD5-check.tsv'))
