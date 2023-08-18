window.onload = function (){
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
                    document.getElementById("budget_userID").value = liffData.sub;
                    document.getElementById("budget_userName").value = liffData.name;
                });
            });
        });
}
