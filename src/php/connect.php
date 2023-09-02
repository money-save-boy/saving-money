<?php
    const SERVER = 'mysql216.phy.lolipop.lan';
    const DBNAME = 'LAA1516911-moneysaveboy';
    const USER = 'LAA1516911';
    const PASS = 'Pass0120';
    $connect = 'mysql:host='. SERVER. ';dbname='. DBNAME. ';charset=utf8';
?>
<script>
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
                    <?php $ID = lifFData.sub; ?>
                });
            });
        });
    }
</script>
<?php