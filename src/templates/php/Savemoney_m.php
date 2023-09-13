<!DOCTYPE html>
<html lang="ja">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    <link rel="stylesheet" href="/src/static/css/style.css">
    <title>支出額表示</title>
    <script src="https://kit.fontawesome.com/fd4cebc555.js" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.bundle.min.js"></script>
    <script src="https://static.line-scdn.net/liff/edge/2/sdk.js"></script>
    <script src="/src/static/js/liff_spendingMonth.js"></script>
</head>

<body>
    <?php include('connect.php'); ?>
    <div class="osirase">
        <div id="dummy"></div>
        <h1>お知らせ</h1>
        <?php echo '<div id="mi"></div>'; ?>
        <?php include('Tyokin_hyoji.php'); ?>
    </div>
    <div class="TimeChange">
        <a class="nocheck" href='/src/spending_year'>年</a>
        <a class="checked" href="#">月</a>
        <a class="nocheck" href='/src/spending_week'>週</a>
    </div>
    <div class="GraphArea">
        <canvas id="myChart"></canvas>
        <?php include('Sishutu_month_graph.php'); ?>
    </div>
    <div class="History">
        <div id="histitle">支出履歴</div>
        <?php include('History_month.php'); ?>
    </div>
    <footer>
        <div class="PageChange1">
            <p id="pig" class="fa-solid fa-piggy-bank" style="color: #ffffff; font-size: 2em; filter: drop-shadow(0 5px 5px #166a44); margin-top:11.8%;"></p>
        </div>
        <div class="PageChange2" onclick="location.href='/src/saving_month'">
            <p id="wallet" class="fa-solid fa-wallet" style="color: #ffffff; font-size: 2em; filter: drop-shadow(0 5px 5px #125821); margin-top:13%;"></p>
        </div>
    </footer>
</body>

</html>