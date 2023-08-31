<?php
    const SERVER = 'mysql216.phy.lolipop.lan';
    const DBNAME = 'LAA1516911-moneysaveboy';
    const USER = 'LAA1516911';
    const PASS = 'Pass0120';
    $connect = 'mysql:host='. SERVER. ';dbname='. DBNAME. ';charset=utf8';
    // 受信したJSONデータを処理する
    $jsonData = file_get_contents("php://input");
    $data = json_decode($jsonData, true);
    $ID = $data['sub'];
    // レスポンスを送信
    $response = array('status' => 'success');
    echo json_encode($response);  
?>