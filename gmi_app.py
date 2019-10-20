from flask import Flask, render_template, url_for
from forms import UploadForm
from werkzeug.utils import secure_filename
app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
	form = UploadForm()

	if form.validate_on_submit():
		filename = secure_filename(form.hospital_data_file.data.filename)
		form.hospital_data_file.data.save('uploads/' + filename)
		return redirect(url_for('dashboard'))
	return render_template('home.html', title='Upload Files', form=form)

if __name__ == '__main__':
	app.run(debug=True)