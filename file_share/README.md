# File Share - Local Network File Sharing App

A simple and beautiful web application to share files between devices connected to the same network (e.g., between your phone and laptop).

## Features

- 📤 **Easy File Upload**: Drag & drop or click to upload files
- 📥 **Quick Download**: Download shared files with one click
- 🗑️ **File Management**: Delete files you no longer need
- 📱 **Cross-Device Access**: Access from any device on your network
- 🎨 **Modern UI**: Beautiful, responsive design that works on desktop and mobile
- 🔄 **Auto-Refresh**: File list automatically updates

## Requirements

- Python 3.7 or higher
- Flask
- Devices must be on the same network (WiFi/LAN)

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the server:

```bash
python app.py
```

2. The server will start and display:

   - Local access URL: `http://127.0.0.1:5000`
   - Network access URL: `http://<your-ip>:5000`

3. **On the same device**: Open `http://127.0.0.1:5000` in your browser

4. **From other devices on the same network**:
   - Make sure they're connected to the same WiFi/network
   - Open a browser and go to `http://<your-ip>:5000` (the IP will be shown when you start the server)

## How to Use

1. **Upload Files**:

   - Drag and drop files onto the upload area, or
   - Click "Choose Files" to browse and select files

2. **Download Files**:

   - Click the "Download" button next to any file

3. **Delete Files**:
   - Click the "Delete" button next to any file you want to remove

## File Storage

- Uploaded files are stored in the `uploads/` directory
- File metadata is stored in `file_metadata.json`
- Maximum file size: 100MB (can be changed in `app.py`)

## Security Features

🔒 **Security Features Enabled**:

- ✅ **Password Authentication**: Protected login system with secure password hashing
- ✅ **CSRF Protection**: All form submissions are protected against Cross-Site Request Forgery attacks
- ✅ **Rate Limiting**: Prevents abuse with request rate limits (20 uploads, 30 downloads, 60 API calls per minute per IP)
- ✅ **Path Traversal Protection**: Prevents directory traversal attacks
- ✅ **Secure Sessions**: HTTP-only cookies with SameSite protection
- ✅ **Input Validation**: All filenames and inputs are validated and sanitized
- ✅ **Password Management**: Change password functionality with minimum 6 character requirement

### Default Password

On first run, the app will create a default password: **`admin123`**

⚠️ **IMPORTANT**: Change this password immediately after first login using the "Change Password" button!

### Security Notes

⚠️ **Important**:

- This application is designed for use on trusted local networks only
- Always use a strong, unique password
- Change the default password immediately after first use
- For additional security, consider setting up HTTPS with a reverse proxy (nginx/Apache) in production
- The password hash is stored in `.password_hash` file - keep this file secure

## Troubleshooting

- **Can't access from other devices?**

  - Make sure all devices are on the same network
  - Check that your firewall isn't blocking port 5000
  - Verify the IP address shown when starting the server

- **File upload fails?**
  - Check file size (max 100MB)
  - Ensure you have write permissions in the directory

## Customization

- Change maximum file size: Edit `MAX_FILE_SIZE` in `app.py`
- Change port: Modify `app.run(port=5000)` in `app.py`
- Change upload folder: Modify `UPLOAD_FOLDER` in `app.py`

## License

Free to use and modify for personal projects.
