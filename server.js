const express = require('express');
const app = express();

// Multer Middleware for File Uploads
const multer = require('multer');
const upload = multer({ dest: 'uploads/' });		// Instance of multer with destination 'uploads/'

// exec() and unlink() in child-process and fs modules to handle 
// C++ process and file removal, respectively
const { exec } = require('child_process');
const { unlink } = require('fs');

// For Static Methods
const static_files_router = express.static('static');
app.use( static_files_router );

// Body Parser Middleware for Post Methods
const bodyParser = require('body-parser');
app.use(bodyParser.json()); // for parsing application/json
app.use(bodyParser.urlencoded({ extended: true }));

// Path Module to create path to executable file
const path = require('path');
const myProjectPath = path.join('build', 'MyProject');

// Set the view engine to EJS
app.set('view engine', 'ejs');

// Get Request to Home Page
app.get('/', (req,res) => {
	// Render index.ejs without fecal egg count
	res.render("index.ejs", { show: false, count: -1 });
});

// imgUpload.single() saves client's image in 'upload/' path
app.post('/', upload.single("image"), (req,res) => {
	const imagePath = req.file.path;		// Path to client's image input

	// Execute C++ executable file
	exec(`${myProjectPath} ${imagePath}`, (error, stdout, stderr) => {
		// Error with executing - terminate exec()
		if (error) {
			console.log("Error: " + error);
			console.log("Stderr: " + stderr);
			res.status(500).send('Failed to process image sent by client');

			// Remove image from uploads/
			unlink(imagePath, err => {
				if (err) {
					console.log("Failed to remove image from 'uploads/' path");
				} else {
					console.log("Successfully removed image");
				}
			});
			return;
		}

		// Render index.ejs with fecal egg count
		res.render("index.ejs", { show: true, count: stdout });

		// Remove image from uploads/
		unlink(imagePath, error => {
			if (error) {
				console.log("Failed to remove image from 'uploads/' path");
			} else {
				console.log("Successfully removed image");
			}
		});
	});
})

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));