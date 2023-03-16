import os
import csv
import hashlib
import datetime
from collections import OrderedDict

REPOS = []
REPO_MD5 = OrderedDict()

# SE EXLUYEN LOS MÓDULOS DETECTADOS PERO NO SON PARTE DE LITIGIO
APP_EXCLUDED = ['sh_event_seat_booking', 'account_reconciliation', 'deltatech_invoice_receipt',
                'account_dynamic_reports', 'website_customer_location_app', 'deltatech_no_quick_create',
                'stock_kardex_audit', 'stock_no_negative', '/fonts/']


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


if __name__ == '__main__':
    print("##################################################")
    print("#############      gaheos-md5.py     #############")
    print("#############  %s   #############" % datetime.datetime.now().strftime('%Y-%m-%d %T'))
    print("##################################################")
    print('repositories.tsv hash: ', md5('repositories.tsv'))
    with open('repositories.tsv', 'r') as fp:
        for row in csv.reader(fp):
            REPOS.append(row)
    for root, dirs, files in os.walk(".", topdown=False):
        if '/static/' in root:
            for name in files:
                filename = os.path.join(root, name)
                file_path = filename.split('/', 2)
                module_file = file_path[2]
                exclude_file = False
                for excluded in APP_EXCLUDED:
                    if excluded in filename:
                        exclude_file = True
                if exclude_file:
                    continue
                REPO_MD5[module_file] = [filename, md5(filename)]
    with open('MD5-src.tsv', 'w') as fp:
        writer = csv.writer(fp, delimiter='\t')
        for url_path, [filename, md5_hash] in REPO_MD5.items():
            writer.writerow([filename, url_path, md5_hash])
    print('MD5-src.tsv hash: ', md5('MD5-src.tsv'))
