#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module."""
## https://mongo-thingy.readthedocs.io/reference.html#module-mongo_thingy.cursor
import inspect

from bapy import ic
from mongo_thingy import connect, Thingy, create_indexes
from mongo_thingy.versioned import Versioned


connect("mongodb://localhost/test")


# BEGIN: MIO
class IP(Thingy):
    pass


ip = IP({"ipv4": "192.168", "ipv6": "12:22"}).save()

pen_db = IP.get_database()
ip_col = pen_db.ip
for item in ip_col.find():
    ic(item['ipv4'])

# o:

ic(IP.add_view(name='ipv4', defaults=False, include='ipv4'))
for item in ic(IP.find().view('ipv4')):
    ic(item['ipv4'])

ic(IP.add_view(name='ipv4', defaults=True, include='ipv4'))
for item in ic(IP.find().view('ipv4')):
    ic(item)
# END: MIO


# BEGIN: MIO
class IP(Thingy):
    pass


ip = IP({"ipv4": "192.168", "ipv6": "12:22"}).save()

old = dict(ipv4='192.168')
old_doc = ic(IP.find_one(dict(ipv4='192.168')))
ic(old_doc)

ip_collection = IP.get_collection()
ic(ip_collection)
old_document = ip_collection.find_one(dict(ipv4='192.168'))
ic(old_document)

if old_document.get('PTR', 'Not Found') == 'Not Found':
    ic('Not Found')

new_document = dict(**old_document, location='madrid')
new = ic(IP.find_one_and_replace(filter=old_document, replacement=new_document))
ic(new)

test = ip_collection.find_one(dict(location='madrid'))
ic(test)
# END: MIO


class User(Thingy):
    pass


user = User({"name": "Mr. Foo", "age": 42}).save()


ic(User.count())
ic(User.find_one({"age": 42}))

ic(user.age)
user.age = 1337

ic(user.save())


class User(Thingy):
    @property
    def username(self):
        return "".join(char for char in self.name if char.isalpha())


ic(User.add_view(name="everything", defaults=True, include="username"))
user = ic(User.find_one())
ic(user.view("everything"))

ic(User.add_view(name="public", defaults=True, exclude="password"))
user.password = "t0ps3cr3t"
ic(user.view())
ic(user.view("public"))

ic(User.add_view(name="credentials", include=["username", "password"]))
ic(user.view("credentials"))

for credentials in User.find().view("credentials"):
    ic(credentials)


class Article(Versioned, Thingy):
    pass


article = Article(content="Cogito ergo sum")
ic(article.version)
ic(article.save())
ic(article.version)

article.content = "Sum ergo cogito"
ic(article.save())
ic(article.version)

ic(article.revert())
ic(article.version)

class AuthenticationGroup(Thingy):
    pass

connect("mongodb://localhost/")
ic(AuthenticationGroup.collection)

class Foo(Thingy):
    collection_name = "bar"

db = Foo()  ## ???

class Foo(Thingy):
    collection = db.bar


ic(Foo.collection)

ic(User.create_index("email", sparse=True, unique=True))

ic(User.add_index("email", sparse=True, unique=True))
ic(User.create_indexes())
ic(create_indexes())
ic(User)
user = ic(User())

__all__ = [item for item in globals() if not item.startswith('_') and not inspect.ismodule(globals().get(item))]
