<?php
try {
    $pdo = new PDO(
        $connect, USER, PASS,
        [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES =>false
        ]
    );
    $sql = "SELECT SUM(money), DATE_FORMAT(torokubi, '%Y-%m') as mon FROM History
                    WHERE user_id = ?
                    GROUP BY mon";
    $stmt = $pdo->query($sql);
    $stmt->execute(/*[$ID]*/['1']);
    $result = $stmt->fetchAll();
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
            labels: [<?php foreach ($result as $row) {
                            echo '"' . ($row["mon"]) . '",';
                        } ?>],
            datasets: [{
                label: '支出額',
                data: [<?php foreach ($result as $row) {
                            echo $row["SUM(money)"] . ",";
                        } ?>],
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true, //グラフの初期値を０に指定
                    }
                }]
            }
        }
    });
</script>