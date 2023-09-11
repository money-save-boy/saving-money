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
    $stmt->execute(/*[$ID]*/["1"]);

    // 結果を取得
    $result = $stmt->fetchAll();

    // 結果を表示
    if (!empty($result)) {
        foreach ($result as $row) {
            echo '<div class="data">';
            echo '<p>', $row['torokubi'], '</p>';
            echo '<p>', $row['category'], '</p>';
            echo '<p>', $row['total'], '</p>';
            echo '</div>';
        }
    } else {
        echo '<h2>Your data does not exist</h2>';
    }
} catch (PDOException $e) {
    echo '<h2>An error occurred: ', $e->getMessage(), '</h2>';
}
?>
