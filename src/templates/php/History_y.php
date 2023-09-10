<?php
    $pdo = new PDO($connect, USER, PASS);
    $str = 'select DATE_FORMAT(torokubi, "%Y-%m") as torokubi, sum(tyokin) from Tyokin where user_id = "1" group by torokubi';
    $sql = $pdo -> query($str);
    //$sql -> execute($ID);
    if(is_array($sql)){
        foreach($sql as $row){
            echo '<div class="data">';
            echo '<p>', $row['torokubi'], '</p>'; 
            echo '<p>', $row['sum(money)'], '</p>';
            echo '</div>';
        }
    }else{
        echo '<h2>History does not exist</h2>';
    }
?>