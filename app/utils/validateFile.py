ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    ext = filename.rsplit('.', 1)[1].lower()
    return '.' in filename and \
           ext in ALLOWED_EXTENSIONS , ext