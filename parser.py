#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import hashlib

from lxml import etree


__author__ = 'ChukovNA'


def init():
    global search_location
    search_location = "/home/nikitos/Downloads/S.T.A.L.K.E.R__[rutracker.org]/fb2/"
    global search_mask
    # search_mask="26 - Sergey Paliy - Bumerang.fb2"
    search_mask = ".fb2"
    global ns
    ns = "{http://www.gribuser.ru/xml/fictionbook/2.0}"


def find_files_by_mask(location, mask):
    find_files = []
    for root, dirs, files in os.walk(location):
        for file in files:
            if file.endswith(mask):
                find_files += [[os.path.join(root, file),
                                hashlib.md5(open(os.path.join(root, file), 'rb').read()).hexdigest().upper()]]
    return find_files


def check_file_md5(md5):
    return True


def parse_files(files):
    for file in files[:]:
        # print(file[0])
        if check_file_md5(file[1]):
            try:
                parser = etree.XMLParser(recover=True)
                book = etree.parse(file[0], parser)
                Authors = []
                Book = {}
                Annotation = ""

                description = book.getroot().find(ns + "description/")

                Book = {"md5": file[1]}

                for title in description.findall(ns + "book-title"):
                    Book["title"] = title.text

                for author in description.findall(ns + "author"):
                    Author = {}
                    author_first_name = author.find(ns + "first-name")
                    if author_first_name is not None:
                        Author['author_first_name'] = author_first_name.text
                    author_last_name = author.find(ns + "last-name")
                    if author_last_name is not None:
                        Author['author_last_name'] = author_last_name.text
                    author_middle_name = author.find(ns + "middle-name")
                    if author_middle_name is not None:
                        Author['author_middle_name'] = author_middle_name.text
                    Authors.append(Author)
                    Book["Autors"] = Authors

                for annotation in description.findall(ns + "annotation"):
                    for child in annotation:
                        if (child is not None) and child.text:
                            Annotation += child.text
                            Book["Annotation"] = Annotation

                print(Book)

            except:

                pass
        # todo: Exception Handling

        else:
            print("re")

            # todo: repeat action


def main():
    init()

    files = find_files_by_mask(search_location, search_mask)
    parse_files(files)


if __name__ == "__main__":
    main()


