from odoo import models, fields, api
from odoo import tools


class CurrentCompany(models.Model):
    _name = "custom.accounting.current.company"
    _auto = False
    _description = "Name and tax code of current company"

    name = fields.Text(string="name")
    vat = fields.Text(string="vat")

    def init(self):
        self._cr.execute("""
        CREATE OR REPLACE VIEW custom_accounting_current_company AS 

            SELECT ROW_NUMBER() OVER () AS ID,
                    RC.NAME AS NAME,
                    RP.VAT AS VAT
                    FROM RES_COMPANY RC JOIN RES_PARTNER RP ON RC.NAME = RP.NAME

        """)
