<?php
try{
    $today = new DateTime();
    $todayYear = $today->format('Y');
} catch (Throwable $e) {
    echo $e->getMessage();
}
?>
<script>
    var ctx = document.getElementById('myChart').getContext('2d'); //2D画像として描画
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
                xAxes: [{
                    ticks: {
                        fontSize: 5, // 数字のフォントサイズを設定
                    }
                }],
                yAxes: [{
                    ticks: {
                        beginAtZero: true, //グラフの初期値を０に指定
                    }
                }]
            }
        }
    });
</script>