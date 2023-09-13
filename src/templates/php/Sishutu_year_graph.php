<?php
try {
    $year = date("Y");
} catch (Throwable $e) {
    echo $e->getMessage();
}
?>
<script>
    var ctx = document.getElementById('myChart').getContext('2d'); //2D画像として描画
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [<?php for ($i = 1; $i <= 12; $i++) {
                            echo '"' . ($i) . '月",';
                        } ?>],
            datasets: [{
                label: "支出額",
                data: [<?php for ($i = 1; $i <= 12; $i++) {
                            echo '0,';
                        } ?>],
                backgroundColor: 'rgba(2, 164, 135, 0.2)',
                borderColor: 'rgba(2, 164, 135, 1)',
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