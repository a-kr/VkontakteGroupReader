# coding: utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse

import login
from group_news_reader import VkontakteGroupNewsReader


def dispatch(request, arg):
    """ Django-вид. """
    groupwall = get_wall()
    return render_to_response("wall.html", 
        {'posts': groupwall.posts if groupwall else None}
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
        