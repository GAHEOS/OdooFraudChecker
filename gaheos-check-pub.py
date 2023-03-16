import csv
import os
import hashlib
import requests
import datetime
from difflib import SequenceMatcher

REPOS = []
REPO_MD5 = []
ANALYZED_DB = [
    'https://octupustech.com',
    'http://elbdarnel-2036481962.us-east-1.elb.amazonaws.com'
]
PUBLIC_URL = 'https://gaheos-repo.odoo.com'


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
    print("#############   gaheos-check-pub.py  #############")
    print("#############  %s   #############" % datetime.datetime.now().strftime('%Y-%m-%d %T'))
    print("##################################################")
    print('MD5-src.tsv hash: ', md5('MD5-src.tsv'))
    with open('MD5-src.tsv', 'r') as fp:
        for file_path, url_path, file_md5 in csv.reader(fp, delimiter='\t'):
            REPO_MD5.append(url_path)
    with open('MD5-check-pub.tsv', 'w') as fp:
        writer = csv.writer(fp, delimiter='\t')
        writer.writerow(["URL", "File Path", "GAHEOS MD5", "Analyzed MD5", "RESULT", "SIMILARITY", "SERVER DATE",
                         "SERVER LAST MODIFIED"])
        for url in ANALYZED_DB:
            for url_path in REPO_MD5:
                remote = requests.get(f'{url}/{url_path}')
                public = requests.get(f'{PUBLIC_URL}/{url_path}')
                if public.status_code == 200:
                    with open('md5-source-pub', 'wb') as tmp:
                        tmp.write(public.content)
                    if remote.status_code == 200:
                        with open('md5-target-pub', 'wb') as tmp:
                            tmp.write(remote.content)
                        row = [url,
                               url_path,
                               md5('md5-source-pub'),
                               md5('md5-target-pub'),
                               "Identico" if md5('md5-source-pub') == md5('md5-target-pub') else "Similar",
                               similarity('md5-source-pub', 'md5-target-pub'), remote.headers['Date'],
                               remote.headers['Last-Modified']]
                        writer.writerow(row)
    print('MD5-check-pub.tsv hash: ', md5('MD5-check-pub.tsv'))
