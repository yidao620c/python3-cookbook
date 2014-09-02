#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 排序不支持原生比较操作的对象
Desc : 
"""


class User:
    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return 'User({})'.format(self.user_id)


def sort_notcompare():
    users = [User(23), User(3), User(99)]
    print(users)
    print(sorted(users, key=lambda u: u.user_id))

    from operator import attrgetter
    print(sorted(users, key=attrgetter('user_id')))

    # print(sorted(users, key=attrgetter('last_name', 'first_name')))

    print(min(users, key=attrgetter('user_id')))
    print(max(users, key=attrgetter('user_id')))
if __name__ == '__main__':
    sort_notcompare()