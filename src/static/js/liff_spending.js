window.onload = function (){
    fetch("/src/secret.json")
        .then((response) => response.json())
        .then((data) => {
            liff.init({
                liffId: data.liffID
            })
            .then(() => {
                if(!liff.isLoggedIn()){
                    liff.login();
                }
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
                    document.getElementById("spending_userID").value = liffData.sub;
                });
            });
        });
}

window.onbeforeunload = function (){
    if(liff.isLoggedIn()){
        liff.logout();
    }
}