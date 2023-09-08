from marshmallow import Schema, fields, validate

# Define a schema for the User model
class UserSchema(Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    role = fields.Str(
        required=True,
        validate=validate.OneOf(choices=['alumni', 'student'])
    )
    email = fields.Email(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    location = fields.Str(required=True)
    company_name = fields.Str(required=True)

# Define a schema for the Alumni model
class AlumniSchema(Schema):
    company_name = fields.String(required=True)
    
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    role = fields.Str(
        required=True,
        validate=validate.OneOf(choices=['alumni', 'student'])
    )
    email = fields.Email(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    location = fields.Str(required=True)
    company_name = fields.Str(required=True)

# Define a schema for the Student model
class StudentSchema(Schema):
    school = fields.String(required=True)
    year_in_school = fields.Integer(required=True)
    major = fields.String(required=True)
    degree = fields.String(
        required=True,
        validate=validate.OneOf(choices=['BS', 'MS'])
    )

    graduation_year = fields.DateTime(required=True)

    # user validation
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    role = fields.Str(
        required=True,
        validate=validate.OneOf(choices=['alumni', 'student'])
    )
    email = fields.Email(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    location = fields.Str(required=True)
    company_name = fields.Str(required=True)