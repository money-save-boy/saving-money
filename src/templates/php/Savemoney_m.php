<!DOCTYPE html>
<html lang="ja">

<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="/src/static/css/style.css">
    <script src="https://kit.fontawesome.com/fd4cebc555.js" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.bundle.min.js"></script>
    <script src="https://static.line-scdn.net/liff/edge/2/sdk.js"></script>
    <script src="/src/static/js/liff_spendingMonth.js"></script>
    <title>支出額表示</title>
</head>

<body>
    <?php
    $connect = include 'connect.php';
    echo $connect;
    ?>
    <?php
    // JSONデータを受け取り、連想配列に変換する
    $jsonData = file_get_contents('/src/static/js/liff_spendingMonth.js');
    $data = json_decode($jsonData, true);
    echo $data;

    // 受け取ったIDを変数として定義
    if (isset($data['id'])) {
        $ID = $data['id'];
        echo $ID;
    } else {
        echo 'IDとれてないよ';
    }
    ?>
    <div class="osirase">
        <h1>お知らせ</h1>
        <input type="button" value="ログアウト" id="logout">
        <?php include 'Zandaka_hyoji.php'; ?>
        <?php include 'Tyokingaku_hyoji.php'; ?>
    </div>
    <div class="TimeChange">
        <a class="nocheck" href="/css/templates/php/SaveMoney_y.php">年</a>
        <a class="checked" href="#">月</a>
        <a class="nocheck" href="/css/templates/php/SaveMoney_w.php">週</a>
    </div>
    <div class="GraphArea">
        <canvas id="myChart"></canvas>
        <?php
        $graph = include 'Sishutu_month_graph.php';
        echo $graph;
        ?>
    </div>
    <div class="History">
        <div id="histitle">支出履歴</div>
        <?php
        $historyMonth = include 'History_month.php';
        echo $historyMonth;
        ?>
    </div>
    <footer>
        <div class="PageChange1">
            <i id="pig" class="fa-solid fa-piggy-bank fa-5x" style="color: #ffffff;"></i>
        </div>
        <div class="PageChange2" onclick="location.href='/src/saving_month'">
            <i id="wallet" class="fa-solid fa-wallet fa-5x" style="color: #ffffff;"></i>
        </div>
    </footer>
</body>

</html>