<!DOCTYPE HTML>
<head>
    <meta lang="ja">
    <link rel="stylesheet" href="../static/css/style.css">
    <script src="https://kit.fontawesome.com/fd4cebc555.js" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.bundle.min.js"></script>
    <?php include('connect.php'); ?>
    <title>節約額表示</title>
</head>
<body>
    <div class="osirase">
        <h1>お知らせ</h1>
        <input type="button" value="ログアウト" id="logout">
        <p id="mod">今月の予算残高</p>
        <p id="save">これまでの貯金額</p>
    </div>
    <div class="TimeChange">
        <a class="nocheck" href="Savemoney_y.php">年</a>
        <a class="nocheck" href="Savemoney_m.php">月</a>
        <a class="checked" href="#">週</a>
    </div>
    <div class="GraphArea">
    <canvas id="myChart"></canvas>
        <?php include('Sishutu_week_graph.php'); ?>
    </div>
    <div class="History">
        <div id="histitle">支出履歴</div>
        <?php include('History_week.php') ?>
    </div>
    <footer>
        <div class="PageChange1">
            <i id="pig" class="fa-solid fa-piggy-bank fa-5x" style="color: #ffffff;"></i>
        </div>
        <div class="PageChange2" onclick="toWallet()">
            <i id="wallet" class="fa-solid fa-wallet fa-5x" style="color: #ffffff;"></i>
        </div>
    </footer>
</body>