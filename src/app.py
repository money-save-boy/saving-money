#coding: utf-8

from flask import Flask, render_template, request, abort
import json
import MySQLdb
import datetime
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage)

app = Flask(__name__)

#json読み込み
with open('secret.json') as f:
    info = json.load(f)

# 予算入力フォーム表示
@app.route('/budget')
def budget():
    return render_template('Yosan_Form.html')

# 支出入力フォーム表示
@app.route('/spending')
def spending():
    return render_template('Shukkin_Form.html')

#データベース接続
@app.route('/in_<int:page>', methods = ['POST'])
def connectDB(page):
    connect = MySQLdb.connect(
        host = info['server'],
        user = info['user'],
        passwd = info['pass'],
        db = info['db'],
        use_unicode = True,
        charset = 'utf8'
    )
    cursor = connect.cursor(MySQLdb.cursors.DictCursor)

    #予算入力
    if page == 1:
        budget_userID = request.form.get('budget_userID')
        userName = request.form.get('budget_userName')
        budget_money = request.form.get('money')
        budget = int(budget_money)
        today = datetime.date.today()
        flag = False

        cursor.execute('SELECT * FROM Yosan')
        rows = cursor.fetchall()

        for row in rows:
            if row['user_id'] == budget_userID:
                flag = True
                yBudget = row['zandaka']

                tMonth = today.month
                tYear = today.year
                yMonth = row['torokubi'].month
                yYear = row['torokubi'].year

        if flag:
            if yYear == tYear:
                if yMonth < tMonth:
                    cursor.execute('SELECT * FROM History')
                    cols = cursor.fetchall()
                    total = 0

                    for col in cols:
                        if col['user_id'] == budget_userID:
                            total += col['money']

                    yBudget -= total
                    if yBudget < 0:
                        yBudget = 0
                    cursor.execute('INSERT INTO Tyokin(user_id, tyokin, torokubi) VALUES(%s, %s, %s)', (budget_userID, yBudget, today))

            elif yYear < tYear:
                cursor.execute('SELECT * FROM History')
                cols = cursor.fetchall()
                total = 0

                for col in cols:
                    if col['user_id'] == budget_userID:
                        total += col['money']

                yBudget -= total
                if yBudget < 0:
                    yBudget = 0
                cursor.execute('INSERT INTO Tyokin(user_id, tyokin, torokubi) VALUES(%s, %s, %s)', (budget_userID, yBudget, today))

            cursor.execute('UPDATE Users SET user_name = %s WHERE user_id = %s', (userName, budget_userID))
            cursor.execute('UPDATE Yosan SET zandaka = %s, torokubi = %s WHERE user_id = %s', (budget, today, budget_userID))
        else:
            cursor.execute('INSERT INTO Users VALUES(%s, %s)', (budget_userID, userName))
            cursor.execute('INSERT INTO Yosan VALUES(%s, %s, %s)', (budget_userID, budget, today))

        connect.commit()
        connect.close()

        return render_template('Yosan_Complete.html')

    #支出入力
    elif page == 2:
        spending_userID = request.form.get('spending_userID')
        categoryNumber = request.form.get('category')
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
        today = datetime.date.today()

        try:
            cursor.execute('INSERT INTO History(user_id, category, money, torokubi) VALUES(%s, %s, %s, %s)', (spending_userID, category, spending, today))
        except Exception as e:
            t = e.__class__.__name__
            return render_template('error.html', error = t)
        connect.commit()
        connect.close()

        return render_template('Shukkin_Complete.html')

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
    if event.message.text == '予算残高':
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text = 'いっぱい残ってる')
        )
    elif event.message.text == '合計支出':
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text = 'あんまり使ってない')
        )
    elif event.message.text == '支出履歴':
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text = '100円くらい\n200円くらい\n1000円くらい')    #\nは改行
        )
    else:
        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text = 'まだ準備できてないよ')
        )

if __name__ == '__main__':
    app.run()