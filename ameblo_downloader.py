#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib.request
import fileinput
import re
import os
import time
import random


# インデックスページから記事のURLを抜き出す
def get_url_lists(url):
  urls_kiji = set([])
  url_part = url.replace('entrylist.html','')
  with urllib.request.urlopen(url) as page:
    html = page.read().decode()
    iterator = re.finditer("href\=\"(" + url_part + "entry\-.+?\.html)\"\>", html)
    for match in iterator:
      urls_kiji.add(match.group(1))
  return urls_kiji

# 記事からImageURLを抜き出す
def get_image_list(kiji):
  urls_image = set([])
  for line in kiji:
    iterator = re.finditer("(\/user_images\/.*?(\..[A-Za-z]+))\"", kiji)
    for match in iterator:
      urls_image.add((match.group(1), match.group(2)))
  return urls_image

# ImageURLを保存
def get_image(image_lists, dirname, count):
  for image_url in image_lists:
    # image_url[0] : ImageURLの一部
    # image_url[1] : 拡張子
    url = "http://stat.ameba.jp" + image_url[0]
    print(url + "..."),
    with urllib.request.urlopen(url) as image:
      filename = os.path.normpath(dirname + "/" + "%03d" % (count) + image_url[1])
      with open(filename, "wb") as fw:
        fw.write(image.read())
        count += 1
    print("done")
    time.sleep(random.randint(1, 10))
  return count

# 記事のURLから記事をDL
def get_kiji(url):
  with urllib.request.urlopen(url_list) as page:
    html = page.read().decode()
  with open('done.txt', 'a') as f:
    f.write(url + "\n")
  return html

# ダウンロード済かチェックする
def is_download(url):
  if os.path.exists('done.txt'):
    with open('done.txt', 'r') as f:
      if url in f.read():
        return True
  return False

# ダウンロード情報をオープン
for line in fileinput.input():
  # ディレクトリ名から、記事のリストを取得
  dirname = line.replace('\n', '')
  # 先頭が'#'の場合はコメント
  if dirname[0] != '#':
    # ディレクトリを作成
    if not os.path.exists(dirname):
      os.mkdir(dirname)
    url = "http://ameblo.jp/" + dirname + "/entrylist.html"
    url_lists = get_url_lists(url)
    count = 0
    for url_list in url_lists:
      if not is_download(url_list):
        kiji = get_kiji(url_list)
        image_lists = get_image_list(kiji)
        count = get_image(image_lists, dirname, count)
      else:
        print(url_list + " is already downloaded.")
