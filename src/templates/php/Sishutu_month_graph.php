<?php
try{
    $year = date("Y");
    $month = date("n");
    $lastDay = date("t", strtotime("$year-$month-01"));
} catch (Throwable $e) {
    echo $e->getMessage();
}
?>
<script>
    var ctx = document.getElementById('myChart').getContext('2d'); //2D画像として描画
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [<?php for($i = 1; $i <= $lastDay; $i++) {
                            echo '"' . ($i). '",';
                        } ?>],
            datasets: [{
                label: <?php echo '"'. $month. '月の支出額"' ?>,
                data: [<?php for($i = 1; $i <= $lastDay; $i++) {
                            echo '0,';
                        } ?>],
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: false, // グラフの自動サイズ調整を無効にする
            maintainAspectRatio: false, // アスペクト比を維持しない
            // グラフのサイズを指定する
            width: 800,
            height: 400,
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