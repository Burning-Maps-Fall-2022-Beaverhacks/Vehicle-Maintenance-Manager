"""Form object declaration."""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class AddVehicleForm(FlaskForm):
    """Add New Vehicle"""
    year = StringField(
        'Year',
        [DataRequired()]
    )
    make = StringField(
        'Make',
        [DataRequired()]
    )
    model = StringField(
        'Model',
        [DataRequired()]
    )
    mileage = StringField(
        'Mileage',
        [DataRequired()]
    )
    color = StringField(
        'Color',
        [DataRequired()]
    )
    submit = SubmitField('Add Vehicle')
