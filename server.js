const express = require('express');
const app = express();

// Multer Middleware for File Uploads
const multer = require('multer');
const upload = multer({ dest: 'uploads/' });		// Instance of multer with destination 'uploads/'

// Handle C++ process and file removal, respectively
const { exec } = require('child_process');
const { unlink } = require('fs');

// Middleware for Static Files
const static_files_router = express.static('static');
app.use( static_files_router );

// Path to MyProject - dynamic based on OS
const path = require('path');
const myProjectPath = path.join(__dirname, 'main.py');

// View .ejs format
app.set('view engine', 'ejs');


// GET and POST requests to '/'
app.get('/', (req,res) => {
	// Render index.ejs without fecal egg count
	res.render("index.ejs", { show: false, count: -1, image: '' });
});

// upload.single() saves image in 'upload/' path
app.post('/', upload.single("image"), (req,res) => {
	const imagePath = req.file.path;		// Path to client's image input

	// Execute OpenCV executable file
	exec(`python main.py -f ${imagePath}`, (error, stdout, stderr) => {
		// Error with executing - terminate exec()
		if (error) {
			console.log("Error: " + stderr);
			res.status(500).send('Failed to process image sent by client');

			// Remove image from uploads/
			unlink(imagePath, err => {
				if (err) {
					console.log("Failed to remove image from 'uploads/' path");
				}
			});
			return;
		}

		// Render index.ejs with fecal egg count
		res.render("index.ejs", { show: true, count: stdout, image: 'imParasites.png' });

		// Remove image from uploads/
		unlink(imagePath, error => {
			if (error) {
				console.log("Failed to remove image from 'uploads/' path");
			}
		});
	});
})

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));