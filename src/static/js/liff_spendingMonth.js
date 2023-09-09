window.onload = function () {
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
                        "Content-Type": "application/x-www-form-urlencoded" //送られたトークンが本当にLINEから来たのか
                    },
                    body: postData
                })
                .then((res) => res.json())
                .then((liffData) => {
                    var id = liffData.sub;
                    // JSONデータをPHPに送信
                    fetch("/src/templates/php/Savemoney_m.php", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({ id: id }), // idをJSONデータとして送信
                    })
                    .then(() => {
                        alert(id);
                    });
                    alert("send");
                });
            });
        });
}

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
