# Copyright (c) 2023, Ideenkreice and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.share import add as add_share
import requests
import json
import re

class VendorDetails(Document):
	pass
				
@frappe.whitelist()
def duplicate(name,pan_number,din,mobile):
	vendor_data=frappe.db.sql("""select name,din,mobile_number,pan_number,status from `tabVendor Details` where name !=%(name)s and ( din=%(din)s or pan_number=%(pan_number)s 
		or mobile_number=%(mobile_number)s)""",values={'din':din,'pan_number':pan_number,'mobile_number':mobile,'name':name},as_dict=1)
	

	for d in vendor_data:
		
		description=[]
		if d.din is not '':
			

			if d.din==din:
				description.append("Din Number")
		if d.pan_number is not '':

			if d.pan_number==pan_number:
				description.append("Pan Number")
		if d.mobile_number==mobile:
			description.append("Mobile Number")
		description_str = ', '.join(description)+" Duplicated"
		
		d['description'] = description_str
	return vendor_data


# @frappe.whitelist()
# def get_vendor_data():
# 	url="http://localhost:8030/api/method/vendormanagement.vendor_management.doctype.vendor_details.vendor_details.get_vendor_list"
# 	response = requests.request("GET", url,headers = {
# 			'Content-Type': 'application/json',
# 				})
# 	response_data=response.json()
	
# 	print("Response:",response_data)
@frappe.whitelist(allow_guest=True)
def get_vendor_list():
	
	data=frappe.db.sql("""select * from `tabVendor Details` """,as_dict=1)
	print("data",data)
	return data

@frappe.whitelist()
def get_vendor_data():
	url="http://35.154.0.123:82/api/method/vendormanagement.vendor_management.doctype.vendor_details.vendor_details.get_vendor_list"
	# url="http://localhost:8030/api/method/vendormanagement.vendor_management.doctype.vendor_details.vendor_details.get_vendor_list"
	response = requests.request("GET", url,headers = {
			'Content-Type': 'application/json',
				})
	response_data=response.json()
	print("Response:",response_data)
	receive_and_create_vendor_data(response_data)
	return response_data
	

@frappe.whitelist(allow_guest=True)
def receive_and_create_vendor_data(response_data):
	# Deserialize the received data
		received_data = response_data
		print("received_data",received_data)

		for d in received_data["message"]:
			name = d["name"]
			if name:
				existing_doc = frappe.db.exists("Vendor Details", {"name1": name})
				if existing_doc:
					print("Document with name {} already exists.".format(name))

				else:
					new_doc=frappe.new_doc("Vendor Details")
					new_doc.name1=name
					new_doc.address1=d['address1']
					new_doc.address_2=d['address_2']
					new_doc.bank_branch=d['bank_branch']
					new_doc.bank_name=d['bank_name']
					new_doc.attachements=d['attachements']
					new_doc.city=d['city']
					new_doc.contact_person_1=d['contact_person_1']
					new_doc.contact_person_2=d['contact_person_2']
					new_doc.din=d['din']
					new_doc.gst_provisional_id=d['gst_provisional_id']
					new_doc.ifsc_code=d['ifsc_code']
					new_doc.mobile_number=d['mobile_number']
					new_doc.msme_category=d['msme_category']
					new_doc.pan_number=d['pan_number']
					new_doc.pin_code=d['pin_code']
					new_doc.state=d['state']
					new_doc.status=d['status']
					new_doc.street=d['street']
					new_doc.telephone_number=d['telephone_number']
					new_doc.vendor_name=d['vendor_name']
					new_doc.banking_account_number=d['banking_account_number']

					new_doc.insert(ignore_permissions=True)

					# Attach files to the document using the path provided
					if d['attachements'] is not None:
						attachment_path =d['attachements']
						# for attachment_path in d['attachements']:
						print("attachment_path",attachment_path)
						filename = os.path.basename(attachment_path)
						print("filename",filename)
					
					# Save the URL to attach the file
						save_url(attachment_path,filename,"Vendor Details",new_doc.name, "Home", is_private=1)

		return "Data received and processed successfully."


