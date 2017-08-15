#!/bin/python

import boto3
from pprint import pprint
import urllib2
import time
import os.path
import zipfile
import os, shutil

def main():
    installed = False

    while not installed:
        if internet_on():
            print "internet is on"
            build_str = get_latest_linux_build(bucket='fetchit')
            if not os.path.isfile("tmp/{}".format(build_str.split('/')[2])):
                download_file(build_str)
                clean_dir()
                install_fetchit("tmp/{}".format(build_str.split('/')[2]))
            else:
                print "no update required"
                break
            installed = True
            print "Done installing fetchit."
            time.sleep(2)
        else:
            print "no internet connection... connect to wifi before we continue"


    # print get_latest_linux_build()


def download_file(filename):
    s3 = boto3.resource('s3')
    s3.Bucket('fetchit').download_file(filename, "tmp/{}".format(filename.split('/')[2]))

def install_fetchit(filename):
    zip_ref = zipfile.ZipFile(filename, 'r')
    zip_ref.extractall("install")
    zip_ref.close()

def clean_dir():
    print 'clean dir'
    for the_file in os.listdir('install'):
        file_path = os.path.join('install', the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)


def internet_on():
    try:
        urllib2.urlopen('http://google.com', timeout=1)
        return True
    except urllib2.URLError as err:
        return False

def get_latest_linux_build(bucket = 'fetchit', contains = 'linux', prefix = 'stage'):
    filez = []
    s3 = boto3.client('s3')
    get_last_modified = lambda obj: int(obj['LastModified'].strftime('%s'))
    paginator = s3.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(
        Bucket=bucket,
        Prefix=prefix
    )

    for page in page_iterator:
        for s3file in page['Contents']:
            if contains in s3file['Key']:
                filez.append(s3file)

    return [obj['Key'] for obj in sorted(filez, key=get_last_modified, reverse=True)][0]


if __name__ == "__main__":
    main()
