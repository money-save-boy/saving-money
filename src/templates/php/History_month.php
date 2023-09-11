<?php
    /*$pdo = new PDO($connect, USER, PASS);
    $str = 'select DATE_FORMAT(torokubi, "%Y-%m") as torokubi, category, sum(money) from History where user_id = ? group by torokubi,category';
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
            echo '<p>', $row['category'], '</p>';
            echo '<p>', $row['sum(money)'], '</p>';
            echo '</div>';
        }
    }else{
        
    }*/
?>

<?php
try {
    // データベース接続情報
    $pdo = new PDO(
        $connect, // 接続文字列
        USER,     // ユーザー名
        PASS,     // パスワード,
        [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, // エラーモードを設定
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC, // デフォルトのフェッチモードを設定
            PDO::ATTR_EMULATE_PREPARES => false // プリペアドステートメントを有効化
        ]
    );
    // プリペアドステートメントを準備
    $sql = 'SELECT DATE_FORMAT(torokubi, "%Y-%m") as torokubi, category, SUM(money) as total 
            FROM History 
            WHERE user_id = ? 
            GROUP BY torokubi, category';

    $stmt = $pdo->prepare($sql);
    // プレースホルダに値をバインドしてクエリを実行
    $stmt->execute(/*[$ID]*/ ['1']);
    // 結果を取得
    $result = $stmt->fetchAll();
    // 結果を表示
    if (!empty($result)) {
        foreach ($result as $row) {
            echo '<tr>';
            echo '<td>', $row['torokubi'], '</td>';
            echo '<td>', $row['category'], '</td>';
            echo '<td>', $row['total'], '</td>';
            echo '</tr>';
        }
        
    } else {
        echo '<h2>Your data does not exist</h2>';
    }
} catch (PDOException $e) {
    echo '<h2>An error occurred: ', $e->getMessage(), '</h2>';
}
?>
