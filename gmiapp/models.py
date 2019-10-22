from gmiapp import db, ma
from sqlalchemy.orm import relationship, backref


class Hospital(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	patient_id = db.Column(db.String(10))
	barcode = db.Column(db.String(10))

	def __repr__(self):
		return f"Hospital('{self.patient_id}','{self.barcode}')"


class Flexstar(db.Model):
	id = db.Column(db.Integer,primary_key=True, autoincrement=True)
	patient_id = db.Column(db.String(10), db.ForeignKey('hospital.patient_id'))
	twod_barcode = db.Column(db.String(10))
	slot_position = db.Column(db.String(5))
	hospital = relationship("Hospital", backref=backref("flexstar"))
	
	def __repr__(self):
		return f"Flexstar('{self.twod_barcode}','{self.slot_position}')"


class HospitalSchema(ma.ModelSchema):
	class Meta:
		model = Hospital


class FlexstarSchema(ma.ModelSchema):
	# hospital = ma.Nested(HospitalSchema, many=True)
	class Meta:
		model = Flexstar

