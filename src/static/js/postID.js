window.onload = function () {
    fetch("secret.json")
        .then((response) => response.json())
        .then((data) => {
            liff.init({
                liffId: data.liffID,
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
                    var id = liffData.sub;
                    // JSONデータをPHPに送信
                    fetch('/src/php/GetID.php', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ id: id }), // idをJSONデータとして送信
                    })
                    .then(response => response.json())
                    .then(data => {
                        // サーバーからの応答を処理する
                        console.log(data);
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
                });
            });
        });
}