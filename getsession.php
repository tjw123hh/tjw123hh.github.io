<?php
$session_id=$_GET['session_id'];
session_id($session_id);
session_start();
 $user=$_SESSION['user'];
 $age=$_SESSION['age'];
$data=[
"msg"=>"OK",
"code"=>"2000",
"result"=>[
			"user"=>$user,
			"age"=>$age
		  ]
];
$data=json_encode($data);

echo $data;

