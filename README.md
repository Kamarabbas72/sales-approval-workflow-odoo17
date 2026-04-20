# Sales Order Approval Workflow — Odoo 17

A custom Odoo 17 addon that adds a manager approval workflow to sales orders above a configurable amount threshold. Prevents sales orders from being confirmed without proper authorization.

![Odoo Version](https://img.shields.io/badge/Odoo-17.0-blue)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-LGPL--3-green)
![Category](https://img.shields.io/badge/Category-Sales-orange)

---

## Features

### Automatic Approval Detection
Sales orders are automatically flagged for approval when the total amount exceeds the configured threshold (default: ₹10,000). The `require_approval` field is computed and stored via `@api.depends` on `amount_total`.

### Approval Status Workflow
Four-stage approval status tracked on every sales order:

| Status | Description |
|--------|-------------|
| No Approval Required | Order is below threshold — can be confirmed directly |
| Waiting for Approval | Approval requested, pending manager action |
| Approved | Manager approved — order can now be confirmed |
| Rejected | Manager rejected — salesperson must revise |

### Role-Based Button Visibility
- **Salesperson** sees: `Request Approval` button when order requires approval
- **Sales Approval Manager** sees: `Approve` and `Reject` buttons when order is waiting

### Rejection Reason Wizard
When a manager clicks Reject, a popup wizard captures the rejection reason which is stored on the order and visible to the salesperson.

### Email Notifications
Automated emails sent at each workflow stage:
- Manager notified when approval is requested
- Salesperson notified when order is approved
- Salesperson notified when order is rejected (with reason)

### Chatter Logging
Every workflow action (request, approve, reject) is logged in the order chatter with the user name and timestamp — full audit trail.

### Confirm Protection
The standard `Confirm` button is blocked for orders requiring approval that haven't been approved yet. Attempting to confirm raises a clear `UserError`.

---

## Module Structure

```
sales_approval_workflow/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── sale_order.py              # Extends sale.order — approval fields + workflow methods
│   └── res_config_settings.py     # Extends res.config.settings — approval threshold
├── wizard/
│   ├── __init__.py
│   ├── reject_reason_wizard.py    # TransientModel — captures rejection reason
│   └── reject_reason_wizard_view.xml
├── views/
│   └── sale_order_views.xml       # Inherits sale.order form + list views
├── data/
│   └── mail_template.xml          # 3 email templates (request, approved, rejected)
└── security/
    ├── security.xml               # Sales Approval Manager group definition
    └── ir.model.access.csv        # Access rights for wizard model
```

---

## Technical Highlights

- `_inherit` on `sale.order` — non-destructive extension of core Sales module
- `@api.depends('amount_total')` computed field with `store=True`
- `super().action_confirm()` override with business rule validation
- `TransientModel` wizard for rejection reason capture
- `mail.template` records for three separate email notification scenarios
- `res.groups` definition for role-based button access control
- View inheritance using `xpath` on Odoo 17 sale order form and list views
- Full chatter integration via `message_post()`

---

## Installation

1. Clone this repository into your Odoo custom addons directory:
   ```bash
   git clone https://github.com/Kamarabbas72/sales-approval-workflow-odoo17.git
   ```

2. Add the path to your `odoo.conf`:
   ```ini
   addons_path = /path/to/odoo/addons,/path/to/your/custom/addons
   ```

3. Restart Odoo and install the module:
   ```bash
   python odoo-bin -c odoo.conf -u sales_approval_workflow -d your_database
   ```

4. Go to **Apps** → search `Sales Order Approval Workflow` → **Install**

5. Assign the **Sales Approval Manager** role to users who should approve orders:
   **Settings** → **Users** → select user → tick **Sales Approval Manager**

---

## How It Works

1. Salesperson creates a quotation with total above the threshold
2. `Request Approval` button appears — salesperson clicks it
3. Status changes to **Waiting for Approval**, manager receives email notification
4. Manager opens the order and sees **Approve** / **Reject** buttons
5. If **Approved** → salesperson is notified, order can now be confirmed
6. If **Rejected** → manager enters reason in popup, salesperson is notified with reason

---

## Requirements

- Odoo 17.0
- Python 3.10+
- Depends on: `sale_management`, `mail`

---

## Roadmap

- [ ] Configurable approval threshold via Settings UI
- [ ] Multi-level approval (e.g. manager → director for very large orders)
- [ ] Approval deadline with automatic escalation
- [ ] Dashboard showing pending approvals by salesperson

---

## Author

**Kamarabbas Bukhari** — Odoo ERP Developer

- GitHub: [github.com/Kamarabbas72](https://github.com/Kamarabbas72)
- LinkedIn: [linkedin.com/in/kamarabbas-bukhari-2522981b1](https://linkedin.com/in/kamarabbas-bukhari-2522981b1)
- Email: fardeenbukhari313@gmail.com
