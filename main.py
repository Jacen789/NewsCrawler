# -*- coding: utf-8 -*-

import os
import pandas as pd
from datetime import datetime
from utils import news_crawler
from utils import preprocessing

# 获取项目路径
project_path = os.path.dirname(os.path.realpath(__file__))
# 获取数据存放目录路径
data_path = os.path.join(project_path, 'data')
news_path = os.path.join(data_path, 'news')
extra_dict_path = os.path.join(data_path, 'extra_dict')

sina_news_df = news_crawler.get_latest_news('sina', top=60, show_content=True)
sohu_news_df = news_crawler.get_latest_news('sohu', top=10, show_content=True)
xinhuanet_news_df = news_crawler.get_latest_news('xinhuanet', top=10, show_content=True)

news_crawler.save_news(sina_news_df, os.path.join(news_path, 'sina_latest_news.csv'))
news_crawler.save_news(sohu_news_df, os.path.join(news_path, 'sohu_latest_news.csv'))
news_crawler.save_news(xinhuanet_news_df, os.path.join(news_path, 'xinhuanet_latest_news.csv'))
# sina_news_df = news_crawler.load_news(os.path.join(news_path, 'sina_latest_news.csv'))
# sohu_news_df = news_crawler.load_news(os.path.join(news_path, 'sohu_latest_news.csv'))
# xinhuanet_news_df = news_crawler.load_news(os.path.join(news_path, 'xinhuanet_latest_news.csv'))

news_df = pd.concat([sina_news_df, sohu_news_df, xinhuanet_news_df], ignore_index=True)
news_df = preprocessing.data_filter(news_df)
last_time = datetime.today().strftime('%Y-%m-%d %H:%M')  # format like '2018-04-06 23:59'
news_df = preprocessing.get_data(news_df, last_time=last_time, delta=5)
news_df['content'] = news_df['content'].map(lambda x: preprocessing.clean_content(x))

news_crawler.save_news(news_df, os.path.join(news_path, 'latest_news.csv'))
# news_df = news_crawler.load_news(os.path.join(news_path, 'latest_news.csv'))


def content_cut_process(x):
    """
    新闻内容文本分词
    :param x: 原始新闻内容文本
    :return: 分词之后的列表
    """
    # 会话内容分词
    words = preprocessing.userdict_cut(x, os.path.join(extra_dict_path, 'userdict.txt'))  # 用户词分词
    words = preprocessing.stop_words_cut(words, os.path.join(extra_dict_path, 'stop_words.txt'))  # 停用词剔除
    # words = preprocessing.disambiguation_cut(
    #     words,
    #     os.path.join(extra_dict_path, 'disambiguation_dict.json'))  # 消歧词典消歧转换
    # words = preprocessing.individual_character_cut(
    #     words,
    #     os.path.join(extra_dict_path, 'individual_character_dict.txt'))  # 剔除单字，但保留特殊单字
    return words


news_df['title_cut'] = news_df['title'].map(content_cut_process)
news_df['content_cut'] = news_df['content'].map(content_cut_process)
news_crawler.save_news(news_df, os.path.join(news_path, 'latest_news_cut.csv'))
