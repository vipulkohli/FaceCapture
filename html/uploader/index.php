<!DOCTYPE HTML>
<html>
<body>
<form action="uploader.php" method="post" enctype="multipart/form-data">
 <fieldset>
          <legend>Image Upload</legend>
    	  	<ol>
    	  		<li><label for="firstname">First Name:</label><input type="text" id="firstname" name="firstname" placeholder="First Name"/></li>
    	  		<li><label for="lastname">Last Name:</label><input type="text" id="lastname" name="lastname" placeholder="Last Name"/></li>
			<label for="file">Choose File:</label> <input type="file" name="file" id="file"><br>
    	  	</ol>
		<input type="submit" name="submit" value="Submit Upload">
        </fieldset>
</form>

</body>
</html>