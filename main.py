# -*- coding: utf-8 -*-

import os
import pandas as pd
from datetime import datetime
from utils import news_crawler
from utils import preprocessing

project_path = os.path.dirname(os.path.realpath(__file__))  # 获取项目路径
news_path = os.path.join(project_path, 'news')  # 新闻数据存放目录路径
if not os.path.exists(news_path):  # 创建news文件夹
    os.mkdir(news_path)

sina_news_df = news_crawler.get_latest_news('sina', top=60, show_content=True)
sohu_news_df = news_crawler.get_latest_news('sohu', top=10, show_content=True)
xinhuanet_news_df = news_crawler.get_latest_news('xinhuanet', top=10, show_content=True)

news_crawler.save_news(sina_news_df, os.path.join(news_path, 'sina_latest_news.csv'))
news_crawler.save_news(sohu_news_df, os.path.join(news_path, 'sohu_latest_news.csv'))
news_crawler.save_news(xinhuanet_news_df, os.path.join(news_path, 'xinhuanet_latest_news.csv'))

news_df = pd.concat([sina_news_df, sohu_news_df, xinhuanet_news_df], ignore_index=True)
news_df = preprocessing.data_filter(news_df)
# last_time = datetime.today().strftime('%Y-%m-%d %H:%M')  # format like '2018-04-06 23:59'
# news_df = preprocessing.get_data(news_df, last_time=last_time, delta=5)
news_df['content'] = news_df['content'].map(lambda x: preprocessing.clean_content(x))

news_crawler.save_news(news_df, os.path.join(news_path, 'latest_news.csv'))
