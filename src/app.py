#coding: utf-8

from flask import Flask, render_template, request, abort
import requests
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
    return render_template('html/Yosan_Form.html')

# 支出入力フォーム表示
@app.route('/spending')
def spending():
    return render_template('html/Shukkin_Form.html')

# 月間支出履歴表示
@app.route('/spending_month')
def spending_month():
    php_server_url = 'https://aso2201030.verse.jp/src/templates/php/Savemoney_m.php'
    response = requests.get(php_server_url)
    return response.content, response.status_code

# 年間支出履歴表示
@app.route('/spending_year')
def spending_year():
    return render_template('php/Savemoney_y.php')

# 週間支出履歴表示
@app.route('/spending_week')
def spending_week():
    return render_template('php/Savemoney_w.php')

# 月間貯金履歴表示
@app.route('/saving_month')
def saving_month():
    return render_template('php/Wallet_m.php')

# 年間貯金履歴表示
@app.route('/saving_year')
def saving_year():
    return render_template('php/Wallet_y.php')

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
        budget_userID = request.form.get('budget_userID')#フォームより取得
        userName = request.form.get('budget_userName')#フォームより取得
        budget_money = request.form.get('money')
        budget = int(budget_money)
        today = datetime.date.today()
        flag = False

        try:
            query = f"SELECT * FROM Yosan WHERE user_id='{budget_userID}'"
            cursor.execute(query)
        except Exception as e:
            t = e.__class__.__name__
            return render_template('html/error.html', error = t)
        rows = cursor.fetchall()

        if len(rows) == 0:
            text = '先月の貯金額がありません'
            #テキスト送信
            line_bot_api.push_message(
                budget_userID,
                TextSendMessage(text = text)
            )
            connect.close()
            return render_template('html/Yosan_Complete.html')

        # レコードが存在する
        user = rows[0]
        query3 = f"SELECT * FROM History WHERE user_id='{budget_userID}'"
        cursor.execute(query3)
        user3 = rows[0]
        tMonth = today.month  #今日の月
        tYear = today.year  #今日の年
        yMonth = user3['torokubi'].month  #データベースの月
        yYear = user3['torokubi'].year #データベースの年

        # 年を跨いでない場合
        if yYear == tYear:
            #Historyテーブルからtourokubiの月が今日の月-1のレコードを全件取得する
            query1 = f"SELECT * FROM History WHERE user_id='{budget_userID}' AND torokubi='{str(tYear)+'-'+str(yMonth)+'-10'}'"
            cursor.execute(query1)
            row1 = cursor.fetchall()
            # もし、それが存在するなら
            # その月内の利用額を全て加算して取得する
            nyugou = 0
            yosan = 0
            if len(row1) > 0:
                for b2 in row1:
                    nyugou += b2['money']
                #予算から予算額を取得する
                query2 = f"SELECT * FROM Yosan WHERE user_id='{budget_userID}' AND torokubi='{str(tYear)+'-'+str(yMonth)}'"
                cursor.execute(query2)
                row2 = cursor.fetchall()
                for a2 in row2:
                    yosan = a2['zandaka']
                #nyugouを引いて貯金額とし、テキスト送信
                if yosan - nyugou <= 0:
                    # テキスト送信
                    line_bot_api.push_message(
                        budget_userID,
                        TextSendMessage(text = "貯金額は0です")
                    )
                else:
                    # テキスト送信
                    line_bot_api.push_message(
                        budget_userID,
                        TextSendMessage(text = "貯金額は"+str(yosan - nyugou)+"です")
                    )
                
            # もし存在しないなら
            # 利用が無いと返答する
            else :
                #テキスト送信
                line_bot_api.push_message(
                    budget_userID,
                    TextSendMessage(text = '先月の利用がありません')
                    )


        elif yYear < tYear:#12月→1月の年を跨いだ場合
            #前年の履歴があるなら上と同じ処理を行う
            #Historyテーブルからtourokubiの月が今日の月-1のレコードを全件取得する
            query5 = f"SELECT * FROM History WHERE user_id='{budget_userID}' AND torokubi='{str(tYear - 1)+'-'+str(12)+'-10'}'"
            cursor.execute(query5)
            row5 = cursor.fetchall()
            # もし、それが存在するなら
            # その月内の利用額を全て加算して取得する
            nyugou1 = 0
            yosan1 = 0
            if len(row5) > 0:
                for b2 in row5:
                    nyugou1 += b2['money']
                #予算から予算額を取得する
                query6 = f"SELECT * FROM Yosan WHERE user_id='{budget_userID}' AND torokubi='{str(tYear - 1)+'-'+str(12)}'"
                cursor.execute(query6)
                row6 = cursor.fetchall()
                for a2 in row6:
                    yosan = a2['zandaka']
                #nyugouを引いて貯金額とし、テキスト送信
                if yosan1 - nyugou1 <= 0:
                    # テキスト送信
                    line_bot_api.push_message(
                        budget_userID,
                        TextSendMessage(text = "貯金額は0です")
                    )
                else:
                    # テキスト送信
                    line_bot_api.push_message(
                        budget_userID,
                        TextSendMessage(text = "貯金額は"+str(yosan1 - nyugou1)+"です")
                    )
            #利用がないなら無いと返答する
            else :
                #テキスト送信
                line_bot_api.push_message(
                    budget_userID,
                    TextSendMessage(text = '先月の利用がありません')
                    )

        #INSERTどうしたらいいか分からない問題発生。欒さん頼んだ

            # if yMonth < tMonth:
            #     try:
            #         query = f"SELECT * FROM History "#WHERE user_id='{budget_userID} AND torokubi={tYear+'-'+yMonth+'-10'}'"
            #         cursor.execute(query)
            #         rows = cursor.fetchall()
            #         # テキスト送信
            #         line_bot_api.push_message(
            #             budget_userID,
            #             TextSendMessage(text = str(len(rows)))
            #         )
            #     except Exception as e:
            #         t = e.__class__.__name__
            #         return render_template('html/error.html', error = t)
            #     cols = cursor.fetchall()
            #     total = 0

            #     for col in cols:
            #         if col['user_id'] == budget_userID:
            #             total += col['money']

            #     yBudget -= total
            #     if yBudget < 0:
            #         yBudget = 0
            #     cursor.execute('SELECT * FROM Tyokin')
            #     for row in rows:
            #         if row['user_id'] == budget_userID:
            #             a = 0
            #             text = ''
            #             cursor.execute('SELECT * FROM Tyokin')
            #             a1 = cursor.fetchall()
            #             for a2 in a1:
            #                 if a2['user_id'] == budget_userID:
            #                     a = a2['tyokin']
            #             a = f'{a:,}'
            #             text = '先月の貯金額は'+ str(a) +'円でした'
            #             #テキスト送信
            #             line_bot_api.push_message(
            #                 budget_userID,
            #                 TextSendMessage(text = text)
            #                 )
        
            #         else :
            #             text = '先月の貯金額がありません'
            #             #テキスト送信
            #             line_bot_api.push_message(
            #                 budget_userID,
            #                 TextSendMessage(text = text)
            #                 )
            #     try:
            #         cursor.execute('INSERT INTO Tyokin(user_id, tyokin, torokubi) VALUES(%s, %s, %s)', (budget_userID, yBudget, today))
            #     except Exception as e:
            #         t = e.__class__.__name__
            #         return render_template('html/error.html', error = t)

    #     elif yYear < tYear:
    #         try:
    #             cursor.execute('SELECT * FROM History')
    #         except Exception as e:
    #             t = e.__class__.__name__
    #             return render_template('html/error.html', error = t)
    #         cols = cursor.fetchall()
    #         total = 0

    #         for col in cols:
    #             if col['user_id'] == budget_userID:
    #                 total += col['money']

    #         yBudget -= total
    #         if yBudget < 0:
    #             yBudget = 0
    #         try:
    #             cursor.execute('INSERT INTO Tyokin(user_id, tyokin, torokubi) VALUES(%s, %s, %s)', (budget_userID, yBudget, today))
    #         except Exception as e:
    #             t = e.__class__.__name__
    #             return render_template('html/error.html', error = t)

    #     try:
    #         cursor.execute('UPDATE Users SET user_name = %s WHERE user_id = %s', (userName, budget_userID))
    #         cursor.execute('UPDATE Yosan SET zandaka = %s, torokubi = %s WHERE user_id = %s', (budget, today, budget_userID))
    #     except Exception as e:
    #         t = e.__class__.__name__
    #         return render_template('html/error.html', error = t)
    # else:
    #     try:
    #         cursor.execute('INSERT INTO Users VALUES(%s, %s)', (budget_userID, userName))
    #         cursor.execute('INSERT INTO Yosan VALUES(%s, %s, %s)', (budget_userID, budget, today))
    #     except Exception as e:
    #         t = e.__class__.__name__
    #         return render_template('html/error.html', error = t)

        connect.commit()
        connect.close()

        return render_template('html/Yosan_Complete.html')

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
        if b > total:
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
        today = datetime.date.today()

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
        today = datetime.date.today()
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
        today = datetime.date.today()
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
                text += '\n'.join([f'{date[i]} [{category[i]}] {a[i]}円' for i in range(cnt - 1, -1, -1)])
                text += '\n\nより詳細な履歴は支出グラフボタンから確認できます'
            else:
                a = a[-10:]
                date = date[-10:]
                category = category[-10:]
                length = len(a)

                text += '\n'.join([f'{date[i]} [{category[i]}] {a[i]}円' for i in range(length - 1, -1, -1)])
                text += '\n\nより詳細な履歴は支出グラフボタンから確認できます'

        else:
            text = '履歴が登録されていません'

        line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text = text)
        )

        connect.commit()
        connect.close()

if __name__ == '__main__':
    app.run()