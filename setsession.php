<?php
session_start();
$session_id=session_id();
$session_name=session_name();
$user=$_GET['user'];
$age=$_GET['age'];
$_SESSION['user']=$user;
$_SESSION['age']=$age;
$data=[
"msg"=>"OK",
"code"=>"2000",
"result"=>[
	"session_id"=>$session_id,
	"session_name"=>$session_name
	]
];

$data=json_encode($data);
echo $data;