from flask import Flask, render_template, url_for
from pymongo import MongoClient
from flask_bootstrap import Bootstrap
from test_controller import test_controller

app = Flask(__name__, static_url_path='/photo', static_folder='./photo')
# 在網址後面加上/test/test_controller就可以得到testcontroller.py裡面的東西，用來區分不同的頁面
# app.register_blueprint(test_controller, url_prefux='/test')

# 模板管理
bootstrap = Bootstrap(app)

# mongodb連線 (mongodb需增加ip才看得到)
mongodb_atlas_account = "adan7575"
mongodb_atlas_password = "adan7575"
client = MongoClient('mongodb+srv://{}:{}@twfruit.i2omj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'.format(mongodb_atlas_account, mongodb_atlas_password))
db = client.TWFruits

# 主頁
@app.route('/')
def index():
    return render_template('index.html')

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
    afa_news = db.afa_news
    news_data = [x for x in afa_news.find()]
    return render_template('news.html', data=news_data)

# 病蟲害防治
@app.route('/diseases')
def diseases():
    return 'diseases page'

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


if __name__ =='__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)   # 0.0.0.0 代表所有人都能訪問

