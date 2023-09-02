<?php
// リクエストがPOSTメソッドでない場合はエラーを返す
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405); // メソッド不許可のステータスコード
    die('Method Not Allowed');
    echo $_SERVER['REQUEST_METHOD'];
}

// JSONデータを受け取り、連想配列に変換する
$jsonData = file_get_contents('php://input');
$data = json_decode($jsonData, true);

// JSONデータの受信と変換が成功したかを確認する
if ($data === null) {
    http_response_code(400); // バッドリクエストのステータスコード
    die('Invalid JSON data');
}

// 受け取ったIDを変数として定義
if (isset($data['id'])) {
    $ID = $data['id'];
} else {
    http_response_code(400); // バッドリクエストのステータスコード
    die('Missing "id" field in JSON data');
}
?>