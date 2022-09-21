from encodings import search_function
from odoo import models, api, fields
from datetime import datetime
import math

class PrintPDFWizard(models.TransientModel):
    _name = "print.pdf"

    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')

    def print_pdf_bt(self):
        vat_none = self.env['custom.accounting.tax.report'].search([("create_date", ">=", self.start_date), ("create_date", "<=", self.end_date), ("tax_name", "=", "Không Chịu Thuế GTGT")])
        vat_0 = self.env['custom.accounting.tax.report'].search([("create_date", ">=", self.start_date), ("create_date", "<=", self.end_date), ("tax_name", "=", "Value Added Tax (VAT) 0%")])
        vat_5 = self.env['custom.accounting.tax.report'].search([("create_date", ">=", self.start_date), ("create_date", "<=", self.end_date), ("tax_name", "=", "Value Added Tax (VAT) 5%")])
        vat_10 = self.env['custom.accounting.tax.report'].search([("create_date", ">=", self.start_date), ("create_date", "<=", self.end_date), ("tax_name", "=", "Value Added Tax (VAT) 10%")])

        company_name = self.env['custom.accounting.current.company'].search([])[0].name
        tax_code = self.env['custom.accounting.current.company'].search([])[0].vat

        if len(vat_none) == 0 and len(vat_0) == 0 and len(vat_5) == 0 and len(vat_10) == 0:
            data = {
                'field_21': 'X',
                'field_26': 0,
                'field_27': 0,
                'field_28': 0,
                'field_29': 0,
                'field_30': 0,
                'field_31': 0,
                'field_32': 0,
                'field_32a': 0,
                'field_33': 0,
                'field_34': 0,
                'field_35': 0,
                'field_36': 0
            }
        else:
            vat_none_subtotal = sum([i.price_subtotal for i in vat_none])
            vat_0_subtotal = sum([i.price_subtotal for i in vat_0])

            vat_5_subtotal = sum([i.price_subtotal for i in vat_5])
            vat_5_tax = sum([i.tax for i in vat_5])

            vat_10_subtotal = sum([i.price_subtotal for i in vat_10])
            vat_10_tax = sum([i.tax for i in vat_10])

            # modify hard-coded value with queried data above
            data = {
                'field_21': '',
                'field_22': 0,
                'field_26': vat_none_subtotal,
                'field_29': vat_0_subtotal,
                'field_30': vat_5_subtotal,
                'field_31': vat_5_tax,
                'field_32': vat_10_subtotal,
                'field_32a': 0,
                'field_33': vat_10_tax,
                'field_37': 0,
                'field_38': 0,
                'field_39a': 0,
                'field_40b': 0
            }
            data['field_27'] = data['field_29'] + data['field_30'] + data['field_32'] + data['field_32a']
            data['field_28'] = data['field_31'] + data['field_33']
            data['field_34'] = data['field_26'] + data['field_27']
            data['field_35'] = data['field_28']
            data['field_36'] = data['field_35']
            
            # calculate to fill field_40a & 40b or field_41
            field_40_value = data['field_36'] - data['field_22'] + data['field_37'] - data['field_38'] - data['field_39a']
            if field_40_value >= 0:
                data['field_40a'] = field_40_value
                data['field_40'] = field_40_value - data['field_40b']
                data['field_41'] = 0
            else:
                data['field_40a'] = 0
                data['field_40'] = 0
                data['field_41'] = field_40_value

            data['date'] = datetime.now().day
            data['month'] = datetime.now().month
            data['year'] = datetime.now().year

            data['company_name'] = company_name

            data['tax_code_0'] = tax_code[0]
            data['tax_code_1'] = tax_code[1]
            data['tax_code_2'] = tax_code[2]
            data['tax_code_3'] = tax_code[3]
            data['tax_code_4'] = tax_code[4]
            data['tax_code_5'] = tax_code[5]
            data['tax_code_6'] = tax_code[6]
            data['tax_code_7'] = tax_code[7]
            data['tax_code_8'] = tax_code[8]
            data['tax_code_9'] = tax_code[9]

            data['report_year'] = self.start_date.year
            data['report_quarter'] = math.ceil(self.start_date.month / 3)

        return self.env.ref('custom_accounting.action_custom_report_sale_order').report_action(self, data=data)
