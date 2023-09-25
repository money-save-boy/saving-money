<?php
try {
    $currentYear = date("Y");
    $years = array();
    for ($i = 0; $i < 5; $i++) {
        $year = $currentYear - $i;
        $years[] = $year;
    }
} catch (Throwable $e) {
    echo $e->getMessage();
}
?>
<script>
    var ctx = document.getElementById('myChart').getContext('2d'); //2D画像として描画
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [<?php for ($i = 4; $i >= 0; $i--) {
                            echo '"' . ($years[$i]) . '",';
                        } ?>],
            datasets: [{
                label: "貯金額",
                data: [<?php for ($i = 0; $i < 5; $i++) {
                            echo '0,';
                        } ?>],
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                xAxes: [{
                    ticks: {
                        fontSize: 10, // 数字のフォントサイズを設定
                    }
                }],
                yAxes: [{
                    ticks: {
                        fontSize: 10, // 数字のフォントサイズを設定
                        beginAtZero: true, //グラフの初期値を０に指定
                    }
                }]
            }
        }
    });
</script>