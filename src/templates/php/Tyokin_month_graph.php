<?php
    try {
        $pdo = new PDO(
            $connect, USER, PASS,
            [
                PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, //エラーをスローさせる
                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC, //デフォルトのfetchがデータを連想配列として返す
                PDO::ATTR_EMULATE_PREPARES => false //プリペアードステートメントの設定。sqlに挿入する変数をバインドさせる
            ]
        );
        $sql = "SELECT SUM(tyokin), DATE_FORMAT(torokubi, '%Y-%m') as mon FROM Tyokin
                WHERE user_id = ?
                GROUP BY mon";
        $stmt = $pdo->prepare($sql);
    $stmt->execute(/*[$ID]*/['1']);
        $result = $stmt->fetchAll();
    } catch (PDOException $e) {
        echo $e->getMessage();
    }
?>
<script>
    var ctx = document.getElementById('myChart').getContext('2d');//2D画像として描画
    <?php if(!is_array($result)){
        echo '<h2>Your data does not exist</h2>';
    }?>
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [<?php foreach($result as $row){
                        echo '"'.($row["mon"]).'",';
             }?>],
            datasets: [{
                label: '貯金額',
                data: [<?php foreach($result as $row){
                    echo $row["SUM(money)"].",";
                } ?>],
                backgroundColor: 
                    'rgba(2, 164, 135, 0.2)',
                borderColor: 
                    'rgba(2, 164, 135, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {     
                        beginAtZero: true,//グラフの初期値を０に指定
                    }
                }]
            }
        }
    });
</script>