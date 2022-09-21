from odoo import models, fields, api
from odoo import tools


class SaleTaxReport(models.Model):
    _name = "custom.accounting.tax.report"
    _auto = False
    _description = "Sale Order Line joined with Sale and some other tables view"

    move_name = fields.Text(string="Invoice")
    create_date = fields.Date(string="Create Date")
    customer = fields.Text(string="Customer")
    product = fields.Text(string="Product")
    quotation = fields.Text(string="Quotation")
    price_subtotal = fields.Float(string="Price Subtotal")
    price_total = fields.Float(string="Price Total")
    tax = fields.Float(string="Tax")
    tax_name = fields.Text(string="Tax Name")


    def init(self):
        self._cr.execute("""
        CREATE OR REPLACE VIEW custom_accounting_tax_report AS 

SELECT ROW_NUMBER() OVER () AS ID,
	L.MOVE_NAME,
	L.DATE AS CREATE_DATE,
	L.NAME AS PRODUCT,
	S.NAME AS QUOTATION,
	P.NAME AS CUSTOMER,
	S.STATE AS STATUS,
	CASE
					WHEN rate.rate is NULL THEN L.PRICE_SUBTOTAL
					ELSE ROUND(L.PRICE_SUBTOTAL / RATE.RATE)
	END AS PRICE_SUBTOTAL,
	CASE 
					WHEN rate.rate is NULL THEN L.PRICE_TOTAL
					ELSE ROUND(L.PRICE_TOTAL / RATE.RATE)
	END AS PRICE_TOTAL,
	(L.PRICE_TOTAL - L.PRICE_SUBTOTAL) AS TAX,
	TAX.NAME AS TAX_NAME
FROM ACCOUNT_MOVE_LINE L
INNER JOIN ACCOUNT_MOVE_LINE_ACCOUNT_TAX_REL REL ON REL.ACCOUNT_MOVE_LINE_ID = L.ID
INNER JOIN ACCOUNT_TAX TAX ON TAX.ID = REL.ACCOUNT_TAX_ID
INNER JOIN SALE_ORDER_LINE_INVOICE_REL ORDER_REL ON ORDER_REL.INVOICE_LINE_ID = L.ID
INNER JOIN SALE_ORDER_LINE ON ORDER_REL.ORDER_LINE_ID = SALE_ORDER_LINE.ID
INNER JOIN SALE_ORDER S ON S.ID = SALE_ORDER_LINE.ORDER_ID
INNER JOIN RES_PARTNER P ON P.ID = S.PARTNER_ID
LEFT JOIN (SELECT DISTINCT ON (CURRENCY_ID) * FROM (select * from RES_CURRENCY_RATE order by name desc) as conversion_rate) RATE ON RATE.CURRENCY_ID = L.CURRENCY_ID
        """)
