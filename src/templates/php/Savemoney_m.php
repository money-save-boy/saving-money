<!DOCTYPE HTML>
<head>
    <meta lang="ja">
    <link rel="stylesheet" href="/src/static/css/style.css">
    <script src="https://kit.fontawesome.com/fd4cebc555.js" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.bundle.min.js"></script>
    <script src="https://static.line-scdn.net/liff/edge/2/sdk.js"></script>
    <script src="/src/static/js/postID.js"></script>
    <?php include('connect.php'); ?>
    <?php
        $requestMethod = $_SERVER['REQUEST_METHOD'];
        echo "リクエストメソッド: " . $requestMethod;
        // リクエストがPOSTメソッドでない場合はエラーを返す
        if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
            http_response_code(405); // メソッド不許可のステータスコード
            die('Method Not Allowed');
        }

        // JSONデータを受け取り、連想配列に変換する
        $jsonData = file_get_contents('php://input');
        $data = json_decode($jsonData, true);

        // JSONデータの受信と変換が成功したかを確認する
        if ($data === null) {
            http_response_code(400); // バッドリクエストのステータスコード
            die('Invalid JSON data');
        }

        // 受け取ったIDを変数として定義
        if (isset($data['id'])) {
            $ID = $data['id'];
        } else {
            http_response_code(400); // バッドリクエストのステータスコード
            die('Missing "id" field in JSON data');
        }
    ?>
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
    <div class="TimeChange">
        <p>月</p>
    </div>
    <div class="NoTimeChange" onclick="location.href='/src/spending_week'">
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
        <div class="PageChange2" onclick="location.href='/src/saving_month'">
            <i id="wallet" class="fa-solid fa-wallet fa-5x" style="color: #ffffff;"></i>
        </div>
    </footer>
</body>