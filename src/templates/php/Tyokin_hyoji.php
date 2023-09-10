<?php
    $pdo = new PDO($connect, USER, PASS);
    $str = 'select tyokin from Tyokin where user_id = ?';
    //$sql = $pdo -> query($str);
    //echo $ID;
    //$sql -> execute($ID);
    if(!is_array($sql)){
        echo '<p id="mod">貯金額 ¥ 0</p>';
    }else {
        foreach($sql as $row){
            if ($row > 0) {
                echo '<p id="mod">貯金額 ¥ ', $row['tyokin'], '</p>';
            }else{
                echo '<p id="minus">貯金額 ¥ -', $row['tyokin'], '</p>';
            }
        }
    }
?>