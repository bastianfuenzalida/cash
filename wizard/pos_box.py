# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api
from odoo.addons.account.wizard.pos_box import CashBox


class Pos_Box(CashBox):
    _register = False

    @api.multi
    def run_from_ui(self, values):
        active_model = 'pos.session'
        active_ids = values['session_id']
        reason = values['reason']
        amount = values['amount']
        context = {'active_model': active_model, 'active_ids': active_ids}

        if reason and amount:
            self = self.create({'name': reason, 'amount': amount})
            for session in self.env[active_model].browse(active_ids):
                if session.cash_register_id:
                    print session.cash_register_id
            bank_statements = [session.cash_register_id for session in
                               self.env[active_model].browse(active_ids)
                               if session.cash_register_id]
            if not bank_statements:
                return ("There is no cash register for this PoS Session")
            self.with_context(context)._run(bank_statements)
            return
        else:
            return ("Reason and Amount is Required Fields ")


class Pos_BoxIn(Pos_Box):
    _inherit = 'cash.box.in'


class PosBoxOut(Pos_Box):
    _inherit = 'cash.box.out'

