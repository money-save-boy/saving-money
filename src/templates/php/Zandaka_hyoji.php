<?php
    $pdo = new PDO($connect, USER, PASS);
    $str = $pdo -> prepare('select zandaka from Yosan where user_id = ?');
    //$sql = $pdo -> query($str);
    //$str -> execute($ID);
    if(!is_array($str)){
        echo '<p id="mod">予算残高 ¥ 0</p>';
    }else {
        foreach($str as $row){
            if ($row > 0) {
                echo '<p id="mod">予算残高 ¥', $row['zandaka'], '</p>';
            }else{
                echo '<p id="minus">予算超過 ¥ -', $row['zandaka'], '</p>';
            }
        }
    }
?>