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
	
	# Enviar a VTEX
	def send_to_vtex(self):
		url = "https://dmujeresec.myvtex.com/api/logistics/pvt/configuration/pickuppoints/" + str(self.store_id)
		headers = {
			'Content-Type': 'application/json',
			'Accept': 'application/json',
			'X-VTEX-API-AppKey': '',
			'X-VTEX-API-AppToken': ''
		}
		
		# add Domingo to data days if is checked
		domingo = False
		if self.store_openingTime_0 and self.store_closingTime_0:
			tzd = pytz.timezone('America/Guayaquil')
			domingo = {
				"dayOfWeek": self.store_business_hours_day_of_week_0,
				"openingTime": str(self.store_openingTime_0.astimezone(tzd))[11:19],
				"closingTime": str(self.store_closingTime_0.astimezone(tzd))[11:19]
			}
		
		# add Lunes to data days if is checked
		if self.store_openingTime_1 and self.store_closingTime_1:
			tzl = pytz.timezone('America/Guayaquil')
			lunes = {
				"dayOfWeek": self.store_business_hours_day_of_week_1,
				"openingTime": str(self.store_openingTime_1.astimezone(tzl))[11:19],
				"closingTime": str(self.store_closingTime_1.astimezone(tzl))[11:19]
			}
		else:
			lunes = {
				"dayOfWeek": self.store_business_hours_day_of_week_1,
				"openingTime": "00:00:00",
				"closingTime": "00:00:00"
			}
		
		# add Martes to data days if is checked
		if self.store_openingTime_2 and self.store_closingTime_2:
			tzm = pytz.timezone('America/Guayaquil')
			martes = {
				"dayOfWeek": self.store_business_hours_day_of_week_2,
				"openingTime": str(self.store_openingTime_2.astimezone(tzm))[11:19],
				"closingTime": str(self.store_closingTime_2.astimezone(tzm))[11:19]
			}
		else:
			martes = {
				"dayOfWeek": self.store_business_hours_day_of_week_2,
				"openingTime": "00:00:00",
				"closingTime": "00:00:00"
			}
		
		# add Miercoles to data days if is checked
		if self.store_openingTime_3 and self.store_closingTime_3:
			tzmi = pytz.timezone('America/Guayaquil')
			miercoles = {
				"dayOfWeek": self.store_business_hours_day_of_week_3,
				"openingTime": str(self.store_openingTime_3.astimezone(tzmi))[11:19],
				"closingTime": str(self.store_closingTime_3.astimezone(tzmi))[11:19]
			}
		else:
			miercoles = {
				"dayOfWeek": self.store_business_hours_day_of_week_3,
				"openingTime": "00:00:00",
				"closingTime": "00:00:00"
			}
		
		# add Jueves to data days if is checked
		if self.store_openingTime_4 and self.store_closingTime_4:
			tzj = pytz.timezone('America/Guayaquil')
			jueves = {
				"dayOfWeek": self.store_business_hours_day_of_week_4,
				"openingTime": str(self.store_openingTime_4.astimezone(tzj))[11:19],
				"closingTime": str(self.store_closingTime_4.astimezone(tzj))[11:19]
			}
		else:
			jueves = {
				"dayOfWeek": self.store_business_hours_day_of_week_4,
				"openingTime": "00:00:00",
				"closingTime": "00:00:00"
			}
		
		# add Viernes to data days if is checked
		if self.store_openingTime_5 and self.store_closingTime_5:
			tzv = pytz.timezone('America/Guayaquil')
			viernes = {
				"dayOfWeek": self.store_business_hours_day_of_week_5,
				"openingTime": str(self.store_openingTime_5.astimezone(tzv))[11:19],
				"closingTime": str(self.store_closingTime_5.astimezone(tzv))[11:19]
			}
		else:
			viernes = {
				"dayOfWeek": self.store_business_hours_day_of_week_5,
				"openingTime": "00:00:00",
				"closingTime": "00:00:00"
			}
		
		# add Sabado to data days if is checked
		if self.store_openingTime_6 and self.store_closingTime_6:
			tzs = pytz.timezone('America/Guayaquil')
			sabado = {
				"dayOfWeek": self.store_business_hours_day_of_week_6,
				"openingTime": str(self.store_openingTime_6.astimezone(tzs))[11:19],
				"closingTime": str(self.store_closingTime_6.astimezone(tzs))[11:19]
			}
		else:
			sabado = {
				"dayOfWeek": self.store_business_hours_day_of_week_6,
				"openingTime": "00:00:00",
				"closingTime": "00:00:00"
			}
		
		# add all days to data
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
			"businessHours": [
				lunes,
				martes,
				miercoles,
				jueves,
				viernes,
				sabado,
				domingo
			],
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
		
		# send data and update store in vtex
		try:
			response = requests.put(url, headers=headers, json=data)
			print("Response:", response.status_code)
			print("Response Content:", response.content)
			
			# convert data to json *optional
			data_json = json.dumps(data)
			data_load = json.loads(data_json)
			print("Data:", data)
			print("Id:", data_load["id"])
			print("Nombre:", data_load.get("name"))
			print("Activo:", data_load["isActive"])
		except Exception as e:
			print("ERRORES", e.__class__.__name__)
			# print where line fails and error message
			exc_type, exc_obj, exc_tb = sys.exc_info()
			print("Error:", exc_type, exc_tb.tb_lineno, e)
			# print where fail the code and error message
			print("Error:", sys.exc_info()[0], sys.exc_info()[1])
			return False
	
	# execute method after save
	@api.model
	def create(self, vals):
		res = super(AddPickupPoints, self).create(vals)
		res.send_to_vtex()
		return res
	
	# execute method after update
	def write(self, vals):
		res = super(AddPickupPoints, self).write(vals)
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
