<?php

    session_start();

    if(!isset($_SESSION['usuario'])){
        echo '
            <script>
                alert("Por favor debes iniciar sesión");
            </script>
        ';
        session_destroy();
        die();
    }
?>


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bienvenida Vendedor</title>
    <link rel="stylesheet" href="css/bienvenida.css">
</head>
<body>
    <h1>Bienvenid@ a TechDreams!</h1>
    <div>
        <p>Haz click <a href="pagina_inicio.html">aquí </a>para administrar tu tienda</p>
        <a href="php/cerrar_sesion.php">Cerrar sesión</a>
    </div>   
    
</body>
</html>