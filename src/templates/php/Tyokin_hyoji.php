<?php
    $pdo = new PDO($connect, USER, PASS);
    $str = 'select tyokin from Tyokin where user_id = ?';
    $sql = $pdo->prepare($str);
$sql->execute(/*[$ID]*/["1"]); //$IDをバインドした書き方
    $result = $sql->fetch(PDO::FETCH_ASSOC); //取得したデータを連想配列として取得する

    if ($result !== false) {
        $tyokin = $result['tyokin'];
        if ($tyokin > 0) {
            echo '<p id="mod">貯金額 ¥ ', $tyokin, '</p>';
        } else {
            echo '<p id="minus">貯金額 ¥ -', $tyokin, '</p>';
        }
    } else {
        echo '<p id="mod">貯金額 ¥ 0</p>';
        echo $result;
    }
?>