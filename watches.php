<?php
    session_start();
    $_SESSION["ip"]='<script>document.writeln(returnCitySN["cip"]);</script>';
    $_SESSION["watches"]=_SESSION["watches"]+1;
    echo 'document.write("浏览量 {$_SESSION["watches"]}")';
?>