"use strict";
document.addEventListener("DOMContentLoaded", function() {
    fetch("/src/secret.json")
    .then((response) => response.json())
    .then((data) => {
        clearToken(data.spendingMonthLiffID);
        liff.init({
            liffId: data.spendingMonthLiffID,
            withLoginOnExternalBrowser: true
        })
        .then(() => {
            var idToken = liff.getIDToken();
            var postData = "id_token=" + idToken + "&client_id=" + data.channelID;
            fetch("https://api.line.me/oauth2/v2.1/verify", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: postData
            })
            .then((res) => res.json())
            .then((liffData) => {
                var jsonData = JSON.stringify({id: liffData.sub});
                console.log('送信データ:', jsonData); // データをコンソールに表示
                fetch('https://aso2201030.verse.jp/src/spending_month_send', {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: jsonData,
                })
                .then((r) => {
                    console.log(r);
                })
                .catch(error => {
                    console.log('miss送信データ:', jsonData);
                    console.log('エラー:', error); // エラーメッセージをコンソールに表示
                });
            });
        });
    })
});

function keyReload(el){
    var keys = [];
    for(var i = 0; i < localStorage.length; i++){
        var key = localStorage.key(i);
        if(key.indexOf(el) == 0){
            keys.push(key);
        }
    }

    return keys;
}

function clearToken(id){
    var keyPrefix = `LIFF_STORE:${id}:`;
    var key = keyPrefix + 'decodedIDToken';
    var deIDTokenString = localStorage.getItem(key);

    if(!deIDTokenString){
        return;
    }

    var deIDToken = JSON.parse(deIDTokenString);

    if (new Date().getTime() > deIDToken.exp * 1000){
        var keys = keyReload(keyPrefix);
        keys.forEach(function(key) {
            localStorage.removeItem(key)
        })
    }
}
