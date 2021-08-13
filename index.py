from flask import Flask, render_template, url_for, request, jsonify
from flask_pymongo import PyMongo, pymongo
from pymongo import MongoClient
from flask_bootstrap import Bootstrap
from flask_paginate import Pagination, get_page_parameter
import matplotlib.pyplot as plt
import pandas as pd
import jieba
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from test_controller import test_controller

# mongodb連線 (mongodb需增加ip才看得到)
mongodb_atlas_account = "adan7575"
mongodb_atlas_password = "adan7575"
client = MongoClient('mongodb+srv://{}:{}@twfruit.i2omj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'.format(mongodb_atlas_account, mongodb_atlas_password))
db = client.TWFruits


def word_cloud(db_connect):
    # connect collection coa_news
    news = db_connect.news
    df_news = pd.DataFrame(list(news.find()))

    # 將content欄位資料轉成list後進行合併
    news_content = df_news['content'].tolist()
    jieba.set_dictionary('./Word_Dictionary/dict.txt')
    with open(file='Word_Dictionary/stop_words.txt', mode='r', encoding='utf-8') as file:
        stop_words = file.read().split('\n')

    seg_words_list = []
    for i in news_content:
        words = jieba.cut(i, cut_all=False)
        for s in words:
            if s.strip() in stop_words:
                pass
            elif s.strip() in [' ', '']:
                pass
            else:
                seg_words_list.append(s.strip())
    seg_words = ' '.join(seg_words_list)

    word_cloud = WordCloud(font_path='C:/Windows/Fonts/msjhbd.ttc').generate(seg_words)
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig('./static/word_cloud.png', bbox_inches='tight', pad_inches=0.0)
    return


app = Flask(__name__, static_url_path='/static', static_folder='./static')
# 在網址後面加上/test/test_controller就可以得到testcontroller.py裡面的東西，用來區分不同的頁面
# app.register_blueprint(test_controller, url_prefux='/test')

# 模板管理
bootstrap = Bootstrap(app)

# 產生文字雲
# word_cloud(db)


# 主頁(一開始進去的)
@app.route('/')
def index():
    return render_template('index.html')


# 主頁(點選主頁後)
@app.route('/main')
def main_page():
    return render_template('index.html')


# 價格預測
@app.route('/predict')
def predict():
    return render_template('predict.html')


# 圖表顯示農業資訊
@app.route('/information')
def information():
    return render_template('summary.html')


# 農業新聞
@app.route('/news')
def news():
    news = db.news
    page_index = request.args.get(get_page_parameter(), type=int, default=1)
    limit = 10  # 每頁10筆
    all_news = [x for x in news.find().sort('date', pymongo.DESCENDING)]
    news_data = []
    last_id = all_news[limit*(page_index-1)]['news_id']
    now = limit * (page_index-1)
    for i in range(limit):
        try:
            news_data.append(all_news[now+i])
        except:
            break
    print(last_id)

    pagination = Pagination(page=page_index, total=len(all_news), per_page_parameter=10, error_out=False, css_framework='bootstrap3')

    return render_template('news.html', posts=news_data, pagination=pagination)

    # posts = pagination.items
    # page = request.args.get(get_page_parameter(), type=int, default=1)
    # news_data = news.paginate(page, 30, False)

    # return jsonify({'news': news, 'start_id': 'starting_id', 'pre_url': prve_url, 'next_url': next_url})
    # return jsonify({'start_id': 'starting_id'})

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/other_link')
def other():
    return render_template('other_link.html')


@app.route('/marketing_price')
def marketing_price():
    return render_template('price.html')


@app.route('/origin_price')
def origin_price():
    return render_template('price.html')


# 病蟲害防治
@app.route('/diseases')
def diseases():
    return 'diseases page'


if __name__ =='__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)   # 0.0.0.0 代表所有人都能訪問

