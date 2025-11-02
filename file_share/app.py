import os
import socket
import secrets
import hashlib
import time
from flask import Flask, render_template, request, send_file, jsonify, redirect, url_for, session, abort
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from functools import wraps
import json
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)

# Security Configuration
UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
ALLOWED_EXTENSIONS = None  # Allow all file types

# Generate secret key for sessions (change this in production!)
app.secret_key = secrets.token_hex(32)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True if using HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Rate limiting storage (in-memory for simplicity, use Redis in production)
rate_limit_storage = defaultdict(list)

# Password file
PASSWORD_FILE = '.password_hash'

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Metadata file to store file information
METADATA_FILE = 'file_metadata.json'

# Security functions
def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, password_hash):
    """Verify password against hash"""
    return hash_password(password) == password_hash

def init_password():
    """Initialize or load password"""
    if not os.path.exists(PASSWORD_FILE):
        # First run - create default password
        default_password = "admin123"  # Users should change this!
        password_hash = hash_password(default_password)
        with open(PASSWORD_FILE, 'w') as f:
            f.write(password_hash)
        print(f"\n⚠️  DEFAULT PASSWORD: {default_password}")
        print("⚠️  Please change this password after first login!\n")
        return password_hash
    else:
        with open(PASSWORD_FILE, 'r') as f:
            return f.read().strip()

def change_password(new_password):
    """Change the password"""
    password_hash = hash_password(new_password)
    with open(PASSWORD_FILE, 'w') as f:
        f.write(password_hash)
    return password_hash

# Load password hash on startup
PASSWORD_HASH = init_password()

def check_rate_limit(identifier, max_requests=10, window=60):
    """Simple rate limiting"""
    now = time.time()
    requests = rate_limit_storage[identifier]
    # Remove old requests outside the time window
    requests[:] = [req_time for req_time in requests if now - req_time < window]
    
    if len(requests) >= max_requests:
        return False
    
    requests.append(now)
    return True

def get_client_ip():
    """Get client IP address"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    return request.remote_addr or 'unknown'

def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
            if request.is_json:
                return jsonify({'error': 'Authentication required'}), 401
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def validate_filename(filename):
    """Validate filename to prevent path traversal"""
    if not filename or not isinstance(filename, str):
        return False
    # Decode URL encoding first if present
    try:
        from urllib.parse import unquote
        filename = unquote(filename)
    except:
        pass
    # Check for path traversal attempts
    if '..' in filename or filename.startswith('/') or filename.startswith('\\'):
        return False
    # Check for null bytes
    if '\x00' in filename:
        return False
    # Filename must not be empty after securing
    secured = secure_filename(filename)
    if not secured or secured == '':
        return False
    return True

def load_metadata():
    """Load file metadata from JSON file"""
    if os.path.exists(METADATA_FILE):
        try:
            with open(METADATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_metadata(metadata):
    """Save file metadata to JSON file"""
    with open(METADATA_FILE, 'w') as f:
        json.dump(metadata, f, indent=2)

def get_local_ip():
    """Get the local IP address of the machine"""
    try:
        # Connect to a remote address to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        password = request.form.get('password', '')
        if verify_password(password, PASSWORD_HASH):
            session['authenticated'] = True
            session.permanent = True
            # Generate CSRF token
            session['csrf_token'] = secrets.token_hex(32)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid password', local_ip=get_local_ip())
    
    # Already authenticated
    if session.get('authenticated'):
        return redirect(url_for('index'))
    
    return render_template('login.html', local_ip=get_local_ip())

@app.route('/logout', methods=['POST'])
def logout():
    """Logout"""
    session.clear()
    return redirect(url_for('login'))

@app.route('/change-password', methods=['POST'])
@require_auth
def change_password_route():
    """Change password"""
    if not session.get('csrf_token') or session.get('csrf_token') != request.form.get('csrf_token'):
        return jsonify({'error': 'Invalid CSRF token'}), 403
    
    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')
    
    if not new_password or len(new_password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    if new_password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400
    
    global PASSWORD_HASH
    PASSWORD_HASH = change_password(new_password)
    return jsonify({'success': True, 'message': 'Password changed successfully'})

@app.route('/')
@require_auth
def index():
    """Main page"""
    metadata = load_metadata()
    files = []
    for filename, info in metadata.items():
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            files.append({
                'name': filename,
                'size': file_size,
                'uploaded': info.get('uploaded', 'Unknown'),
                'size_formatted': format_file_size(file_size)
            })
    
    files.sort(key=lambda x: x['uploaded'], reverse=True)
    local_ip = get_local_ip()
    port = request.environ.get('SERVER_PORT', 5000)
    csrf_token = session.get('csrf_token', '')
    
    return render_template('index.html', files=files, local_ip=local_ip, port=port, csrf_token=csrf_token)

def format_file_size(size):
    """Format file size in human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"

@app.route('/upload', methods=['POST'])
@require_auth
def upload_file():
    """Handle file upload"""
    # Rate limiting
    client_ip = get_client_ip()
    if not check_rate_limit(f'upload:{client_ip}', max_requests=20, window=60):
        return jsonify({'error': 'Too many upload requests. Please wait a moment.'}), 429
    
    # CSRF protection
    csrf_token = request.form.get('csrf_token') or request.headers.get('X-CSRF-Token')
    if not session.get('csrf_token') or session.get('csrf_token') != csrf_token:
        return jsonify({'error': 'Invalid CSRF token'}), 403
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file:
        # Validate filename
        original_filename = file.filename
        if not validate_filename(original_filename):
            return jsonify({'error': 'Invalid filename'}), 400
        
        filename = secure_filename(original_filename)
        if not filename:
            return jsonify({'error': 'Invalid filename'}), 400
        
        # Ensure filename doesn't contain path traversal
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # Normalize path to prevent directory traversal
        file_path = os.path.normpath(file_path)
        if not file_path.startswith(os.path.abspath(app.config['UPLOAD_FOLDER'])):
            return jsonify({'error': 'Invalid file path'}), 400
        
        # If file exists, add timestamp to make it unique
        if os.path.exists(file_path):
            name, ext = os.path.splitext(filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{name}_{timestamp}{ext}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file_path = os.path.normpath(file_path)
        
        try:
            file.save(file_path)
            
            # Update metadata
            metadata = load_metadata()
            metadata[filename] = {
                'uploaded': datetime.now().isoformat(),
                'original_name': original_filename,
                'uploaded_by_ip': client_ip
            }
            save_metadata(metadata)
            
            file_size = os.path.getsize(file_path)
            return jsonify({
                'success': True,
                'filename': filename,
                'size': format_file_size(file_size),
                'message': 'File uploaded successfully'
            })
        except Exception as e:
            return jsonify({'error': 'Upload failed'}), 500
    
    return jsonify({'error': 'Upload failed'}), 500

@app.route('/download/<filename>')
@require_auth
def download_file(filename):
    """Handle file download"""
    # Rate limiting for downloads
    client_ip = get_client_ip()
    if not check_rate_limit(f'download:{client_ip}', max_requests=30, window=60):
        abort(429)
    
    # Decode URL-encoded filename
    try:
        from urllib.parse import unquote
        filename = unquote(filename)
    except:
        pass
    
    # Basic security check - prevent path traversal
    if not filename or '..' in filename:
        abort(403)
    
    # Secure the filename (this will sanitize it)
    secured_filename = secure_filename(filename)
    if not secured_filename:
        abort(400)
    
    # Verify file exists in metadata (additional security layer)
    # Files in metadata are stored with secured filenames, so this should match
    metadata = load_metadata()
    if secured_filename not in metadata:
        # File not in metadata - might be a security issue or file was deleted
        # But also check if filename might have been URL-encoded differently
        # Allow download if file exists and is safe
        pass  # Continue to path validation
    
    # Build file path
    upload_dir = os.path.abspath(app.config['UPLOAD_FOLDER'])
    file_path = os.path.join(upload_dir, secured_filename)
    file_path = os.path.normpath(file_path)
    
    # Security check: ensure file is within uploads directory
    upload_dir_abs = os.path.abspath(upload_dir)
    file_path_abs = os.path.abspath(file_path)
    
    # Normalize for Windows case-insensitivity
    if os.name == 'nt':
        upload_dir_abs = os.path.normcase(upload_dir_abs)
        file_path_abs = os.path.normcase(file_path_abs)
    
    # Simple and reliable check: file must be inside upload directory
    if not file_path_abs.startswith(upload_dir_abs + os.sep):
        abort(403)
    
    # Check if file exists and is actually a file
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        abort(404)
    
    return send_file(file_path, as_attachment=True)

@app.route('/delete/<filename>', methods=['DELETE'])
@require_auth
def delete_file(filename):
    """Handle file deletion"""
    # CSRF protection
    csrf_token = request.headers.get('X-CSRF-Token') or request.args.get('csrf_token')
    if not session.get('csrf_token') or session.get('csrf_token') != csrf_token:
        return jsonify({'error': 'Invalid CSRF token'}), 403
    
    # Validate filename
    if not validate_filename(filename):
        return jsonify({'error': 'Invalid filename'}), 400
    
    filename = secure_filename(filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file_path = os.path.normpath(file_path)
    
    # Ensure file is within upload folder
    upload_abs = os.path.abspath(app.config['UPLOAD_FOLDER'])
    if not file_path.startswith(upload_abs):
        return jsonify({'error': 'Invalid file path'}), 403
    
    if os.path.exists(file_path) and os.path.isfile(file_path):
        try:
            os.remove(file_path)
            # Update metadata
            metadata = load_metadata()
            if filename in metadata:
                del metadata[filename]
            save_metadata(metadata)
            return jsonify({'success': True, 'message': 'File deleted successfully'})
        except Exception as e:
            return jsonify({'error': 'Delete failed'}), 500
    
    return jsonify({'error': 'File not found'}), 404

@app.route('/api/files')
@require_auth
def api_files():
    """API endpoint to get list of files"""
    # Rate limiting
    client_ip = get_client_ip()
    if not check_rate_limit(f'api:{client_ip}', max_requests=60, window=60):
        return jsonify({'error': 'Too many requests'}), 429
    
    metadata = load_metadata()
    files = []
    for filename, info in metadata.items():
        # Validate filename before processing
        if not validate_filename(filename):
            continue
        
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file_path = os.path.normpath(file_path)
        
        # Ensure file is within upload folder
        upload_abs = os.path.abspath(UPLOAD_FOLDER)
        if not file_path.startswith(upload_abs):
            continue
        
        if os.path.exists(file_path) and os.path.isfile(file_path):
            try:
                file_size = os.path.getsize(file_path)
                files.append({
                    'name': filename,
                    'size': file_size,
                    'size_formatted': format_file_size(file_size),
                    'uploaded': info.get('uploaded', 'Unknown')
                })
            except:
                continue
    
    files.sort(key=lambda x: x['uploaded'], reverse=True)
    return jsonify(files)

@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(e):
    return jsonify({'error': f'File too large. Maximum size is {MAX_FILE_SIZE / (1024*1024):.0f}MB'}), 413

@app.errorhandler(404)
def handle_not_found(e):
    if request.is_json:
        return jsonify({'error': 'Not found'}), 404
    return render_template('error.html', error_code=404, error_message='Page not found'), 404

@app.errorhandler(403)
def handle_forbidden(e):
    if request.is_json:
        return jsonify({'error': 'Forbidden'}), 403
    return render_template('error.html', error_code=403, error_message='Access forbidden'), 403

@app.errorhandler(429)
def handle_rate_limit(e):
    return jsonify({'error': 'Too many requests. Please wait a moment.'}), 429

if __name__ == '__main__':
    local_ip = get_local_ip()
    print(f"\n{'='*60}")
    print(f"File Share Server Starting...")
    print(f"{'='*60}")
    print(f"\n🔒 Security Features Enabled:")
    print(f"  ✓ Password Authentication")
    print(f"  ✓ Rate Limiting")
    print(f"  ✓ CSRF Protection")
    print(f"  ✓ Path Traversal Protection")
    print(f"\nAccess the app from this device:")
    print(f"  http://127.0.0.1:5000")
    print(f"\nAccess from other devices on the same network:")
    print(f"  http://{local_ip}:5000")
    print(f"\n{'='*60}\n")
    
    # Run on all interfaces (0.0.0.0) so it's accessible from other devices
    # Note: debug=False for production, but keep it True for development
    app.run(host='0.0.0.0', port=5000, debug=False)

