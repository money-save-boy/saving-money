window.onload = function (){
fetch("secret.json")
    .then((response) => response.json())
    .then((data) => {
        liff.init({
            liffId: data.liffID,
            withLoginOnExternalBrowser: true
        })
        .then(() => {
            let idToken = liff.getIDToken();
            let postData = "id_token=" + idToken + "&client_id=" + data.channelID;
            fetch("https://api.line.me/oauth2/v2.1/verify", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: postData
            })
            fetch("/src/php/connect.php", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            })
            .catch(error => {
                console.error('Error fetching JSON:', error);
            });
        });
    });
}
const postData = {
    operate: 'fetch',
    option: 'none'
  }
  fetch( url,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(postData)
    } )
    .then( res => res.json() )
    .then( files => {
      setData( files )
    } )