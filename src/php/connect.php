<?php
    const SERVER = 'mysql216.phy.lolipop.lan';
    const DBNAME = 'LAA1516911-moneysaveboy';
    const USER = 'LAA1516911';
    const PASS = 'Pass0120';
    $connect = 'mysql:host='. SERVER. ';dbname='. DBNAME. ';charset=utf8';
    $data = file_get_contents('php://input'); // POSTされた生のデータを受け取る
    $ID = json_decode($data); // json形式をphp変数に変換
    // echoすると返せる
    echo json_encode($ID);
?>
