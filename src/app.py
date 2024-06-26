#coding: utf-8

from flask import Flask, render_template, request, abort, jsonify
import requests
import json
import MySQLdb
from datetime import datetime, timedelta
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, FollowEvent)

app = Flask(__name__)

#json読み込み
with open('secret.json') as f:
    info = json.load(f)

# 予算入力フォーム表示
@app.route('/budget')
def budget():
    return render_template('html/Yosan_Form.html')

# 支出入力フォーム表示
@app.route('/spending')
def spending():
    return render_template('html/Shukkin_Form.html')

# 月別支出履歴表示
@app.route('/spending_month')
def spending_month():
    php_server_url = 'https://aso2201030.verse.jp/src/templates/php/Savemoney_m.php'
    php_response = requests.get(php_server_url)
    return php_response.content, php_response.status_code

@app.route('/displayGraph_<string:page>', methods = ['POST'])
def displayGraph(page):
    if request.method == 'POST':
        connect = MySQLdb.connect(
            host = info['server'],
            user = info['user'],
            passwd = info['pass'],
            db = info['db'],
            use_unicode = True,
            charset = 'utf8'
        )
        cursor = connect.cursor(MySQLdb.cursors.DictCursor)

        jsonData = request.get_json()
        spendingSum = {}
        today = datetime.now()
        sWeek = today - timedelta(days = today.weekday())
        eWeek = sWeek + timedelta(days = 6)
        day = ''

        cursor.execute(f"SELECT * FROM History WHERE user_id='{jsonData['id']}'")
        rows = cursor.fetchall()
        for row in rows:
            if page == 'month':
                if today.month == row['torokubi'].month:
                    day = row['torokubi'].day
            elif page == 'year':
                if today.year == row['torokubi'].year:
                    day = row['torokubi'].month
            elif page == 'week':
                try:
                    compare = datetime(row['torokubi'].year, row['torokubi'].month, row['torokubi'].day)
                    if sWeek <= compare <= eWeek:
                        day = row['torokubi'].day
                except Exception as e:
                    t =  f"{e.__class__.__name__}: {e}"
                    return render_template('html/error.html', error = t)

            money = row['money']
            if day in spendingSum:
                spendingSum[day] += money
            else:
                spendingSum[day] = money

        post_data = [{"day": k, "money": v} for k, v in spendingSum.items()]
        post = jsonify(post_data)

        cursor.close()
        connect.close()

        return post

@app.route('/displayBudget', methods = ['POST'])
def displayBudget():
    connect = MySQLdb.connect(
        host = info['server'],
        user = info['user'],
        passwd = info['pass'],
        db = info['db'],
        use_unicode = True,
        charset = 'utf8'
    )
    cursor = connect.cursor(MySQLdb.cursors.DictCursor)

    jsonData = request.get_json()
    budget = 0
    spending = 0
    today = datetime.now().date()

    cursor.execute('SELECT * FROM Yosan')
    rows = cursor.fetchall()
    for row in rows:
        if row['user_id'] == jsonData['id'] and today.month == row['torokubi'].month:
            budget = row['zandaka']

    cursor.execute('SELECT * FROM History')
    cols = cursor.fetchall()
    for col in cols:
        if col['user_id'] == jsonData['id'] and today.month == col['torokubi'].month:
            spending += col['money']

    post = jsonify(budget - spending)

    connect.commit()
    cursor.close()
    connect.close()

    return post

@app.route('/displaySaving', methods = ['POST'])
def displaySaving():
    connect = MySQLdb.connect(
        host = info['server'],
        user = info['user'],
        passwd = info['pass'],
        db = info['db'],
        use_unicode = True,
        charset = 'utf8'
    )
    cursor = connect.cursor(MySQLdb.cursors.DictCursor)

    jsonData = request.get_json()
    total = 0

    cursor.execute(f"SELECT * FROM Tyokin WHERE user_id='{jsonData['id']}'")
    rows = cursor.fetchall()
    for row in rows:
        total += row['tyokin']

    post = jsonify(total)

    connect.commit()
    cursor.close()
    connect.close()

    return post

@app.route('/displaySpending_<string:page>', methods = ['POST'])
def displaySpending(page):
    connect = MySQLdb.connect(
        host = info['server'],
        user = info['user'],
        passwd = info['pass'],
        db = info['db'],
        use_unicode = True,
        charset = 'utf8'
    )
    cursor = connect.cursor(MySQLdb.cursors.DictCursor)

    jsonData = request.get_json()
    date = []
    category = []
    money = []
    today = datetime.now()
    sWeek = today - timedelta(days = today.weekday())
    eWeek = sWeek + timedelta(days = 6)

    cursor.execute(f"SELECT * FROM History WHERE user_id='{jsonData['id']}'")
    rows = cursor.fetchall()
    for row in rows:
        if page == 'month':
            if today.month == row['torokubi'].month:
                date.append(f"{row['torokubi'].month}/{row['torokubi'].day}")
                category.append(row['category'])
                money.append(row['money'])
        elif page == 'year':
            if today.year == row['torokubi'].year:
                date.append(row['torokubi'].month)
                category.append(row['category'])
                money.append(row['money'])
        elif page == 'week':
            compare = datetime(row['torokubi'].year, row['torokubi'].month, row['torokubi'].day)
            if sWeek <= compare <= eWeek:
                date.append(f"{row['torokubi'].month}/{row['torokubi'].day}")
                category.append(row['category'])
                money.append(row['money'])

    postData = [date, category, money]
    post = jsonify(postData)

    connect.commit()
    cursor.close()
    connect.close()

    return post

# 年間支出履歴表示
@app.route('/spending_year')
def spending_year():
    php_server_url = 'https://aso2201030.verse.jp/src/templates/php/Savemoney_y.php'
    php_response = requests.get(php_server_url)
    return php_response.content, php_response.status_code

# 週間支出履歴表示
@app.route('/spending_week')
def spending_week():
    php_server_url = 'https://aso2201030.verse.jp/src/templates/php/Savemoney_w.php'
    php_response = requests.get(php_server_url)
    return php_response.content, php_response.status_code

# 月間貯金履歴表示
@app.route('/saving_month')
def saving_month():
    php_server_url = 'https://aso2201030.verse.jp/src/templates/php/Wallet_m.php'
    php_response = requests.get(php_server_url)
    return php_response.content, php_response.status_code

# 年間貯金履歴表示
@app.route('/saving_year')
def saving_year():
    php_server_url = 'https://aso2201030.verse.jp/src/templates/php/Wallet_y.php'
    php_response = requests.get(php_server_url)
    return php_response.content, php_response.status_code

@app.route('/graphDisplay_<string:page>', methods = ['POST'])
def graphDisplay(page):
    connect = MySQLdb.connect(
        host = info['server'],
        user = info['user'],
        passwd = info['pass'],
        db = info['db'],
        use_unicode = True,
        charset = 'utf8'
    )
    cursor = connect.cursor(MySQLdb.cursors.DictCursor)

    jsonData = request.get_json()
    today = datetime.now().date()
    day = ''
    money = 0
    savingSum = {}

    cursor.execute(f"select * from Tyokin where user_id='{jsonData['id']}'")
    rows = cursor.fetchall()

    for row in rows:
        if page == 'month':
            if row['torokubi'].year == today.year:
                day = row['torokubi'].month - 1

        elif page == 'year':
            current = today.year
            years = [current - i for i in range(5)]

            try:
                for year in years:
                    if year == row['torokubi'].year:
                        day = year
            except Exception as e:
                t =  f"{e.__class__.__name__}: {e}"
                return render_template('html/error.html', error = t)

        money = row['tyokin']

        if day in savingSum:
            savingSum[day] += money
        else:
            savingSum[day] = money

    postData = [{"day": k, "money": v} for k, v in savingSum.items()]
    post = jsonify(postData)

    cursor.close()
    connect.close()

    return post

@app.route('/savingDisplay_<string:page>', methods = ['POST'])
def spendingDisplay(page):
    connect = MySQLdb.connect(
        host = info['server'],
        user = info['user'],
        passwd = info['pass'],
        db = info['db'],
        use_unicode = True,
        charset = 'utf8'
    )
    cursor = connect.cursor(MySQLdb.cursors.DictCursor)

    jsonData = request.get_json()
    today = datetime.now().date()
    date = []
    money = []

    cursor.execute(f"select * from Tyokin where user_id='{jsonData['id']}'")
    rows = cursor.fetchall()
    for row in rows:
        if page == 'month':
            if row['torokubi'].year == today.year:
                date.append(row['torokubi'].month - 1)
                money.append(row['tyokin'])

        elif page == 'year':
            current = today.year
            years = [current - i for i in range(5)]

            for year in years:
                if year == row['torokubi'].year:
                    date.append(row['torokubi'].year)
                    money.append(row['tyokin'])

    postData = [date, money]
    post = jsonify(postData)

    connect.commit()
    cursor.close()
    connect.close()

    return post


#データベース接続
@app.route('/in_<int:page>', methods = ['POST'])
def connectDB(page):
    try:
        connect = MySQLdb.connect(
            host = info['server'],
            user = info['user'],
            passwd = info['pass'],
            db = info['db'],
            use_unicode = True,
            charset = 'utf8'
        )
        cursor = connect.cursor(MySQLdb.cursors.DictCursor)
    except Exception as e:
            t =  f"{e.__class__.__name__}: {e}"
            return render_template('html/error.html', error = t)

    #予算入力
    if page == 1:
        budget_userID = request.form.get('budget_userID')#フォームより取得
        budget_money = request.form.get('money')
        budget = int(budget_money)
        today = datetime.now().date()

        try:
            query = f"SELECT * FROM Yosan WHERE user_id='{budget_userID}'" #予算
            cursor.execute(query)
            rows = cursor.fetchall()
        except Exception as e:
            t =  f"{e.__class__.__name__}: {e}"
            return render_template('html/error.html', error = t)

        #初回利用
        if len(rows) == 0:
            try:
                sql2 = f"INSERT INTO Yosan VALUES ('{budget_userID}', {budget}, '{today}')" #予算登録
                cursor.execute(sql2)
            except Exception as e:
                t =  f"{e.__class__.__name__}: {e}"
                return render_template('html/error.html', error = t)
        else:
            #レコードが存在する(2回目以降の利用)
            try:
                query2 = f"SELECT * FROM History WHERE user_id='{budget_userID}'" #支出履歴
                cursor.execute(query2)
                rows3 = cursor.fetchall()
            except Exception as e:
                t =  f"{e.__class__.__name__}: {e}"
                return render_template('html/error.html', error = t)

            try:
                for row in rows:
                    total = 0
                    text = ''
                    if (today.year == row['torokubi'].year and today.month > row['torokubi'].month) or today.year > row['torokubi'].year:
                        for row3 in rows3:
                            total += row3['money']

                        total = budget - total
                        if total < 0:
                            total = 0
                        sql3 = f"INSERT INTO Tyokin(user_id, tyokin, torokubi) VALUES('{budget_userID}', {total}, {today})"
                        cursor.execute(sql3)

                        text = f"{int(today.month) - 1}月の貯金額は{total}円でした！"
                        line_bot_api.push_message(
                            budget_userID,
                            TextSendMessage(text = text)
                        )
            except Exception as e:
                t =  f"{e.__class__.__name__}: {e}"
                return render_template('html/error.html', error = t)

            try:
                sql5 = f"UPDATE Yosan SET zandaka={budget}, torokubi='{today}' WHERE user_id='{budget_userID}'"
                cursor.execute(sql5)
            except Exception as e:
                t =  f"{e.__class__.__name__}: {e}"
                return render_template('html/error.html', error = t)

        connect.commit()
        cursor.close()
        connect.close()

        return render_template('html/Yosan_Complete.html')


    #支出入力
    elif page == 2:
        spending_userID = request.form.get('spending_userID')
        categoryNumber = request.form.get('category')
        category = ''
        if categoryNumber == '1':
            category = '食費'
        elif categoryNumber == '2':
            category = '交通費'
        elif categoryNumber == '3':
            category = '日用品費'
        elif categoryNumber == '4':
            category = '被服費'
        elif categoryNumber == '5':
            category = '娯楽費'
        spending_money = request.form.get('money')
        spending = int(spending_money)
        today = datetime.now().date()

        try:
            cursor.execute('INSERT INTO History(user_id, category, money, torokubi) VALUES(%s, %s, %s, %s)', (spending_userID, category, spending, today))
        except Exception as e:
            t = e.__class__.__name__
            return render_template('html/error.html', error = t)

        #Messaging APIでの処理
        a = 0
        b = 0
        total = 0
        text = ''

        cursor.execute('SELECT * FROM Yosan')
        a1 = cursor.fetchall()
        for a2 in a1:
            if a2['user_id'] == spending_userID:
                a = a2['zandaka']

        cursor.execute('SELECT * FROM History')
        b1 = cursor.fetchall()
        for b2 in b1:
            if b2['user_id'] == spending_userID:
                if b2['torokubi'].month == today.month:
                    b += b2['money']

        total = a - b
        #totalが予算残高
        #bが合計額
        if total < 0:
            text = '予算オーバーです！'
            #テキスト送信
            line_bot_api.push_message(
                spending_userID,
                TextSendMessage(text = text)
                )
        connect.commit()
        connect.close()

        return render_template('html/Shukkin_Complete.html')

#MessagingAPI
handler = WebhookHandler(info['channelSecret'])
line_bot_api = LineBotApi(info['channelAccessToken'])

@app.route('/hook', methods = ['POST'])
def hook():    #Webhookの検証
    signature = request.headers['x-line-signature']
    body = request.get_data(as_text = True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return abort(200, 'OK')

@handler.add(MessageEvent, message = TextMessage)    #テキストメッセージの場合
def message(event):
    connect = MySQLdb.connect(
        host = info['server'],
        user = info['user'],
        passwd = info['pass'],
        db = info['db'],
        use_unicode = True,
        charset = 'utf8'
    )
    cursor = connect.cursor(MySQLdb.cursors.DictCursor)

    if event.message.text == '予算残高':
        a = 0
        b = 0
        total = 0
        text = ''
        today = datetime.now().date()

        cursor.execute('SELECT * FROM Yosan')
        a1 = cursor.fetchall()
        for a2 in a1:
            if a2['user_id'] == event.source.user_id:
                a = a2['zandaka']

        cursor.execute('SELECT * FROM History')
        b1 = cursor.fetchall()
        for b2 in b1:
            if b2['user_id'] == event.source.user_id:
                if b2['torokubi'].month == today.month:
                    b += b2['money']

        if a == 0:
            text = '予算が登録されていません'
        else:
            total = a - b
            total = f'{total:,}'
            text = '予算残高は' + str(total) + '円です'

        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text = text)
        )

        connect.commit()
        connect.close()
    elif event.message.text == '合計支出':
        today = datetime.now().date()
        total = 0
        text = ''

        cursor.execute('SELECT * FROM History')
        a1 = cursor.fetchall()
        for a2 in a1:
            if a2['user_id'] == event.source.user_id:
                if a2['torokubi'].month == today.month:
                    total += a2['money']

        total = f'{total:,}'
        text = '今月の支出は' + str(total) + '円です'

        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text = text)
        )

        connect.commit()
        connect.close()
    elif event.message.text == '合計貯金':
        total = 0
        text = ''

        cursor.execute('SELECT * FROM Tyokin')
        a1 = cursor.fetchall()
        for a2 in a1:
            if a2['user_id'] == event.source.user_id:
                total += a2['tyokin']

        total = f'{total:,}'
        text = '今までの貯金額は' + str(total) + '円です'

        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text = text)
        )

        connect.commit()
        connect.close()
    elif event.message.text == '支出履歴':
        today = datetime.now().date()
        a = [0] * 10
        date = [''] * 10
        category = [''] * 10
        text = '最新のものから最大で10件を表示しています\n\n'
        cnt = 0

        cursor.execute('SELECT * FROM History')
        a1 = cursor.fetchall()
        for a2 in reversed(a1):
            if cnt == 10:
                break

            if a2['user_id'] == event.source.user_id:
                a[cnt] = a2['money']
                date[cnt] = a2['torokubi'].strftime('%Y/%m/%d')
                category[cnt] = a2['category']
                cnt += 1

        if cnt > 0:
            if cnt < 10:
                text += '\n'.join([f'{date[i]} [{category[i]}] {a[i]:,}円' for i in range(cnt - 1, -1, -1)])
                text += '\n\nより詳細な履歴は支出グラフボタンから確認できます'
            else:
                a = a[-10:]
                date = date[-10:]
                category = category[-10:]
                length = len(a)

                text += '\n'.join([f'{date[i]} [{category[i]}] {a[i]:,}円' for i in range(length - 1, -1, -1)])
                text += '\n\nより詳細な履歴は支出グラフボタンから確認できます'

        else:
            text = '履歴が登録されていません'

        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text = text)
        )

        connect.commit()
        connect.close()

@handler.add(FollowEvent)
def handle_follow(event):
    connect = MySQLdb.connect(
        host = info['server'],
        user = info['user'],
        passwd = info['pass'],
        db = info['db'],
        use_unicode = True,
        charset = 'utf8'
    )
    cursor = connect.cursor(MySQLdb.cursors.DictCursor)

    sql1 = f"SELECT * FROM Users WHERE user_id='{event.source.user_id}'"
    cursor.execute(sql1)
    rows = cursor.fetchall()
    if len(rows) == 0:
        try:
            line_bot_api.push_message(
                event.source.user_id,
                TextSendMessage(text = '友だち追加ありがとうございます！')
            )
            sql2 = f"INSERT INTO Users VALUES('{event.source.user_id}')"
            cursor.execute(sql2)
        except Exception as e:
            t =  f"{e.__class__.__name__}: {e}"
            line_bot_api.push_message(
                event.source.user_id,
                TextSendMessage(text = t)
            )
    else:
        line_bot_api.push_message(
            event.source.user_id,
            TextSendMessage(text = 'おかえりなさい！')
        )

    connect.commit()
    cursor.close()
    connect.close()

if __name__ == '__main__':
    app.run()