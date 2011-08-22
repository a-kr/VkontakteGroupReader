# coding: utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse

import login
from group_news_reader import VkontakteGroupNewsReader
from post import PostInfo


def dispatch(request, arg):
    """ Django-вид. """
    if arg == '':
        groupwall = get_wall()
        return render_to_response("wall.html", 
            {'posts': groupwall.posts if groupwall else None}
        );
    elif arg.startswith('hidden_comments/'):
        post_id = arg.split('/')[1];
        comments = get_hidden_comments(post_id)
        return render_to_response("ajax_comments.html", 
            {'comments': comments}
        );
        
    
def get_wall():
    """ Возвращает GroupWall.
        Возможно, закешированный как-нить.
        
        В случае ошибки может вернуть None, это
        обрабатывается в шаблоне.
    """
    # Сейчас дергает сервер при каждом запросе
    vk = VkontakteGroupNewsReader(login.login, login.password, login.group_url)
    vk.get_posts()
    return vk.current_wall_posts
    
def get_hidden_comments(post_id):
    """ Возвращает набор скрытых комментов для указанного поста.
        Это тоже надо бы закешировать.
    """
    url = PostInfo.hidden_comments_url(post_id)
    comments = VkontakteGroupNewsReader.get_hidden_comments(url)
    return comments
    
        