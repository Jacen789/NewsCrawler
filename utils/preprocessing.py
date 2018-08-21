# -*- coding: utf-8 -*-

import re
# import opencc
import jieba
import json
from datetime import datetime
from datetime import timedelta


def data_filter(df):
    """数据过滤"""
    # 过滤掉没有内容的新闻
    df = df[df['content'] != ''].copy()
    df = df.dropna(subset=['content']).copy()
    # 去重
    df = df.drop_duplicates(subset=['url'])
    df = df.reset_index(drop=True)
    return df


def get_data(df, last_time, delta):
    """
    获取某段时间的新闻数据
    :param df: 原始数据
    :param last_time: 指定要获取数据的最后时间
    :param delta: 时间间隔
    :return: last_time前timedelta的数据
    """
    last_time = datetime.strptime(last_time, '%Y-%m-%d %H:%M')
    delta = timedelta(delta)
    df['time'] = df['time'].map(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M'))
    df = df[df['time'].map(lambda x: (x <= last_time) and (x > last_time - delta))].copy()
    df = df.sort_values(by=['time'], ascending=[0])
    df['time'] = df['time'].map(lambda x: datetime.strftime(x, '%Y-%m-%d %H:%M'))
    df = df.reset_index(drop=True)
    return df


def clean_content(content):
    """清理新闻内容"""
    # 清理未知字符和空白字符
    content = re.sub(r'\?+', ' ', content)
    content = re.sub(r'( *\n+)+', '\n', content)
    content = re.sub(r'\u3000', '', content)
    # 清理责任编辑
    content = content.split('\n责任编辑')[0]
    content = content.split('返回搜狐，查看更多')[0]
    # 中文繁体转简体
    # x = opencc.OpenCC('t2s').convert(x)
    # 英文大写转小写
    content = content.lower()
    # 提取数字英文中文
    content = re.sub(r'[^0-9A-Za-z\u4E00-\u9FFF]+', ' ', content)
    return content


def userdict_cut(x, userdict_path):
    # 用户词词典
    jieba.load_userdict(userdict_path)
    words = jieba.cut(x)
    return words


def stop_words_cut(words, stop_words_path):
    # 停用词处理
    with open(stop_words_path, 'r', encoding='utf-8') as f:
        stopwords = [line.strip() for line in f.readlines()]
        stopwords.append(' ')
        words = [word for word in words if word not in stopwords]
    return words


def disambiguation_cut(words, disambiguation_dict_path):
    # 消歧词典
    with open(disambiguation_dict_path, 'r', encoding='utf-8') as f:
        disambiguation_dict = json.load(f)
        words = [(disambiguation_dict[word] if disambiguation_dict.get(word) else word) for word in words]
    return words


def individual_character_cut(words, individual_character_dict_path):
    # 删除无用单字
    with open(individual_character_dict_path, 'r', encoding='utf-8') as f:
        individual_character = [line.strip() for line in f.readlines()]
        words = [word for word in words if ((len(word) > 1) or ((len(word) == 1) and (word in individual_character)))]
    return words
