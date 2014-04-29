from flask.ext.script import Manager, Server

from api import api, add_document

manager = Manager(api)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger=True,
    use_reloader=True,
    host='0.0.0.0')
)

waterpoint_schema = {
    'date_recorded': {
        'type': 'datetime',
    },
    'company': {
        'type': 'string',
    },
    'region': {
        'type': 'string',
    },
    'district': {
        'type': 'string',
    },
    'lga_name': {
        'type': 'string',
    },
    'ward': {
        'type': 'string',
    },
    'village': {
        'type': 'string',
    },
    'village_po': {
        'type': 'string',
    },
    'village_re': {
        'type': 'string',
    },
    'village_ph': {
        'type': 'string',
    },
    'subvillage': {
        'type': 'string',
    },
    'wpt_name': {
        'type': 'string',
    },
    'wpt_code': {
        'type': 'string',
        # 'unique': True, FIXME: These are not unique in the dataset
    },
    'population': {
        'type': 'integer',
    },
    'scheme_name': {
        'type': 'string',
    },
    'water_perm': {
        'type': 'string',
    },
    'catchment': {
        'type': 'string',
    },
    'funder': {
        'type': 'string',
    },
    'installer': {
        'type': 'string',
    },
    'construction_year': {
        'type': 'datetime',
    },
    'source_type': {
        'type': 'string',
    },
    'extraction': {
        'type': 'string',
    },
    'waterpoint': {
        'type': 'string',
    },
    'status_detail': {
        'type': 'string',
    },
    'status': {
        'type': 'string',
        'allowed': ['Functional', 'Not functional'],
    },
    'breakdown_year': {
        'type': 'datetime',
    },
    'hardware_defect': {
        'type': 'string',
    },
    'reason_wpt': {
        'type': 'string',
    },
    'water_quantity': {
        'type': 'string',
    },
    'water_quality': {
        'type': 'string',
    },
    'scheme_management': {
        'type': 'string',
    },
    'wp_management': {
        'type': 'string',
    },
    'water_payment': {
        'type': 'string',
    },
    'amount_tsh': {
        'type': 'float',
    },
    'public_meeting': {
        'type': 'string',
    },
    'comment': {
        'type': 'string',
    },
    'gps_height': {
        'type': 'float',
    },
    'latitude': {
        'type': 'float',
    },
    'longitude': {
        'type': 'float',
    },
}


def check(response):
    assert response.status_code == 201, response.data
    print response.data


@manager.command
def create_waterpoints():
    """Create facility for waterpoints."""
    check(add_document('facilities',
                       {'facility_code': "wp001",
                        'facility_name': "Waterpoint",
                        'fields': waterpoint_schema,
                        'description': "A waterpoint in Tanzania",
                        'keywords': ["location", "water", "infrastructure"],
                        'group': "water",
                        'endpoint': "waterpoints"}))

if __name__ == "__main__":
    manager.run()
