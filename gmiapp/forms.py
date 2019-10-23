from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField,SelectField,TextField
from wtforms import validators, ValidationError


class UploadForm(FlaskForm):
	hospital_data_file = FileField('Hospital Data Input File',[validators.Required(),FileAllowed(['xml'], 'xml only!')])
	flexstar_output_file = FileField('Flexstar Output File',[validators.Required(),FileAllowed(['csv'], 'CSV only!')])
	submit = SubmitField('Importdata')


class DashboardForm(FlaskForm):
	CRITERIA = [('patient_id','patient ID'),('twod_barcode', '2D barcode'),('slot_position', 'Slot')]
	
	search_text = TextField(u'Search Text',[validators.Required("Please enter text to search.")])
	criteria_choices = SelectField(label='State', choices=CRITERIA)

