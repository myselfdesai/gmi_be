from flask import render_template, url_for, request, redirect
from flask import flash, current_app, jsonify
from werkzeug.utils import secure_filename
from csv import DictReader
from gmiapp.forms import UploadForm, DashboardForm
from gmiapp.models import Hospital, Flexstar, HospitalSchema, FlexstarSchema
from gmiapp import app, db
import xml.etree.ElementTree as ET
import json
# import ipdb


def allowed_file_hospital_data(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in 'xml'


def allowed_file_flexstar_data(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in 'csv'


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
	form = UploadForm()

	if request.method == 'POST':
		db.drop_all()
		db.create_all()
		# if user does not select file, handle the user submit here

		# if request.files['hospital_data_file'].filename == '':
		# 	flash('No Hospital File provided','danger')
		# 	return redirect(request.url)
		# if request.files['flexstar_output_file'].filename == '':
		# 	flash('No Flexstar File provided','danger')
		# 	return redirect(request.url)

		# form.hospital_data_file.data.save('uploads/' + secure_filename(form.hospital_data_file.data.filename))
		# form.flexstar_output_file.data.save('uploads/' + secure_filename(form.flexstar_output_file.data.filename))

		UPLOAD_FOLDER_PATH = current_app.root_path+'/uploads/'
		csv_file_path = UPLOAD_FOLDER_PATH+request.files['flexstar_output_file'].filename
		count_index_alphabet = 0
		alphabet_slot = ['A','B','C','D','E','F','G','H']
		database_list = []

		# parse hospital xml file and save data to Hospital table in db
		tree = ET.parse(UPLOAD_FOLDER_PATH+request.files['hospital_data_file'].filename)
		root = tree.getroot()
		for sample in root.findall('sample'):
			hospital_db_data = Hospital(patient_id=sample.find('patient-id').text,barcode=sample.find('barcode').text)
			db.session.add(hospital_db_data)
			db.session.commit()

		# parse flexstar output csv file and save data to Flexstar table in db
		with open(csv_file_path,'r') as filecsv:
			csv_reader = DictReader(filecsv)
			for row in csv_reader:
				if int(row['well_position']) % 12 == 0:
					slot_pos = alphabet_slot[count_index_alphabet]+':'+row['well_position']
					count_index_alphabet += 1
				else:
					slot_pos = alphabet_slot[count_index_alphabet]+':'+row['well_position']
				flexstar_db_data = Flexstar(patient_id=row['bpatientID'],twod_barcode=row['2d_barcode'],slot_position=slot_pos)
				db.session.add(flexstar_db_data)
				db.session.commit()
		flash (f'DNA Data extracted from both the files and saved succefully', 'success')
		# return redirect(url_for('dashboard'))
	return render_template('home.html', title='Upload Files', form=form)


@app.route("/dashboard")
def dashboard():
	form = DashboardForm()
	browser_list = db.session.query(Hospital, Flexstar).outerjoin(Flexstar, Hospital.patient_id == Flexstar.patient_id).all()
	form.browser_list=browser_list
	return render_template('dashboard.html', title='DNA slot dashboard', form=form)


@app.route('/searchsample/', methods=['post'])
def searchsample():
	form = DashboardForm()
	if form.validate_on_submit():
		# browser_list = db.session.query(Hospital, Flexstar).outerjoin(Flexstar, Hospital.patient_id == Flexstar.patient_id).all()
		# query_for_search =  db.session.query(Hospital, Flexstar).outerjoin(Flexstar, Hospital.patient_id == Flexstar.patient_id).all()

		if form.criteria_choices.data == 'patient_id':
			qry = db.session.query(Flexstar).join(
				Hospital, Hospital.patient_id == Flexstar.patient_id).filter(
				Hospital.patient_id == form.search_text.data)
		elif form.criteria_choices.data == 'barcode':
			qry = db.session.query(Flexstar).join(
				Hospital, Hospital.patient_id == Flexstar.patient_id).filter(
				Hospital.barcode == form.search_text.data)
		elif form.criteria_choices.data == 'twod_barcode':
			qry = db.session.query(Flexstar).join(
				Hospital, Hospital.patient_id == Flexstar.patient_id).filter(
				Flexstar.twod_barcode == form.search_text.data)
		else:
			qry = db.session.query(Flexstar).join(
				Hospital, Hospital.patient_id == Flexstar.patient_id).filter(
				Flexstar.slot_position == form.search_text.data)
		
		hs_schema = HospitalSchema(many=True)
		hospital_list = hs_schema.dump(qry)


		flex_schema = FlexstarSchema(many=True)
		flexstar_list = flex_schema.dump(qry)

		return jsonify(data={'message': 'success','hospital_json':hospital_list,'flexstar_json':flexstar_list})
	return jsonify(data=form.errors)
