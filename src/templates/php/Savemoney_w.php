<!DOCTYPE HTML>
<head>
    <meta lang="ja">
    <link rel="stylesheet" href="/src/static/css/style.css">
    <script src="https://kit.fontawesome.com/fd4cebc555.js" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.bundle.min.js"></script>
    <script src="/src/js/GetId.js"></script>
    <?php include('connect.php'); ?>
    <title>支出額表示</title>
</head>
<body>
    <div class="osirase">
        <h1>お知らせ</h1>
        <input type="button" value="ログアウト" id="logout">
        <?php include('Zandaka_hyoji.php'); ?>
        <?php include('Tyokingaku_hyoji.php'); ?>
    </div>
    <div class="NoTimeChange" onclick="location.href='/src/spending_year'">
        <p>年</p>
    </div>
    <div class="NoTimeChange" onclick="location.href='/src/spending_month'">
        <p>月</p>
    </div>
    <div class="TimeChange">
        <p>週</p>
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
        <div class="PageChange2"  onclick="location.href='/src/saving_month'">
            <i id="wallet" class="fa-solid fa-wallet fa-5x" style="color: #ffffff;"></i>
        </div>
    </footer>
</body>