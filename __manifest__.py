{
	'name': 'DMujeres Admin Pickup Points',
	'author': 'DMujeres Beauty Market',
	'website': 'https://www.dmujeres.ec',
	'license': 'LGPL-3',
	'version': '1.0.0',
	'depends': ['base', 'website', 'web_studio'],
	'data': [
		'views/views.xml',
		'views/menu.xml',
		'security/ir.model.access.csv',
	],
	'assets': {
		'web.assets_backend': [
			'/admin_pickup_points/static/src/js/utils.js',
		]
	},
}
