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
                var jsonData = {"id": liffData.sub};
                var json = JSON.stringify(jsonData);
                fetch('/src/spending_month_send', {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: json,
                })
                .then((spending_month_send) => spending_month_send.json())
                .then((graphData) => {
                    for(var i = 0; i < 12; i++){
                        myChart.data.datasets[0].data[i] = graphData[i];
                    }
                    myChart.update();
                })
                fetch('/src/displayBudget', {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: json,
                })
                .then((displayBudget) => displayBudget.json())
                .then((budget) => {
                    if(budget < 0){
                        document.getElementById("mi").innerHTML = "<p id='minus'>予算超過 ¥" + budget + "</p>";
                    } else {
                        console.log(typeof budget);
                        document.getElementById("mi").innerHtml = "<p id='mod'>予算残高 ¥" + budget + "</p>";
                    }
                })
                .catch(function(error) {
                    console.error(error);
                });
            });
        });
    })
});

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