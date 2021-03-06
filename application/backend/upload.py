from werkzeug.utils import secure_filename
from application import app
from application.models import db, Part
import os

ALLOWED_EXTENSIONS = set(['csv', 'txt'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file(request):
	if 'file' not in request:
		'No file to upload'
	file = request['file']
	if file.filename == '':
		return 'Filename is blank'
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		fh = open(filepath, "r")
		parts = []
		Part.query.delete()
		for line in fh:
			parts = line.split(",")
			desired_qty=int(int(parts[4])*.75)
			part = Part(partnum=parts[0], name=parts[1], vendor=parts[2], location=parts[3], quantity=parts[4], desired_qty=desired_qty, available_qty=parts[5])
			db.session.add(part)
		db.session.commit()
		return file.filename
