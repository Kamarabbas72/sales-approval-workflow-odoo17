{
    'name': 'Sales Order Approval Workflow',
    'version': '17.0.1.0.0',
    'summary': 'Adds manager approval workflow for sales orders above a configured amount',
    'author': 'Kamarabbas Bukhari',
    'category': 'Sales',
    'depends': ['sale_management', 'mail'],
    'data': [
        'security/security.xml',
        'wizard/reject_reason_wizard_view.xml',
        'security/ir.model.access.csv',
        'data/mail_template.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
