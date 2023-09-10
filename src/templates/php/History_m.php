<?php
    $pdo = new PDO($connect, USER, PASS);
    $str = 'select DATE_FORMAT(torokubi, "%Y-%m") as torokubi, sum(tyokin) from Tyokin where user_id = ? group by torokubi';
    $sql = $pdo -> query($str);
    if(isset($ID)){
        $sql -> execute($ID);
    }else{
        echo '<h2>Your ID does not exist</h2>';
    }
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