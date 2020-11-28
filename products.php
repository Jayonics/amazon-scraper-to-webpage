<?php
    if ( isset ( $searchTerm )) {
        echo "Search term specified.";
        echo "Running amazon extract with search term";
        #$shCommand = exec('/usr/bin/python3 products.py'.' --searchTerm="'.$searchTerm.'"', $output);
        $shCommand2 = escapeshellcmd('products.py'.' --searchTerm="'.$searchTerm.'"');
        $output2 = shell_exec($shCommand2);
        var_dump($output2);
        #var_dump($output);
    }
    else {
        echo "Search term unspecified.";
        echo "The script will run with the default terms specified in the python script - main function arguments";
        #$shCommand = exec('/usr/bin/python3 products.py', $output);
        $shCommand2 = escapeshellcmd('products.py');
        $output2 = shell_exec($shCommand2);
        var_dump($output2);
        #var_dump($output);
    }
?>
<!doctype html>
<html lang="HTML5">
<head>
    <title>Products</title>
</head>
<body>
<div class="productsDisplay">
    <ul>
        <?php
        $row = 0;
        if (($handle = fopen("results.csv", "r")) !== FALSE) {
            while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
                $num = count($data);
                echo '<li class="productItem" id='.$row.'>';
                $row++;
                for ($c=0; $c < $num; $c++) {
                    if ( $c === 0 && $data[$c] === "Description"){
                        # When column headings are inserted into the csv file, the php fgetcsv will add the headings like an item.
                        # This if statement ensures that, if the value of the first column heading is 'Description', that the php fgetcsv will move immediately to
                        # to the final column and then move to the next row. (to skip the further if statements that expect amazon product information).
                        # The script then continues as normal, making appropriate elements from the column data.
                        $c = $num;
                        $row++;
                    }
                    if ( $c === 0 ){
                        echo '<h4 class="productName" id="'.$row.'">'.$data[$c].'</h3>';
                    }
                    if ( $c === 1 ) {
                        echo '<img class="productImage" id="'.$row.'" src='.$data[$c].'>';
                    }
                    if ( $c === 2 ) {
                        echo '<p class="productPrice" id="'.$row.'">'.$data[$c].'</p>';
                    }
                    if ( $c === 3 ) {
                        echo '<p class="productRating" id="'.$row.'">'.$data[$c].'</p>';
                    }
                    if ( $c === 4 ) {
                        echo '<p class="productNRatings" id="'.$row.'">Number of reviews: '.$data[$c].'</p>';
                    }
                    if ( $c === 5 ) {
                        echo '<a href="'.$data[$c].'">Link to product.</a>';
                    }
                }
                echo "</li>";
            }
            fclose($handle);
        }
        ?>
    </ul>
</div>
</body>
</html>
