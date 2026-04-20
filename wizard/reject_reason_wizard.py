from odoo import models, fields, _


class SaleApprovalRejectWizard(models.TransientModel):
    _name = 'sale.approval.reject.wizard'
    _description = 'Sales Approval Rejection Reason'

    order_id = fields.Many2one(
        'sale.order',
        string='Sales Order',
        required=True,
    )

    reason = fields.Text(
        string='Rejection Reason',
        required=True,
    )

    def action_confirm_reject(self):
        self.order_id.approval_state = 'rejected'
        self.order_id.rejection_reason = self.reason
        template = self.env.ref(
            'sales_approval_workflow.mail_template_approval_rejected',
            raise_if_not_found=False
        )
        if template:
            template.send_mail(self.order_id.id, force_send=True)
        self.order_id.message_post(
            body=_('Order rejected by %s. Reason: %s') % (
                self.env.user.name, self.reason
            ),
            subtype_xmlid='mail.mt_note',
        )
        return {'type': 'ir.actions.act_window_close'}
