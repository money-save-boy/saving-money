<?php
    $pdo = new PDO($connect, USER, PASS);
    $str = 'select DATE_FORMAT(torokubi, "%Y-%m") as torokubi, category, sum(money) from History where user_id = "1" group by torokubi,category';
    $sql = $pdo -> query($str);
    if($sql = NULL){
        echo '<h2>Your data does not exist</h2>'
    }else{
        foreach($sql as $row){
            echo '<div class="data">';
            echo '<p>', $row['torokubi'], '</p>';
            echo '<p>', $row['category'], '</p>';      
            echo '<p>', $row['sum(money)'], '</p>';
            echo '</div>';
        }
    }
?>