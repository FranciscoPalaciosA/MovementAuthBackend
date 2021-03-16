from api.restplus import api
from flask_restplus import fields

create_user_args = api.model('Data to create user', {
    "email": fields.String(description="Email of the user"),
    "name": fields.String(description="Name of the user")
})

view_response = api.model('User View Permissions', {
    "general": fields.Boolean(description='Permission on general view', default=True),
    "weather": fields.Boolean(description='Permission on weather view', default=True),
    "satellite": fields.Boolean(description='Permission on satellite view', default=True),
    "planting_tool": fields.Boolean(description='Permission on planting tool view', default=True),
    "weather_tool": fields.Boolean(description='Permission on weather tool view', default=True),
    "default": fields.String(description='Default view to be loaded', default="general")
})

report_types = api.model('Report types that can be authorized', {
    "harvest": fields.Boolean(description='Permission on generating harvest reports', default=True),
    "planting": fields.Boolean(description='Permission on generating planting reports', default=False),
    "weather": fields.Boolean(description='Permission on generating weather reports', default=False)
})

functionality_response = api.model('User Functionality Permissions', {
    "report_generation": fields.Nested(report_types, description='Permission on generating reports'),
})

permissions_response = api.model('User Permissions', {
    "views": fields.Nested(view_response),
    "features": fields.Nested(functionality_response),
})

user_response = api.model('User', {
    "name": fields.String(description='Name of the user', default="unknown"),
    "company": fields.String(description='Company of the user', default="unknown")
})
