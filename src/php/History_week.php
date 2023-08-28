<?php
    $pdo = new PDO($connect, USER, PASS);
    $str = 'select DATE_FORMAT(torokubi, "%Y-%u") as torokubi, category, sum(money) from History where user_id = "1" group by torokubi';
    $sql = $pdo -> query($str);
    foreach($sql as $row){
        echo '<div class="data">';
        echo '<p>', $row['torokubi'], '</p>';
        echo '<p>', $row['category'], '</p>';      
        echo '<p>', $row['sum(money)'], '</p>';
        echo '</div>';
    }
?>