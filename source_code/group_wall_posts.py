# -*- coding:utf-8 -*-
__author__ = 'Tural'

from data_structures import SortedDict

class GroupWall(object):
    def __init__(self):
        self.posts = SortedDict()

    def add_new_post(self, post):
        """
            post_id - идентификатор поста
            post - PostInfo комментария
        """
        self.posts[post.id] = post

    def check_for_new_posts_and_comments(self, wall):
        """Сравнивает текущее состояние стены с состоянием стены переданным через
         параметр wall. В случае, если состояния одинаковы, возвращает False иначе
         проставляет новым запиясям флаг is_new и возвращает True"""
        has_something_new = False
        for post_id, post in self.posts.iteritems():
            #проверка является ли пост новым
            if not wall.posts.has_key( post_id ):
                post.is_new = True
                has_something_new = True
            else:
                for reply_id, reply in post.replies.iteritems():
                    if not wall.posts[post_id].replies.has_key(reply_id):
                        reply.is_new = True
                        has_something_new = True
        return has_something_new

    def __cmp__(self, other):
        if self.posts == other.posts:
            return 0
        return 1