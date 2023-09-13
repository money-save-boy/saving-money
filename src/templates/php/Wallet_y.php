<!DOCTYPE HTML>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    <link rel="stylesheet" href="/src/static/css/style2.css">
    <script src="https://kit.fontawesome.com/fd4cebc555.js" crossorigin="anonymous"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>
    <script src="/src/static/js/postID.js"></script>
    <?php include('connect.php'); ?>
    <title>貯金額表示</title>
</head>
<body>
    <div class="osirase">
        <h1>お知らせ</h1>
        <?php include 'Zandaka_hyoji.php' ; ?>
        <?php include 'Tyokingaku_hyoji.php' ; ?>
    </div>
    <div class="TimeChange">
        <a class="checked" href='#'>年</a>
        <a class="nocheck" href="/src/saving_year">月</a>
    </div>
    <div class="GraphArea">
        <canvas id="myChart"></canvas>
        <?php include 'Tyokin_year_graph.php' ; ?>
    </div>
    <div class="History">
        <div id="histitle">貯金履歴</div>
        <?php include 'History_y.php'; ?>
    </div>
    <footer>
        <div class="PageChange1" onclick="location.href='/src/spending_month'">
            <p id="pig" class="fa-solid fa-piggy-bank" style="color: #ffffff; font-size: 3em; filter: drop-shadow(0 5px 5px #7e3459); margin-top:11.8%;"></p>
        </div>
        <div class="PageChange2">
            <p id="pig" class="fa-solid fa-wallet" style="color: #ffffff; font-size: 3em; filter: drop-shadow(0 5px 5px #7a1d34); margin-top:13%;"></p>
        </div>
    </footer>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.bundle.js"></script>
</body>
</html>