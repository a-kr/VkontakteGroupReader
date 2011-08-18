# coding: utf-8
import os

from group_news_reader import VkontakteGroupNewsReader
import time
import login

__author__ = 'Tural'

def get_online_tests():
    try:
        vk = VkontakteGroupNewsReader( login.login, login.password, login.group_url )
        for i in range(2):
            vk.get_posts()
            time.sleep(120)
    except Exception as e:
        print e

def check_comparasion():
    path0 = os.path.normpath(
        os.path.join(
            os.getcwd(), "..", "vkontakte_group_small.html" ) )
    f0 = open( path0, "r" )
    wall0 = VkontakteGroupNewsReader.parse_response(f0)
    f0.close()

    path1 = os.path.normpath(
        os.path.join(
            os.getcwd(), "..", "vkontakte_group.html" ) )
    f1 = open( path1, "r" )
    wall1 = VkontakteGroupNewsReader.parse_response(f1)
    f1.close()

    wall1.check_for_new_posts_and_comments( wall0 )

if __name__ == '__main__':
    check_comparasion()
