from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField
from wtforms.validators import DataRequired

class UploadForm(FlaskForm):
	hospital_data_file = FileField('Hospital Data Input', validators=[FileAllowed(['xml'])])
	flexstar_output_file = FileField('Flexstar Output', validators=[FileAllowed(['csv'])])
	submit = SubmitField('Importdata')
