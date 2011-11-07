<?php
	$index = (int)$_GET['idx'];

	$file = fopen("train-images-idx3-ubyte", "r");
	$label = fopen( "train-labels-idx1-ubyte", "r");

	if (!$file || !$label ) {
			echo "Failed to open file";
			exit();
	}

/*
	for ( $i = 0; $i < 32; $i += 1 ) {
		$r = unpack("C",fread($file,1));
		echo $r[1]. " ";
	}
*/
	$magica = unpack( "S", fread($file, 2));
	$magic = $magica[1];

	if ( $magic != 0) {
		echo "Magic number : ".$magic." != 0<br>" ;
		exit();
	}
	$typea = unpack( "C", fread($file, 1));
	$type = $typea[1];
	if ( $type != 0x08 ) {
		echo "Type : ".strval($type)." != 0x08 (ubyte)<br>" ;
		exit();
	}

	$dimena = unpack( "C", fread($file, 1));
	$dimen = $dimena[1];
	if ( $dimen != 3 ) {
		echo "Dimension : ".strval($dimen)." != 3 <br>" ;
		exit();
	}

	$pcounta = unpack( "C", fread($file, 1));
	$pcounta = unpack( "C", fread($file, 1));
	$pcounta = unpack( "C", fread($file, 1));
	$pcount = $pcounta[1]*256;
	$pcounta = unpack( "C", fread($file, 1));
	$pcount += $pcounta[1];

	$xsizea = unpack( "C", fread($file, 1));
	$xsizea = unpack( "C", fread($file, 1));
	$xsizea = unpack( "C", fread($file, 1));
	$xsizea = unpack( "C", fread($file, 1));
	$xsize = $xsizea[1];
	$ysizea = unpack( "C", fread($file, 1));
	$ysizea = unpack( "C", fread($file, 1));
	$ysizea = unpack( "C", fread($file, 1));
	$ysizea = unpack( "C", fread($file, 1));
	$ysize = $ysizea[1];

	echo "IDX file composed of ".strval($pcount)." images<br>";
	echo "Each image size is (".$xsize.", ".$ysize.")<br>";
	echo "Current index = ".$index."<br>";
	if ( $index > 0 )
		echo "<a href=\"idxviewer.php?idx=".($index-1)."\">Previous</a>--";
	if ( $index < $pcount - 1 )
		echo "<a href=\"idxviewer.php?idx=".($index+1)."\">Next </a>";

	$parea = $xsize * $ysize;
	$offset = $parea * $index;

	fseek($file, $offset, SEEK_CUR);

	fseek($label, $index + 8);
	$labelva = unpack( "C", fread($label, 1));
	$labelv = $labelva[1];
	echo "<br><br>";
	echo "Label: ".$labelv."<br><br><br>";


	echo "<table>";
	for( $i = 0; $i < $xsize; $i += 1) {
		echo "<tr>";
		for ( $j = 0; $j < $ysize; $j += 1) {
			$dataa = unpack( "C", fread($file, 1));
			$data = $dataa[1];
			echo "<td width=20>".$data."</td>";

			
		}
		echo "</tr>";
	}
	echo "</table>";


	fclose($file);
?>
