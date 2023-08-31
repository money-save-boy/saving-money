<?php
    const SERVER = 'mysql216.phy.lolipop.lan';
    const DBNAME = 'LAA1516911-moneysaveboy';
    const USER = 'LAA1516911';
    const PASS = 'Pass0120';
    $connect = 'mysql:host='. SERVER. ';dbname='. DBNAME. ';charset=utf8';

    header('Access-Control-Allow-Origin: *');
    header('Access-Control-Allow-Headers: Origin, X-Requested-With, Content-Type, Accept');
    header("Content-type: application/json; charset=UTF-8");

    $input_json = file_get_contents('php://input');
    $post = json_decode( $input_json, true );
    $ID = $post['sub'];
    // データベースへの接続を確立
    try {
        $pdo = new PDO($connect, USER, PASS);
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    } catch (PDOException $e) {
        echo "データベースへの接続に失敗しました: " . $e->getMessage();
        exit;
    }
    try {
        $query = "SELECT * FROM Users WHERE user_id = :id"; // your_table にテーブル名を入れてください
        $stmt = $pdo->prepare($query);
        $stmt->bindParam(':id', $ID);
        $stmt->execute();
        $result = $stmt->fetch(PDO::FETCH_ASSOC);
        
    } catch (PDOException $e) {
        echo "クエリの実行に失敗しました: " . $e->getMessage();
    }
?>