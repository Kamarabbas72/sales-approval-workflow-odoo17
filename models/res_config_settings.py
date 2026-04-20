from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    approval_min_amount = fields.Float(
        string='Minimum Amount for Approval',
        config_parameter='sales_approval_workflow.approval_min_amount',
        default=10000,
    )
