<?php

session_start();

include 'conexion_be.php';

$correo = $_POST['correo'];
$contrasena = $_POST['contrasena'];

$validar_login = mysqli_query($conexion, "SELECT * FROM customers WHERE correo='$correo' AND contrasena='$contrasena'");

if (mysqli_num_rows($validar_login) > 0) {
    $row = mysqli_fetch_assoc($validar_login);
    $acceso = $row['acceso'];

    if ($acceso == 'admin') {
        $_SESSION['usuario'] = $correo;
        header("Location: ../bienvenida_vendedor.php");
        exit;
    } else {
        $_SESSION['usuario'] = $correo;
        header("Location: ../bienvenida_comprador.php");
        exit;
    }
} else {
    echo '
        <script>
            alert("Usuario no existe, por favor verifique los datos introducidos");
            window.location = "../login.php";
        </script>
    ';
    exit;
}
?>
