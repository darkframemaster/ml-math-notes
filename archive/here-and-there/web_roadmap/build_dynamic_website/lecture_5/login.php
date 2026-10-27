<?php

	/*
	*
	* A simple login module with MySQL.
	*
	*/

	// enable session
	session_start();
	
	// connect to database
	if (($connection = mysqli_connect("localhost:3306","root","xh1008")) === FALSE)
		die("Could not connect to database!");

	// select database
	if (mysqli_select_db($connection, 'test') === FALSE)
		die("Could not select database!");

	// check in if username and password were submitted
	if (isset($_POST["user"]) && isset($_POST["pass"]))
	{
		// prepare SQL
		/*function:
		*	mysql_real_escape_string(string)
		*
		* Escaping the dengrous word in the input.
		*	
		*/
		$sql = sprintf("SELECT * FROM users WHERE user='%s'",
				mysqli_real_escape_string($connection, $_POST["user"]));
		// execute query
		$result = mysqli_query($connection, $sql);
		if ($result === FALSE)
			die("Could not query database!");
		
		// check whether we found a row
		if (mysqli_num_rows($result) == 1)
		{
			// fetch row
			print("<b>log in</b>");
			$row = mysqli_fetch_assoc($result);
			
			// check password
			if ($row["pass"] == $_POST["pass"])
			{
				print("<b>log in</b>");
				//remember that user's logged in
				$_SESSION["authenticated"] = TRUE;
	
				// redirect user to home page,using absolute path,
				$host = $_SERVER["HTTP_HOST"];
				$path = rtrim(dirname($_SERVER["PHP_SELF"]), "/\\");
				header("Location: http://$host$path/");
				exit;
			}
		}
	}
?>

<html>
<head>
	<title>Log In</title>
</head>
<body>
	<p>Please relog!</p>
	<form action="login.php" method="post">
		<table>
			<tr>
				<td>UserName:</td>
				<td><input name="user" type="text" /></td>
			</tr>
			<tr>
				<td>PassWord</td>
				<td><input name="pass" type="password" /></td>
			</tr>
			<tr>
				<td></td>
				<td><input type="submit" value="Log In" /></td>
			</tr>
		</table>
	</form>			
</body>
</html>
