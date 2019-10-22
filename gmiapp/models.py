from gmiapp import db, ma
from marshmallow_sqlalchemy import fields

class Hospital(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	patient_id = db.Column(db.String(10), nullable=False)
	barcode = db.Column(db.String(10))

	def __repr__(self):
		return f"FlexstarOutput('{self.patient_id}','{self.barcode}')"


class Flexstar(db.Model):
	id = db.Column(db.Integer,primary_key=True, autoincrement=True)
	patient_id = db.Column(db.String(10),db.ForeignKey('hospital.patient_id'), nullable=False)
	twod_barcode = db.Column(db.String(10))
	slot_position = db.Column(db.String(5))

	def __repr__(self):
		return f"Flexstar('{self.twod_barcode}','{self.slot_position}')"


class HospitalSchema(ma.ModelSchema):
	class Meta:
		model = Hospital


class FlexstarSchema(ma.ModelSchema):
	flexstar = fields.Nested(HospitalSchema)
	class Meta:
		model = Flexstar