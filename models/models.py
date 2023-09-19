import base64
import datetime
import re
import sys

import pytz
import requests
from odoo import models, fields, api
from odoo.addons.website import tools
from odoo.tools import json
import json
import logging

_logger = logging.getLogger(__name__)

class AddPickupPoints(models.Model):
    _name = 'add.pickup_points'
    _description = 'Stores Odoo From View To Vtex'
    
    # Fields
    store_id = fields.Integer(string='Id', required=True, max_length=10)
    store_name = fields.Char(string='Nombre', required=False)
    store_description = fields.Char(string='URL de la foto', required=False,
	                                placeholder='https://www.macronegocios.ec/document/share/36/265bbb2d-f313-4689-8868-d298b3d417bd')
    store_formatted_address = fields.Char(string='Dirección Formateada', required=False)
    store_address_postal_code = fields.Char(string='Codigo Postal', required=False)
    store_city = fields.Char(string='Ciudad', required=False)
    store_state = fields.Char(string='Provincia', required=False)
    store_address_street = fields.Char(string='Calle', required=False)
    store_address_complement = fields.Char(string='Complemento Direccion', required=False)
    store_address_location_latitude = fields.Char(string='Latitude', required=False)
    store_address_location_longitude = fields.Char(string='Longitude', required=False)
    store_tags_label = fields.Char(string='Ciudad Tags Label', required=False)
    store_is_active = fields.Selection([('true', 'SI'), ('false', 'NO')], string='Esta Activa', required=False)
    store_image = fields.Binary(compute='_compute_store_image', required=False, string=' ')
	
	# Business Hours Domingo
    store_business_hours_day_of_week_0 = fields.Selection([('0', 'Domingo')], string='Domingo', required=False)
    store_openingTime_0 = fields.Datetime(string='Abre el Domingo', required=False, formatter='hh:mm:ss')
    store_closingTime_0 = fields.Datetime(string='Cierra el Domingo', required=False, formatter='hh:mm:ss')
	# Business Hours Lunes
    store_business_hours_day_of_week_1 = fields.Selection([('1', 'Lunes')], string='Lunes', required=False,
	                                                      selected='true')
    store_openingTime_1 = fields.Datetime(string='Abre el Lunes', required=False, formatter='hh:mm:ss',
	                                      default='10:00:00')
    store_closingTime_1 = fields.Datetime(string='Cierra el Lunes', required=False, formatter='hh:mm:ss')
	# Business Hours Martes
    store_business_hours_day_of_week_2 = fields.Selection([('2', 'Martes')], string='Martes', required=False)
    store_openingTime_2 = fields.Datetime(string='Abre el Martes', required=False, formatter='hh:mm:ss')
    store_closingTime_2 = fields.Datetime(string='Cierra el Martes', required=False, formatter='hh:mm:ss')
	
    store_business_hours_day_of_week_3 = fields.Selection([('3', 'Miercoles')], string='Miercoles', required=False)
    store_openingTime_3 = fields.Datetime(string='Abre el Miercoles', required=False, formatter='hh:mm:ss')
    store_closingTime_3 = fields.Datetime(string='Cierra el Miercoles', required=False, formatter='hh:mm:ss')
	
    store_business_hours_day_of_week_4 = fields.Selection([('4', 'Jueves')], string='Jueves', required=False)
    store_openingTime_4 = fields.Datetime(string='Abre el Jueves', required=False, formatter='hh:mm:ss')
    store_closingTime_4 = fields.Datetime(string='Cierra el Jueves', required=False, formatter='hh:mm:ss')
	
    store_business_hours_day_of_week_5 = fields.Selection([('5', 'Viernes')], string='Viernes', required=False)
    store_openingTime_5 = fields.Datetime(string='Abre el Viernes', required=False, formatter='hh:mm:ss')
    store_closingTime_5 = fields.Datetime(string='Cierra el Viernes', required=False, formatter='hh:mm:ss')
	
    store_business_hours_day_of_week_6 = fields.Selection([('6', 'Sabado')], string='Sabado', required=False)
    store_openingTime_6 = fields.Datetime(string='Abre el Sabado', required=False, formatter='hh:mm:ss')
    store_closingTime_6 = fields.Datetime(string='Cierra el Sabado', required=False, formatter='hh:mm:ss')

    # Helper Function
    def create_business_hour(self, opening_time, closing_time, day):
        tz = pytz.timezone('America/Guayaquil')
        return {
            "dayOfWeek": day,
            "openingTime": str(opening_time.astimezone(tz))[11:19] if opening_time else "00:00:00",
            "closingTime": str(closing_time.astimezone(tz))[11:19] if closing_time else "00:00:00"
        }
        
    def send_to_vtex(self):
        url = f"https://dmujeresec.myvtex.com/api/logistics/pvt/configuration/pickuppoints/{self.store_id}"
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-VTEX-API-AppKey': '',
            'X-VTEX-API-AppToken': ''
        }
        
        business_hours = []
        for i in range(7):
            opening_time = getattr(self, f'store_openingTime_{i}')
            closing_time = getattr(self, f'store_closingTime_{i}')
            day = getattr(self, f'store_business_hours_day_of_week_{i}')
            business_hours.append(self.create_business_hour(opening_time, closing_time, day))
        
        data = {
            "id": str(self.store_id),
			"name": self.store_name,
			"description": "{\"image\": ""\"" + str(self.store_description) + "\"}",
			"instructions": "",
			"formatted_address": self.store_formatted_address,
			"address": {
				"postalCode": self.store_address_postal_code,
				"country": {
					"acronym": "ECU",
					"name": "Ecuador"
				},
				"city": self.store_city,
				"state": self.store_state,
				"neighborhood": "",
				"street": self.store_address_street,
				"number": "",
				"complement": self.store_address_complement,
				"reference": "",
				"location": {
					"latitude": self.store_address_location_latitude,
					"longitude": self.store_address_location_longitude
				}
			},
			"isActive": self.store_is_active,
			"distance": 1661450584064.0,
			"seller": "dmujeresec",
			"_sort": [
				1.66145058
			],
            "businessHours": business_hours,
            "tagsLabel": [
				self.store_tags_label
			],
			"pickupHolidays": [],
			"isThirdPartyPickup": "false",
			"accountOwnerName": "dmujeresec",
			"accountOwnerId": "3dfe14c0-f3de-423e-8bd5-f0aac72368b5",
			"parentAccountName": "",
			"originalId": ""
        }
        
        try:
            response = requests.put(url, headers=headers, json=data)
            _logger.info(f"Response: {response.status_code}")
        except Exception as e:
            _logger.error(f"Error: {e}, Line: {sys.exc_info()[2].tb_lineno}")
            return False

    @api.model
    def create(self, vals):
        res = super().create(vals)
        res.send_to_vtex()
        return res

    def write(self, vals):
        res = super().write(vals)
        self.send_to_vtex()
        return res

	# convierto la url a imagen binaria y la guardo en store_image
    def _compute_store_image(self):
		# convert url to image binary
        if self.store_description:
            url = self.store_description
            response = requests.get(url)
			# save image binary in store_image
            self.store_image = base64.b64encode(response.content)
