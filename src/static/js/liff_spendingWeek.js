document.addEventListener("DOMContentLoaded", function() {
    fetch("/src/secret.json")
    .then((response) => response.json())
    .then((data) => {
        clearToken(data.spendingWeekLiffID);
        liff.init({
            liffId: data.spendingWeekLiffID,
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
                fetch('/src/displayGraph_week', {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: json,
                })
                .then((displayGraph) => displayGraph.json())
                .then((graphData) => {
                    var weekDates = getWeekDates();
                    for(var i = 1; i < graphData.length; i++){
                        for (var j = weekDates.start; j <= weekDates.end; j.setDate(j.getDate() + 1)){
                            if(graphData[i]["day"] == String(j.getDate())){
                                myChart.data.datasets[0].data[j.getDay()] = graphData[i]["money"];
                            }
                        }
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
                        budget = String(budget).replace(/(\d)(?=(\d\d\d)+(?!\d))/g, '$1,');
                        document.getElementById("mi").innerHTML = "<p id='minus'>予算超過 ¥" + budget + "</p>";
                    } else {
                        budget = String(budget).replace(/(\d)(?=(\d\d\d)+(?!\d))/g, '$1,');
                        document.getElementById("mi").innerHTML = "<p id='mod'>予算残高 ¥" + budget + "</p>";
                    }
                })
                fetch('/src/displaySaving', {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: json,
                })
                .then((displaySaving) => displaySaving.json())
                .then((saving) => {
                    if(saving == 0){
                        document.getElementById("mo").innerHTML = "<p id='mod'>貯金額 ¥" + saving + "</p>";
                    } else {
                        saving = String(saving).replace(/(\d)(?=(\d\d\d)+(?!\d))/g, '$1,');
                        document.getElementById("mo").innerHTML = "<p id='mod'>貯金額 ¥" + saving + "</p>";
                    }
                })
                fetch('/src/displaySpending_week', {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: json,
                })
                .then((displaySpending) => displaySpending.json())
                .then((spending) => {
                    var div = document.getElementsByClassName("History")[0];
                    var text = "<div id='histitle'>支出履歴</div>";
                    var cnt = 0;
                    for(var i = 0; i < spending[0].length; i++){
                        text += "<div class='data'>";
                        text += "<p class='date'>" + spending[0][i] + "</p>";
                        text += "<p class='category'>" + spending[1][i] + "</p>";
                        text += "<p class='price'>¥" + String(spending[2][i]).replace(/(\d)(?=(\d\d\d)+(?!\d))/g, '$1,') + "</p>";
                        text += "</div>";
                        cnt++;
                    }
                    if(cnt == 0){
                        text += "<p>No Data</p>";
                    }
                    div.innerHTML = text;
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

function getWeekDates() {
    var today = new Date();
    var currentDay = today.getDay(); // 0 (日曜日) から 6 (土曜日) までの値を取得
    var startDate = new Date(today);
    var endDate = new Date(today);

    // 週の始まり（日曜日）に設定
    startDate.setDate(today.getDate() - currentDay);

    // 週の終わり（土曜日）に設定
    endDate.setDate(today.getDate() + (6 - currentDay));

    return {
        start: startDate,
        end: endDate
    };
}