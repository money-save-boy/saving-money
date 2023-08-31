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
            $sql = "SELECT SUM(tyokin),DATE_FORMAT(torokubi, '%Y') as yea FROM Tyokin
                    WHERE user_id = ?
                    GROUP BY yea";
            $stmt = $pdo->query($sql);
            $stmt -> execute($ID);
            $result = $stmt->fetchAll();
        } catch (PDOException $e) {
            echo $e;
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
                        echo '"'.($row["yea"]).'",';
             }?>],
            datasets: [{
                label: '支出額',
                data: [<?php foreach($result as $row){
                    echo $row["SUM(tyokin)"].",";
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
<?php