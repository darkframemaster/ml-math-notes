<?php
	/*
	* Using function `simplexml_load_file` to read a xml file.
	* The param can be a filename and a whole URL.
	* The variable `dom` will point at the root point of the xml datastructure,and in this case it is `blogs`.
	*/
	$dom = simplexml_load_file("blogs.xml");
?>

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<title>Blogs</title>
</head>
<body>
	<h1>Blogs</h1>
	<ul>
	<?php
		print($dom);
		foreach ($dom->blog as $blog)
		{
			print("<li>");
			print($blog["number"]);
			print(": ");
			print($blog->title);
			print("<ul>");
			foreach ($blog->body as $body)
			{	
				print("<li>");
				print($body);
				print("</li>");
			}
			print("</ul>");
			print("</li>");
		}
	
		$results = $dom->xpath("/blogs/blog[@number='1']");
		if(count($results) == 1)
		{
			$item = $results[0];
			print("<br />");
			print('search result:');
			print("<b>$item->title</b>");
		}
	?>
	</ul>
</body>
</html>
