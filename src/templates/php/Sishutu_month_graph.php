<?php
try {
    $pdo = new PDO($connect, USER, PASS);
    $sql = $pdo->prepare("SELECT SUM(money), DATE_FORMAT(torokubi, '%Y-%m') as mon FROM History
                    WHERE user_id = ?
                    GROUP BY mon");
    $sql->execute(/*[$ID]*/['1']);
    $result = $sql->fetchAll();
    $today = new DateTime();
    $todayYear = $today->format('Y');
} catch (PDOException $e) {
    echo $e->getMessage();
}
?>
<script>
    var ctx = document.getElementById('myChart').getContext('2d'); //2D画像として描画
    <?php if (!is_array($result)) {
        echo '<h2>Your data does not exist</h2>';
    } ?>
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [<?php for($i = 1; $i <= 12; $i++) {
                            echo '"' . ($todayYear) . '-'. ($i). '",';
                        } ?>],
            datasets: [{
                label: '支出額',
                data: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        suggestedMin: 0,
                        suggestedMax: 100000,
                        stepSize: 10000,
                        beginAtZero: true, //グラフの初期値を０に指定
                    }
                }]
            }
        }
    });
</script>