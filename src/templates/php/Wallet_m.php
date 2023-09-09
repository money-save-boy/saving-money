<!DOCTYPE HTML>
<head>
    <meta lang="ja">
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
        <input type="button" value="ログアウト" id="logout">
        <?php include('Zandaka_hyoji.php'); ?>
        <?php include('Tyokingaku_hyoji.php'); ?>
    </div>
    <div class="TimeChange">
        <a class="nocheck" href='/src/saving_year'>年</a>
        <a class="checked" href="#">月</a>
    </div>
    <div class="GraphArea">
        <canvas id="myChart"></canvas>
        <?php include('Tyokin_month_graph.php'); ?>
    </div>
    <div class="History">
        <div id="histitle">貯金履歴</div>
        <?php include('History_m.php') ?>
    </div>
    <footer>
        <div class="PageChange1" onclick="location.href='/src/spending_month'">
            <i id="pig" class="fa-solid fa-piggy-bank fa-5x" style="color: #ffffff;"></i>
        </div>
        <div class="PageChange2">
            <i id="wallet" class="fa-solid fa-wallet fa-5x" style="color: #ffffff;"></i>
        </div>
    </footer>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.bundle.js"></script>
</body>