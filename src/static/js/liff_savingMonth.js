document.addEventListener("DOMContentLoaded", function() {
    fetch("/src/secret.json")
    .then((response) => response.json())
    .then((data) => {
        clearToken(data.savingMonthLiffID);
        liff.init({
            liffId: data.savingMonthLiffID,
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
                fetch('/src/graphDisplay_month', {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: json,
                })
                .then((displayGraph) => displayGraph.json())
                .then((graphData) => {
                    for(var i = 0; i < graphData.length; i++){
                        for(var j = 0; j < myChart.data.labels.length; j++){
                            if(graphData[i]["day"] == j + 1){
                                myChart.data.datasets[0].data[j] = graphData[i]["money"];
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
                fetch('/src/savingDisplay_month', {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: json,
                })
                .then((savingDisplay) => savingDisplay.json())
                .then((saving) => {
                    var div = document.getElementsByClassName("History")[0];
                    var text = "<div id='histitle'>貯金履歴</div>";
                    text += "<table class='data'>";
                    var day = new Array(12).fill(0);
                    for(var i = 0; i < saving[0].length; i++){
                        day[saving[0][i] - 1] += saving[1][i];
                    }
                    for(var i = 0; i < 12; i++){
                        text += "<tr>";
                        text += "<td class='Ydate'>" + String(i + 1) + "月</td>";
                        text += "<td class='Yprice'>¥" + String(day[i]).replace(/(\d)(?=(\d\d\d)+(?!\d))/g, '$1,') + "</td>";
                        text += "</tr>";
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