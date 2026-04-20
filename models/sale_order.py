from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    approval_state = fields.Selection([
        ('not_required', 'No Approval Required'),
        ('waiting',      'Waiting for Approval'),
        ('approved',     'Approved'),
        ('rejected',     'Rejected'),
    ], string='Approval Status',
       default='not_required',
       tracking=True,
       copy=False)

    rejection_reason = fields.Text(
        string='Rejection Reason',
        readonly=True,
        copy=False,
    )

    approved_by = fields.Many2one(
        'res.users',
        string='Approved By',
        readonly=True,
        copy=False,
    )

    approved_date = fields.Datetime(
        string='Approved On',
        readonly=True,
        copy=False,
    )

    require_approval = fields.Boolean(
        string='Requires Approval',
        compute='_compute_require_approval',
        store=True,
    )

    @api.depends('amount_total')
    def _compute_require_approval(self):
        min_amount = float(self.env['ir.config_parameter'].sudo().get_param(
            'sales_approval_workflow.approval_min_amount', default=10000
        ))
        for order in self:
            order.require_approval = order.amount_total >= min_amount

    def action_request_approval(self):
        for order in self:
            if not order.require_approval:
                raise UserError(_('This order does not require approval.'))
            order.approval_state = 'waiting'
            template = self.env.ref(
                'sales_approval_workflow.mail_template_approval_request',
                raise_if_not_found=False
            )
            if template:
                template.send_mail(order.id, force_send=True)
            order.message_post(
                body=_('Approval requested by %s.') % self.env.user.name,
                subtype_xmlid='mail.mt_note',
            )
        return True

    def action_approve(self):
        for order in self:
            order.approval_state = 'approved'
            order.approved_by = self.env.user
            order.approved_date = fields.Datetime.now()
            template = self.env.ref(
                'sales_approval_workflow.mail_template_approval_approved',
                raise_if_not_found=False
            )
            if template:
                template.send_mail(order.id, force_send=True)
            order.message_post(
                body=_('Order approved by %s.') % self.env.user.name,
                subtype_xmlid='mail.mt_note',
            )
        return True

    def action_reject(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Rejection Reason',
            'res_model': 'sale.approval.reject.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_order_id': self.id},
        }

    def action_reset_to_draft(self):
        for order in self:
            order.approval_state = 'not_required'
            order.rejection_reason = False
            order.approved_by = False
            order.approved_date = False
        return True

    def action_confirm(self):
        for order in self:
            if order.require_approval and order.approval_state not in ('approved',):
                raise UserError(_(
                    'Order "%s" requires manager approval before confirmation. '
                    'Please request approval first.'
                ) % order.name)
        return super().action_confirm()
