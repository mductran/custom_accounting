# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'BDOOP Accounting',
    'version': '1.0.0',
    'category': '',
    'author': 'Duc',
    'sequence': -1,
    'summary': 'THis is a new custom accounting',
    'description': """THis is a new custome accounting app for bdoop""",
    'website': '',
    'depends': ["mail", "sale", "board"],
    'data': [
        'security/ir.model.access.csv',
        
        'view/menu.xml',

        'view/orders.xml',
        'view/dashboard.xml',
        'view/customers.xml',
        'view/calendar.xml',
        
        'wizards/print_pdf.xml',

        'report/sale_order_report.xml',
    ],
    'xmlDependencies': ['/tabla_stock_notification/static/src/xml/status_templates.xml'],
    'demo': [],
    'application': True,
    'installable': True,
    'assets': {},
    'license': 'LGPL-3',
}
