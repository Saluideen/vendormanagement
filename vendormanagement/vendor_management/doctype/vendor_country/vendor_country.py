import frappe
from frappe.model.document import Document
import requests
import json
from frappe.utils.background_jobs import enqueue

class VendorCountry(Document):
    def on_update(self):
        frappe.enqueue(self.set_country)
    def after_rename(self, old, new, merge=False):
        base_url=get_api_settings()
        # rename_country()
        # url = "http://192.168.29.100:8002/api/method/vendormanagement.vendor_management.doctype.vendor_country.vendor_country.rename_country"
        url = base_url['base_url']+"/api/method/vendormanagement.vendor_management.doctype.vendor_country.vendor_country.rename_country"
        data = {
            "old":old,
            "new": new,
            
        }

        try:
            response = requests.post(url, headers={'Content-Type': 'application/json'}, json=data)
            if response.status_code == 200:
                print("Country data updated on the external server.")
            else:
                print("Failed to update country data on the external server. Status code:", response.status_code)
        except requests.exceptions.RequestException as e:
            print("An error occurred during the request:", e)
        
    def on_trash(self):
        self.remove_country()
    def remove_country(self):
        base_url=get_api_settings()
        if base_url['base_url']:
            data={
            "name":self.name

            }
            url= base_url['base_url']+"/api/method/vendormanagement.vendor_management.doctype.vendor_country.vendor_country.get_country_remove"
            # url="http://192.168.29.100:8002/api/method/vendormanagement.vendor_management.doctype.vendor_country.vendor_country.get_country_remove"
            # url = "http://localhost:8030/api/method/demo.demo.doctype.demo_country.demo_country.remove_country"
            response = requests.request("DELETE", url,headers = {
            'Content-Type': 'application/json',
            },json=data)
            response_data=response.json()
            print("Response:",response_data)
            return response_data

    def set_country(self):
        base_url=get_api_settings()
        
        if self.status=="unsync":
            url = base_url['base_url']+"/api/method/vendormanagement.vendor_management.doctype.vendor_country.vendor_country.update_country"
            # url = "http://localhost:8030/api/method/demo.demo.doctype.demo_country.demo_country.update_country"
            data = {
                "name":self.name,
                "country": self.country,
                "country_code": self.country_code
            }

            try:
                response = requests.post(url, headers={'Content-Type': 'application/json'}, json=data)
                if response.status_code == 200:
                    print("Country data updated on the external server.")
                else:
                    print("Failed to update country data on the external server. Status code:", response.status_code)
            except requests.exceptions.RequestException as e:
                print("An error occurred during the request:", e)
@frappe.whitelist(allow_guest=True)
def rename_country():
    data = frappe.form_dict
    frappe.db.sql("""
        UPDATE `tabVendor Country`
        SET name = %s
        WHERE name = %s
        """, (data.new, data.old))

@frappe.whitelist(allow_guest=True)
def update_country():
    data = frappe.form_dict
    try:
        # Check if a Vendor Country document with the given ID already exists
        existing_doc = frappe.get_all("Vendor Country", filters={"country": data.get("country")})

        if existing_doc:
            # Update the existing document with the new data
            existing_doc = frappe.get_doc("Vendor Country", existing_doc[0].name)
            existing_doc.country_code = data.get("country_code")
            existing_doc.save(ignore_permissions=True)
        else:
            # Create a new Vendor Country document and enter the data into it
            new_doc = frappe.new_doc("Vendor Country")
            new_doc.country = data.get("country")
            new_doc.country_code = data.get("country_code")
            new_doc.status="sync"
            new_doc.insert(ignore_permissions=True)

        return "Country data updated or created successfully"
    except Exception as e:
        return "An error occurred while processing the request: " + str(e)

@frappe.whitelist()
def get_country_list():
    
    
    country_list = frappe.get_all("Vendor Country", fields=["id", "country", "country_code"])
    return country_list
@frappe.whitelist(allow_guest=True)
def get_country_remove():
    data=frappe.form_dict
    
    frappe.delete_doc('Vendor Country',data.name)
frappe.whitelist()
def get_api_settings():
	base_url=frappe.get_doc("Vendor API Settings").base_url
	api_key=frappe.get_doc("Vendor API Settings").api_key
	api_secret=frappe.get_doc("Vendor API Settings").api_secret
	return {'base_url':base_url,'api_key':api_key,'api_secret':api_secret}
	
