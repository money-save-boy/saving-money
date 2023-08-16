#coding: utf-8

from flask import Flask, render_template, request
import json
import MySQLdb
import datetime

app = Flask(__name__)

# 予算入力フォーム表示
@app.route('/budget')
def budget():
    return render_template('Yosan_Form.html')

# 支出入力フォーム表示
@app.route('/spending')
def spending():
    return render_template('Shukkin_Form.html')

#データベース接続
@app.route('/in/<int:page>', methods = ['POST'])
def connectDB(page):
    with open('secret.json') as f:
        dbInfo = json.load(f)

    connect = MySQLdb.connect(
        host = dbInfo['server'],
        user = dbInfo['user'],
        passwd = dbInfo['pass'],
        db = dbInfo['db'],
        use_unicode = True,
        charset = "utf8"
    )
    cursor = connect.cursor(MySQLdb.cursors.DictCursor)

    if page == 1:   #予算入力
        budget_userID = request.form.get('budget_userID')
        userName = request.form.get('budget_userName')
        budget_money = request.form.get('money')
        budget = int(budget_money)
        today = datetime.date.today()

        cursor.execute('SELECT * FROM Yosan WHERE user_id = %s', (budget_userID))
        rows = cursor.fetchall()

        if rows == []:
            cursor.execute('INSERT INTO Users VALUES(%s, %s)', (budget_userID, userName))
            cursor.execute('INSERT INTO Yosan VALUES(%s, %s, %s)', (budget_userID, budget, today))
        else:
            cursor.execute('UPDATE Users SET user_name = %s', (userName))
            cursor.execute('UPDATE Yosan SET zandaka = %s, torokubi = %s WHERE user_id = %s', (budget, today, budget_userID))

        connect.commit()
        connect.close()

        return render_template('Yosan_Complete.html')
    elif page == 2: #支出入力
        spending_userID = request.form.get('spending_userID')
        categoryNumber = request.form.get('category')
        if categoryNumber == 1:
            category = '食費'
        elif categoryNumber == 2:
            category = '交通費'
        elif categoryNumber == 3:
            category = '日用品費'
        elif categoryNumber == 4:
            category = '被服費'
        elif categoryNumber == 5:
            category = '娯楽費'
        spending_money = request.form.get('money')
        spending = int(spending_money)
        today = datetime.date.today()

        cursor.execute('INSERT INTO History(user_id, category, money, torokubi) VALUES(%s, %s, %s, %s)', (spending_userID, category, spending, today))
        connect.commit()
        connect.close()
        return render_template('Shukkin_Complete.html')

if __name__ == "__main__":
    app.run()