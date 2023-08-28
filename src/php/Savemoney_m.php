<!DOCTYPE HTML>
<head>
    <meta lang="ja">
    <link rel="stylesheet" href="../static/css/style.css">
    <script src="https://kit.fontawesome.com/fd4cebc555.js" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.bundle.min.js"></script>
    <?php include('connect.php'); ?>
    <title>支出額表示</title>
</head>
<body>
    <div class="osirase">
        <h1>お知らせ</h1>
        <input type="button" value="ログアウト" id="logout">
        <p id="mod">今月の予算残高</p>
        <p id="save">これまでの貯金額</p>
    </div>
    <div class="NoTimeChange" onclick="location.href='/src/php/Savemoney_y.php'">
        <p>年</p>
    </div>
    <div class="TimeChange">
        <p>月</p>
    </div>
    <div class="NoTimeChange" onclick="location.href='/src/php/Savemoney_w.php'">
        <p>週</p>
    </div>
    <div class="GraphArea">
    <canvas id="myChart"></canvas>
        <?php include('Sishutu_month_graph.php'); ?>
    </div>
    <div class="History">
        <div id="histitle">支出履歴</div>
        <?php include('History_month.php') ?>
    </div>
    <footer>
        <div class="PageChange1">
            <i id="pig" class="fa-solid fa-piggy-bank fa-5x" style="color: #ffffff;"></i>
        </div>
        <div class="PageChange2" onclick="location.href='/src/php/Wallet_m.php'">
            <i id="wallet" class="fa-solid fa-wallet fa-5x" style="color: #ffffff;"></i>
        </div>
    </footer>
</body>