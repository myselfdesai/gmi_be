from flask import render_template, url_for, request, redirect
from flask import flash, current_app, jsonify
from werkzeug.utils import secure_filename
from csv import DictReader
from gmiapp.forms import UploadForm, DashboardForm
from gmiapp.models import Hospital, Flexstar, HospitalSchema, FlexstarSchema
from gmiapp import app, db
import xml.etree.ElementTree as ET
import json
import os
# import ipdb


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
	"""
	First starting page that gives functionality to accept/upload files two file (csv,xml)
	"""
	form = UploadForm()
	if request.method == 'POST':
		db.drop_all() # delete initial already created database (future we can create different table to maintain upload by user or time and then access the particular data)
		db.create_all() 

		UPLOAD_FOLDER_PATH = current_app.root_path + '/uploads/'
		app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER_PATH
		request.files['hospital_data_file'].save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(request.files['hospital_data_file'].filename)))
		request.files['flexstar_output_file'].save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(request.files['flexstar_output_file'].filename)))

		
		csv_file_path = UPLOAD_FOLDER_PATH + request.files['flexstar_output_file'].filename
		count_index_alphabet = 0
		alphabet_slot = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']	#vertical 8 rows in alphabet list 
		database_list = []

		# parse hospital xml file and save data to Hospital table in db
		tree = ET.parse(UPLOAD_FOLDER_PATH + request.files['hospital_data_file'].filename)
		root = tree.getroot()
		for sample in root.findall('sample'):
			hospital_db_data = Hospital(patient_id=sample.find('patient-id').text,barcode=sample.find('barcode').text)
			db.session.add(hospital_db_data)
			db.session.commit()

		# parse flexstar output csv file and save data to Flexstar table in db
		with open(csv_file_path, 'r') as filecsv:
			csv_reader = DictReader(filecsv)
			"""
			As idea is to get xml data fields. Every slot row has number 1 to 12 so we calculate below 
			and then assign specific alphabet using list(declared as alphabet_slot). This is used to 
			denote slot as a co-ordinates ex. A:10
			"""
			for row in csv_reader:
				if int(row['well_position']) % 12 == 0:
					slot_pos = alphabet_slot[count_index_alphabet] + ':' + row['well_position']
					count_index_alphabet += 1
				else:
					slot_pos = alphabet_slot[count_index_alphabet] + ':' + row['well_position']
				flexstar_db_data = Flexstar(patient_id=row['bpatientID'],twod_barcode=row['2d_barcode'],slot_position=slot_pos)
				db.session.add(flexstar_db_data)
				db.session.commit()
		flash (f'DNA Data extracted from both the files and saved succefully', 'success')
		return redirect(url_for('dashboard'))
	return render_template('home.html', title='Upload Files', form=form)


@app.route("/dashboard")
def dashboard():
	"""
	This view used to display list of all 96 samples in web browser with aggregated data collected from both files
	"""
	form = DashboardForm()
	browser_list = db.session.query(Hospital, Flexstar).outerjoin(Flexstar, Hospital.patient_id == Flexstar.patient_id).all()
	form.browser_list = browser_list
	return render_template('dashboard.html', title='DNA slot dashboard', form=form)


@app.route('/searchsample/', methods=['post'])
def searchsample():
	"""
	Ajax request to get the search result for specific query.
	"""
	form = DashboardForm()
	if form.validate_on_submit():
		if form.criteria_choices.data == 'patient_id':
			qry = db.session.query(Flexstar).join(
				Hospital).filter(Hospital.patient_id == form.search_text.data)
		elif form.criteria_choices.data == 'barcode':
			qry = db.session.query(Flexstar).join(
				Hospital).filter(Hospital.barcode == form.search_text.data)
		elif form.criteria_choices.data == 'twod_barcode':
			qry = db.session.query(Flexstar).join(
				Hospital).filter(Flexstar.twod_barcode == form.search_text.data)
		else:
			qry = db.session.query(Flexstar).join(
				Hospital).filter(Flexstar.slot_position == form.search_text.data)
		
		# used below marshmallow func. to convert modal object to dict that input to jsonify
		flex_schema = FlexstarSchema(many=True)
		flexstar_list = flex_schema.dump(qry)

		hs_schema = HospitalSchema(many=True)
		hospital_list = hs_schema.dump(qry)

		return jsonify(data={'message': 'success', 'hospital_json': hospital_list, 'flexstar_json':flexstar_list})
	return jsonify(data=form.errors)
