# -*- coding: utf-8 -*-
__author__ = 'Tural'

from data_structures import SortedDict

class PostAuthor(object):
    """Автор поста"""
    def __init__(self, name, image_url):
        self.name = name
        self.image_url = image_url

    def __cmp__(self, other):
        if self.name == other.name and self.image_url == other.image_url:
            return 0
        return 1

class CommentPostInfo(object):
    """Информация о комментарии"""
    def __init__(self, id, author, date, text):
        self.id = id
        self.author = author
        self.date = date
        self.text = text
        self._is_new = False

    def get_is_new(self):
        return self._is_new

    def set_is_new(self, value):
        self._is_new = value

    is_new = property( get_is_new, set_is_new, doc=u'Свойство-флаг новизны сообщения ответа' )

    def __cmp__(self, other):
        if self.id == other.id and self.author == other.author and \
            self.date == other.date and self.text == other.text:
            return 0
        return 1

class PostInfo(CommentPostInfo):
    """Информация о посте"""
    def __init__(self, id, author, date, text):
        CommentPostInfo.__init__( self, id, author, date, text )
        self.replies = SortedDict() #посты - ответы на пост

    def get_is_new(self):
        return self._is_new

    def set_is_new(self, value):
        self._is_new = value
        if value:
            for reply in self.replies:
                reply.is_new = True

    is_new = property( get_is_new, set_is_new, doc=u'Свойство-флаг новизны поста' )

    def __cmp__(self, other):
        if self.id == other.id and self.author == other.author and \
            self.date == other.date and self.text == other.text and self.replies == other.replies:
            return 0
        return 1

    def add_reply(self, comment):
        """
            comment_id - идентификатор поста-комментария
            comment - CommentPostInfo комментария
        """
        self.replies[comment.id] = comment