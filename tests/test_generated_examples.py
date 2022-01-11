from __future__ import absolute_import, division, print_function
import t99


class TestGeneratedExamples(object):
    def test_customer_list(self, request_mock):
        t99.Customer.list(limit=3)
        request_mock.assert_requested("get", "/v1/customers")

    def test_balancetransaction_retrieve(self, request_mock):
        t99.BalanceTransaction.retrieve("txn_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "get",
            "/v1/balance_transactions/txn_xxxxxxxxxxxxx",
        )

    def test_balancetransaction_list(self, request_mock):
        t99.BalanceTransaction.list(limit=3)
        request_mock.assert_requested("get", "/v1/balance_transactions")

    def test_charge_create(self, request_mock):
        t99.Charge.create(
            amount=2000,
            currency="usd",
            source="tok_xxxx",
            description="My First Test Charge (created for API docs)",
        )
        request_mock.assert_requested("post", "/v1/charges")

    def test_charge_retrieve(self, request_mock):
        t99.Charge.retrieve("ch_xxxxxxxxxxxxx")
        request_mock.assert_requested("get", "/v1/charges/ch_xxxxxxxxxxxxx")

    def test_charge_update(self, request_mock):
        t99.Charge.modify("ch_xxxxxxxxxxxxx", metadata={"order_id": "6735"})
        request_mock.assert_requested("post", "/v1/charges/ch_xxxxxxxxxxxxx")

    def test_charge_capture(self, request_mock):
        t99.Charge.capture("ch_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "post",
            "/v1/charges/ch_xxxxxxxxxxxxx/capture",
        )

    def test_charge_list(self, request_mock):
        t99.Charge.list(limit=3)
        request_mock.assert_requested("get", "/v1/charges")

    def test_customer_create(self, request_mock):
        t99.Customer.create(
            description="My First Test Customer (created for API docs)",
        )
        request_mock.assert_requested("post", "/v1/customers")

    def test_customer_retrieve(self, request_mock):
        t99.Customer.retrieve("cus_xxxxxxxxxxxxx")
        request_mock.assert_requested("get", "/v1/customers/cus_xxxxxxxxxxxxx")

    def test_customer_update(self, request_mock):
        t99.Customer.modify(
            "cus_xxxxxxxxxxxxx", metadata={"order_id": "6735"}
        )
        request_mock.assert_requested(
            "post", "/v1/customers/cus_xxxxxxxxxxxxx"
        )

    def test_customer_delete(self, request_mock):
        t99.Customer.delete("cus_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "delete", "/v1/customers/cus_xxxxxxxxxxxxx"
        )

    def test_customer_list2(self, request_mock):
        t99.Customer.list(limit=3)
        request_mock.assert_requested("get", "/v1/customers")

    def test_dispute_retrieve(self, request_mock):
        t99.Dispute.retrieve("dp_xxxxxxxxxxxxx")
        request_mock.assert_requested("get", "/v1/disputes/dp_xxxxxxxxxxxxx")

    def test_dispute_update(self, request_mock):
        t99.Dispute.modify(
            "dp_xxxxxxxxxxxxx", metadata={"order_id": "6735"}
        )
        request_mock.assert_requested("post", "/v1/disputes/dp_xxxxxxxxxxxxx")

    def test_dispute_close(self, request_mock):
        t99.Dispute.close("dp_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "post", "/v1/disputes/dp_xxxxxxxxxxxxx/close"
        )

    def test_dispute_list(self, request_mock):
        t99.Dispute.list(limit=3)
        request_mock.assert_requested("get", "/v1/disputes")

    def test_event_retrieve(self, request_mock):
        t99.Event.retrieve("evt_xxxxxxxxxxxxx")
        request_mock.assert_requested("get", "/v1/events/evt_xxxxxxxxxxxxx")

    def test_event_list(self, request_mock):
        t99.Event.list(limit=3)
        request_mock.assert_requested("get", "/v1/events")

    def test_file_retrieve(self, request_mock):
        t99.File.retrieve("file_xxxxxxxxxxxxx")
        request_mock.assert_requested("get", "/v1/files/file_xxxxxxxxxxxxx")

    def test_file_list(self, request_mock):
        t99.File.list(limit=3)
        request_mock.assert_requested("get", "/v1/files")

    def test_filelink_create(self, request_mock):
        t99.FileLink.create(file="file_xxxxxxxxxxxxx")
        request_mock.assert_requested("post", "/v1/file_links")

    def test_filelink_retrieve(self, request_mock):
        t99.FileLink.retrieve("link_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "get", "/v1/file_links/link_xxxxxxxxxxxxx"
        )

    def test_filelink_update(self, request_mock):
        t99.FileLink.modify(
            "link_xxxxxxxxxxxxx",
            metadata={"order_id": "6735"},
        )
        request_mock.assert_requested(
            "post", "/v1/file_links/link_xxxxxxxxxxxxx"
        )

    def test_filelink_list(self, request_mock):
        t99.FileLink.list(limit=3)
        request_mock.assert_requested("get", "/v1/file_links")

    def test_mandate_retrieve(self, request_mock):
        t99.Mandate.retrieve("mandate_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "get", "/v1/mandates/mandate_xxxxxxxxxxxxx"
        )

    def test_paymentintent_create(self, request_mock):
        t99.PaymentIntent.create(
            amount=2000,
            currency="usd",
            payment_method_types=["card"],
        )
        request_mock.assert_requested("post", "/v1/payment_intents")

    def test_paymentintent_retrieve(self, request_mock):
        t99.PaymentIntent.retrieve("pi_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "get", "/v1/payment_intents/pi_xxxxxxxxxxxxx"
        )

    def test_paymentintent_update(self, request_mock):
        t99.PaymentIntent.modify(
            "pi_xxxxxxxxxxxxx",
            metadata={"order_id": "6735"},
        )
        request_mock.assert_requested(
            "post",
            "/v1/payment_intents/pi_xxxxxxxxxxxxx",
        )

    def test_paymentintent_confirm(self, request_mock):
        t99.PaymentIntent.confirm(
            "pi_xxxxxxxxxxxxx",
            payment_method="pm_card_visa",
        )
        request_mock.assert_requested(
            "post",
            "/v1/payment_intents/pi_xxxxxxxxxxxxx/confirm",
        )

    def test_paymentintent_capture(self, request_mock):
        t99.PaymentIntent.capture("pi_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "post",
            "/v1/payment_intents/pi_xxxxxxxxxxxxx/capture",
        )

    def test_paymentintent_cancel(self, request_mock):
        t99.PaymentIntent.cancel("pi_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "post",
            "/v1/payment_intents/pi_xxxxxxxxxxxxx/cancel",
        )

    def test_paymentintent_list(self, request_mock):
        t99.PaymentIntent.list(limit=3)
        request_mock.assert_requested("get", "/v1/payment_intents")

    def test_setupintent_create(self, request_mock):
        t99.SetupIntent.create(payment_method_types=["card"])
        request_mock.assert_requested("post", "/v1/setup_intents")

    def test_setupintent_retrieve(self, request_mock):
        t99.SetupIntent.retrieve("seti_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "get", "/v1/setup_intents/seti_xxxxxxxxxxxxx"
        )

    def test_setupintent_update(self, request_mock):
        t99.SetupIntent.modify(
            "seti_xxxxxxxxxxxxx",
            metadata={"user_id": "3435453"},
        )
        request_mock.assert_requested(
            "post",
            "/v1/setup_intents/seti_xxxxxxxxxxxxx",
        )

    def test_setupintent_confirm(self, request_mock):
        t99.SetupIntent.confirm(
            "seti_xxxxxxxxxxxxx",
            payment_method="pm_card_visa",
        )
        request_mock.assert_requested(
            "post",
            "/v1/setup_intents/seti_xxxxxxxxxxxxx/confirm",
        )

    def test_setupintent_cancel(self, request_mock):
        t99.SetupIntent.cancel("seti_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "post",
            "/v1/setup_intents/seti_xxxxxxxxxxxxx/cancel",
        )

    def test_setupintent_list(self, request_mock):
        t99.SetupIntent.list(limit=3)
        request_mock.assert_requested("get", "/v1/setup_intents")

    def test_setupattempt_list(self, request_mock):
        t99.SetupAttempt.list(setup_intent="seti_xxxxxxxxxxxxx", limit=3)
        request_mock.assert_requested("get", "/v1/setup_attempts")

    def test_payout_create(self, request_mock):
        t99.Payout.create(amount=1100, currency="usd")
        request_mock.assert_requested("post", "/v1/payouts")

    def test_payout_retrieve(self, request_mock):
        t99.Payout.retrieve("po_xxxxxxxxxxxxx")
        request_mock.assert_requested("get", "/v1/payouts/po_xxxxxxxxxxxxx")

    def test_payout_update(self, request_mock):
        t99.Payout.modify("po_xxxxxxxxxxxxx", metadata={"order_id": "6735"})
        request_mock.assert_requested("post", "/v1/payouts/po_xxxxxxxxxxxxx")

    def test_payout_list(self, request_mock):
        t99.Payout.list(limit=3)
        request_mock.assert_requested("get", "/v1/payouts")

    def test_payout_cancel(self, request_mock):
        t99.Payout.cancel("po_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "post", "/v1/payouts/po_xxxxxxxxxxxxx/cancel"
        )

    def test_payout_reverse(self, request_mock):
        t99.Payout.reverse("po_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "post",
            "/v1/payouts/po_xxxxxxxxxxxxx/reverse",
        )

    def test_product_create(self, request_mock):
        t99.Product.create(name="Gold Special")
        request_mock.assert_requested("post", "/v1/products")

    def test_product_retrieve(self, request_mock):
        t99.Product.retrieve("prod_xxxxxxxxxxxxx")
        request_mock.assert_requested("get", "/v1/products/prod_xxxxxxxxxxxxx")

    def test_product_update(self, request_mock):
        t99.Product.modify(
            "prod_xxxxxxxxxxxxx", metadata={"order_id": "6735"}
        )
        request_mock.assert_requested(
            "post", "/v1/products/prod_xxxxxxxxxxxxx"
        )

    def test_product_list(self, request_mock):
        t99.Product.list(limit=3)
        request_mock.assert_requested("get", "/v1/products")

    def test_product_delete(self, request_mock):
        t99.Product.delete("prod_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "delete", "/v1/products/prod_xxxxxxxxxxxxx"
        )

    def test_price_create(self, request_mock):
        t99.Price.create(
            unit_amount=2000,
            currency="usd",
            recurring={"interval": "month"},
            product="prod_xxxxxxxxxxxxx",
        )
        request_mock.assert_requested("post", "/v1/prices")

    def test_price_retrieve(self, request_mock):
        t99.Price.retrieve("price_xxxxxxxxxxxxx")
        request_mock.assert_requested("get", "/v1/prices/price_xxxxxxxxxxxxx")

    def test_price_update(self, request_mock):
        t99.Price.modify(
            "price_xxxxxxxxxxxxx", metadata={"order_id": "6735"}
        )
        request_mock.assert_requested("post", "/v1/prices/price_xxxxxxxxxxxxx")

    def test_price_list(self, request_mock):
        t99.Price.list(limit=3)
        request_mock.assert_requested("get", "/v1/prices")

    def test_refund_create(self, request_mock):
        t99.Refund.create(charge="ch_xxxxxxxxxxxxx")
        request_mock.assert_requested("post", "/v1/refunds")

    def test_refund_retrieve(self, request_mock):
        t99.Refund.retrieve("re_xxxxxxxxxxxxx")
        request_mock.assert_requested("get", "/v1/refunds/re_xxxxxxxxxxxxx")

    def test_refund_update(self, request_mock):
        t99.Refund.modify("re_xxxxxxxxxxxxx", metadata={"order_id": "6735"})
        request_mock.assert_requested("post", "/v1/refunds/re_xxxxxxxxxxxxx")

    def test_refund_list(self, request_mock):
        t99.Refund.list(limit=3)
        request_mock.assert_requested("get", "/v1/refunds")

    def test_token_create(self, request_mock):
        t99.Token.create(
            card={
                "number": "4242424242424242",
                "exp_month": "5",
                "exp_year": "2022",
                "cvc": "314",
            },
        )
        request_mock.assert_requested("post", "/v1/tokens")

    def test_token_create2(self, request_mock):
        t99.Token.create(
            bank_account={
                "country": "US",
                "currency": "usd",
                "account_holder_name": "Jenny Rosen",
                "account_holder_type": "individual",
                "routing_number": "110000000",
                "account_number": "000123456789",
            },
        )
        request_mock.assert_requested("post", "/v1/tokens")

    def test_token_create3(self, request_mock):
        t99.Token.create(pii={"id_number": "000000000"})
        request_mock.assert_requested("post", "/v1/tokens")

    def test_token_create4(self, request_mock):
        t99.Token.create(
            account={
                "individual": {"first_name": "Jane", "last_name": "Doe"},
                "tos_shown_and_accepted": True,
            },
        )
        request_mock.assert_requested("post", "/v1/tokens")

    def test_token_create5(self, request_mock):
        t99.Token.create(
            person={
                "first_name": "Jane",
                "last_name": "Doe",
                "relationship": {"owner": True},
            },
        )
        request_mock.assert_requested("post", "/v1/tokens")

    def test_token_create6(self, request_mock):
        t99.Token.create(cvc_update={"cvc": "123"})
        request_mock.assert_requested("post", "/v1/tokens")

    def test_token_retrieve(self, request_mock):
        t99.Token.retrieve("tok_xxxx")
        request_mock.assert_requested("get", "/v1/tokens/tok_xxxx")

    def test_paymentmethod_create(self, request_mock):
        t99.PaymentMethod.create(
            type="card",
            card={
                "number": "4242424242424242",
                "exp_month": 5,
                "exp_year": 2022,
                "cvc": "314",
            },
        )
        request_mock.assert_requested("post", "/v1/payment_methods")

    def test_paymentmethod_retrieve(self, request_mock):
        t99.PaymentMethod.retrieve("pm_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "get", "/v1/payment_methods/pm_xxxxxxxxxxxxx"
        )

    def test_paymentmethod_update(self, request_mock):
        t99.PaymentMethod.modify(
            "pm_xxxxxxxxxxxxx",
            metadata={"order_id": "6735"},
        )
        request_mock.assert_requested(
            "post",
            "/v1/payment_methods/pm_xxxxxxxxxxxxx",
        )

    def test_paymentmethod_list(self, request_mock):
        t99.PaymentMethod.list(customer="cus_xxxxxxxxxxxxx", type="card")
        request_mock.assert_requested("get", "/v1/payment_methods")

    def test_paymentmethod_attach(self, request_mock):
        t99.PaymentMethod.attach(
            "pm_xxxxxxxxxxxxx",
            customer="cus_xxxxxxxxxxxxx",
        )
        request_mock.assert_requested(
            "post",
            "/v1/payment_methods/pm_xxxxxxxxxxxxx/attach",
        )

    def test_paymentmethod_detach(self, request_mock):
        t99.PaymentMethod.detach("pm_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "post",
            "/v1/payment_methods/pm_xxxxxxxxxxxxx/detach",
        )

    def test_source_retrieve(self, request_mock):
        t99.Source.retrieve("src_xxxxxxxxxxxxx")
        request_mock.assert_requested("get", "/v1/sources/src_xxxxxxxxxxxxx")

    def test_source_update(self, request_mock):
        t99.Source.modify(
            "src_xxxxxxxxxxxxx", metadata={"order_id": "6735"}
        )
        request_mock.assert_requested("post", "/v1/sources/src_xxxxxxxxxxxxx")

    def test_checkout_session_create(self, request_mock):
        t99.checkout.Session.create(
            success_url="https://example.com/success",
            cancel_url="https://example.com/cancel",
            payment_method_types=["card"],
            line_items=[{"price": "price_xxxxxxxxxxxxx", "quantity": 2}],
            mode="payment",
        )
        request_mock.assert_requested("post", "/v1/checkout/sessions")

    def test_checkout_session_retrieve(self, request_mock):
        t99.checkout.Session.retrieve("cs_test_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "get",
            "/v1/checkout/sessions/cs_test_xxxxxxxxxxxxx",
        )

    def test_checkout_session_list(self, request_mock):
        t99.checkout.Session.list(limit=3)
        request_mock.assert_requested("get", "/v1/checkout/sessions")

    def test_coupon_create(self, request_mock):
        t99.Coupon.create(
            percent_off=25,
            duration="repeating",
            duration_in_months=3,
        )
        request_mock.assert_requested("post", "/v1/coupons")

    def test_coupon_retrieve(self, request_mock):
        t99.Coupon.retrieve("25_5OFF")
        request_mock.assert_requested("get", "/v1/coupons/25_5OFF")

    def test_coupon_update(self, request_mock):
        t99.Coupon.modify("co_xxxxxxxxxxxxx", metadata={"order_id": "6735"})
        request_mock.assert_requested("post", "/v1/coupons/co_xxxxxxxxxxxxx")

    def test_coupon_delete(self, request_mock):
        t99.Coupon.delete("co_xxxxxxxxxxxxx")
        request_mock.assert_requested("delete", "/v1/coupons/co_xxxxxxxxxxxxx")

    def test_coupon_list(self, request_mock):
        t99.Coupon.list(limit=3)
        request_mock.assert_requested("get", "/v1/coupons")

    def test_creditnote_create(self, request_mock):
        t99.CreditNote.create(
            invoice="in_xxxxxxxxxxxxx",
            lines=[
                {
                    "type": "invoice_line_item",
                    "invoice_line_item": "il_xxxxxxxxxxxxx",
                    "quantity": 1,
                },
            ],
        )
        request_mock.assert_requested("post", "/v1/credit_notes")

    def test_creditnote_update(self, request_mock):
        t99.CreditNote.modify(
            "cn_xxxxxxxxxxxxx",
            metadata={"order_id": "6735"},
        )
        request_mock.assert_requested(
            "post", "/v1/credit_notes/cn_xxxxxxxxxxxxx"
        )

    def test_creditnote_void_credit_note(self, request_mock):
        t99.CreditNote.void_credit_note("cn_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "post",
            "/v1/credit_notes/cn_xxxxxxxxxxxxx/void",
        )

    def test_creditnote_list(self, request_mock):
        t99.CreditNote.list(limit=3)
        request_mock.assert_requested("get", "/v1/credit_notes")

    def test_customer_customerbalancetransaction_retrieve(self, request_mock):
        t99.Customer.retrieve_balance_transaction(
            "cus_xxxxxxxxxxxxx",
            "cbtxn_xxxxxxxxxxxxx",
        )
        request_mock.assert_requested(
            "get",
            "/v1/customers/cus_xxxxxxxxxxxxx/balance_transactions/cbtxn_xxxxxxxxxxxxx",
        )

    def test_billing_portal_session_create(self, request_mock):
        t99.billing_portal.Session.create(
            customer="cus_xxxxxxxxxxxxx",
            return_url="https://example.com/account",
        )
        request_mock.assert_requested("post", "/v1/billing_portal/sessions")

    def test_billing_portal_configuration_create(self, request_mock):
        t99.billing_portal.Configuration.create(
            features={
                "customer_update": {
                    "allowed_updates": ["email", "tax_id"],
                    "enabled": True,
                },
                "invoice_history": {"enabled": True},
            },
            business_profile={
                "privacy_policy_url": "https://example.com/privacy",
                "terms_of_service_url": "https://example.com/terms",
            },
        )
        request_mock.assert_requested(
            "post", "/v1/billing_portal/configurations"
        )

    def test_billing_portal_configuration_update(self, request_mock):
        t99.billing_portal.Configuration.modify(
            "bpc_xxxxxxxxxxxxx",
            business_profile={
                "privacy_policy_url": "https://example.com/privacy",
                "terms_of_service_url": "https://example.com/terms",
            },
        )
        request_mock.assert_requested(
            "post",
            "/v1/billing_portal/configurations/bpc_xxxxxxxxxxxxx",
        )

    def test_billing_portal_configuration_retrieve(self, request_mock):
        t99.billing_portal.Configuration.retrieve("bpc_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "get",
            "/v1/billing_portal/configurations/bpc_xxxxxxxxxxxxx",
        )

    def test_billing_portal_configuration_list(self, request_mock):
        t99.billing_portal.Configuration.list(limit=3)
        request_mock.assert_requested(
            "get", "/v1/billing_portal/configurations"
        )

    def test_customer_taxid_retrieve(self, request_mock):
        t99.Customer.retrieve_tax_id(
            "cus_xxxxxxxxxxxxx", "txi_xxxxxxxxxxxxx"
        )
        request_mock.assert_requested(
            "get",
            "/v1/customers/cus_xxxxxxxxxxxxx/tax_ids/txi_xxxxxxxxxxxxx",
        )

    def test_invoice_create(self, request_mock):
        t99.Invoice.create(customer="cus_xxxxxxxxxxxxx")
        request_mock.assert_requested("post", "/v1/invoices")

    def test_invoice_retrieve(self, request_mock):
        t99.Invoice.retrieve("in_xxxxxxxxxxxxx")
        request_mock.assert_requested("get", "/v1/invoices/in_xxxxxxxxxxxxx")

    def test_invoice_update(self, request_mock):
        t99.Invoice.modify(
            "in_xxxxxxxxxxxxx", metadata={"order_id": "6735"}
        )
        request_mock.assert_requested("post", "/v1/invoices/in_xxxxxxxxxxxxx")

    def test_invoice_delete(self, request_mock):
        t99.Invoice.delete("in_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "delete", "/v1/invoices/in_xxxxxxxxxxxxx"
        )

    def test_invoice_finalize_invoice(self, request_mock):
        t99.Invoice.finalize_invoice("in_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "post",
            "/v1/invoices/in_xxxxxxxxxxxxx/finalize",
        )

    def test_invoice_pay(self, request_mock):
        t99.Invoice.pay("in_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "post", "/v1/invoices/in_xxxxxxxxxxxxx/pay"
        )

    def test_invoice_send_invoice(self, request_mock):
        t99.Invoice.send_invoice("in_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "post", "/v1/invoices/in_xxxxxxxxxxxxx/send"
        )

    def test_invoice_void_invoice(self, request_mock):
        t99.Invoice.void_invoice("in_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "post", "/v1/invoices/in_xxxxxxxxxxxxx/void"
        )

    def test_invoice_mark_uncollectible(self, request_mock):
        t99.Invoice.mark_uncollectible("in_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "post",
            "/v1/invoices/in_xxxxxxxxxxxxx/mark_uncollectible",
        )

    def test_invoice_list(self, request_mock):
        t99.Invoice.list(limit=3)
        request_mock.assert_requested("get", "/v1/invoices")

    def test_invoiceitem_create(self, request_mock):
        t99.InvoiceItem.create(
            customer="cus_xxxxxxxxxxxxx",
            price="price_xxxxxxxxxxxxx",
        )
        request_mock.assert_requested("post", "/v1/invoiceitems")

    def test_invoiceitem_retrieve(self, request_mock):
        t99.InvoiceItem.retrieve("ii_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "get", "/v1/invoiceitems/ii_xxxxxxxxxxxxx"
        )

    def test_invoiceitem_update(self, request_mock):
        t99.InvoiceItem.modify(
            "ii_xxxxxxxxxxxxx",
            metadata={"order_id": "6735"},
        )
        request_mock.assert_requested(
            "post", "/v1/invoiceitems/ii_xxxxxxxxxxxxx"
        )

    def test_invoiceitem_delete(self, request_mock):
        t99.InvoiceItem.delete("ii_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "delete", "/v1/invoiceitems/ii_xxxxxxxxxxxxx"
        )

    def test_invoiceitem_list(self, request_mock):
        t99.InvoiceItem.list(limit=3)
        request_mock.assert_requested("get", "/v1/invoiceitems")

    def test_plan_create(self, request_mock):
        t99.Plan.create(
            amount=2000,
            currency="usd",
            interval="month",
            product="prod_xxxxxxxxxxxxx",
        )
        request_mock.assert_requested("post", "/v1/plans")

    def test_plan_retrieve(self, request_mock):
        t99.Plan.retrieve("price_xxxxxxxxxxxxx")
        request_mock.assert_requested("get", "/v1/plans/price_xxxxxxxxxxxxx")

    def test_plan_update(self, request_mock):
        t99.Plan.modify(
            "price_xxxxxxxxxxxxx", metadata={"order_id": "6735"}
        )
        request_mock.assert_requested("post", "/v1/plans/price_xxxxxxxxxxxxx")

    def test_plan_delete(self, request_mock):
        t99.Plan.delete("price_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "delete", "/v1/plans/price_xxxxxxxxxxxxx"
        )

    def test_plan_list(self, request_mock):
        t99.Plan.list(limit=3)
        request_mock.assert_requested("get", "/v1/plans")

    def test_promotioncode_create(self, request_mock):
        t99.PromotionCode.create(coupon="25_5OFF")
        request_mock.assert_requested("post", "/v1/promotion_codes")

    def test_promotioncode_update(self, request_mock):
        t99.PromotionCode.modify(
            "promo_xxxxxxxxxxxxx",
            metadata={"order_id": "6735"},
        )
        request_mock.assert_requested(
            "post",
            "/v1/promotion_codes/promo_xxxxxxxxxxxxx",
        )

    def test_promotioncode_retrieve(self, request_mock):
        t99.PromotionCode.retrieve("promo_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "get",
            "/v1/promotion_codes/promo_xxxxxxxxxxxxx",
        )

    def test_promotioncode_list(self, request_mock):
        t99.PromotionCode.list(limit=3)
        request_mock.assert_requested("get", "/v1/promotion_codes")

    def test_subscription_create(self, request_mock):
        t99.Subscription.create(
            customer="cus_xxxxxxxxxxxxx",
            items=[{"price": "price_xxxxxxxxxxxxx"}],
        )
        request_mock.assert_requested("post", "/v1/subscriptions")

    def test_subscription_retrieve(self, request_mock):
        t99.Subscription.retrieve("sub_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "get", "/v1/subscriptions/sub_xxxxxxxxxxxxx"
        )

    def test_subscription_update(self, request_mock):
        t99.Subscription.modify(
            "sub_xxxxxxxxxxxxx",
            metadata={"order_id": "6735"},
        )
        request_mock.assert_requested(
            "post", "/v1/subscriptions/sub_xxxxxxxxxxxxx"
        )

    def test_subscription_list(self, request_mock):
        t99.Subscription.list(limit=3)
        request_mock.assert_requested("get", "/v1/subscriptions")

    def test_subscriptionitem_create(self, request_mock):
        t99.SubscriptionItem.create(
            subscription="sub_xxxxxxxxxxxxx",
            price="price_xxxxxxxxxxxxx",
            quantity=2,
        )
        request_mock.assert_requested("post", "/v1/subscription_items")

    def test_subscriptionitem_retrieve(self, request_mock):
        t99.SubscriptionItem.retrieve("si_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "get",
            "/v1/subscription_items/si_xxxxxxxxxxxxx",
        )

    def test_subscriptionitem_update(self, request_mock):
        t99.SubscriptionItem.modify(
            "si_xxxxxxxxxxxxx",
            metadata={"order_id": "6735"},
        )
        request_mock.assert_requested(
            "post",
            "/v1/subscription_items/si_xxxxxxxxxxxxx",
        )

    def test_subscriptionitem_delete(self, request_mock):
        t99.SubscriptionItem.delete("si_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "delete",
            "/v1/subscription_items/si_xxxxxxxxxxxxx",
        )

    def test_subscriptionitem_list(self, request_mock):
        t99.SubscriptionItem.list(subscription="sub_xxxxxxxxxxxxx")
        request_mock.assert_requested("get", "/v1/subscription_items")

    def test_subscriptionschedule_create(self, request_mock):
        t99.SubscriptionSchedule.create(
            customer="cus_xxxxxxxxxxxxx",
            start_date=1620753115,
            end_behavior="release",
            phases=[
                {
                    "items": [{"price": "price_xxxxxxxxxxxxx", "quantity": 1}],
                    "iterations": 12,
                },
            ],
        )
        request_mock.assert_requested("post", "/v1/subscription_schedules")

    def test_subscriptionschedule_retrieve(self, request_mock):
        t99.SubscriptionSchedule.retrieve("sub_sched_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "get",
            "/v1/subscription_schedules/sub_sched_xxxxxxxxxxxxx",
        )

    def test_subscriptionschedule_update(self, request_mock):
        t99.SubscriptionSchedule.modify(
            "sub_sched_xxxxxxxxxxxxx",
            end_behavior="release",
        )
        request_mock.assert_requested(
            "post",
            "/v1/subscription_schedules/sub_sched_xxxxxxxxxxxxx",
        )

    def test_subscriptionschedule_cancel(self, request_mock):
        t99.SubscriptionSchedule.cancel("sub_sched_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "post",
            "/v1/subscription_schedules/sub_sched_xxxxxxxxxxxxx/cancel",
        )

    def test_subscriptionschedule_release(self, request_mock):
        t99.SubscriptionSchedule.release("sub_sched_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "post",
            "/v1/subscription_schedules/sub_sched_xxxxxxxxxxxxx/release",
        )

    def test_subscriptionschedule_list(self, request_mock):
        t99.SubscriptionSchedule.list(limit=3)
        request_mock.assert_requested("get", "/v1/subscription_schedules")

    def test_taxrate_create(self, request_mock):
        t99.TaxRate.create(
            display_name="VAT",
            description="VAT Germany",
            jurisdiction="DE",
            percentage=16,
            inclusive=False,
        )
        request_mock.assert_requested("post", "/v1/tax_rates")

    def test_taxrate_retrieve(self, request_mock):
        t99.TaxRate.retrieve("txr_xxxxxxxxxxxxx")
        request_mock.assert_requested("get", "/v1/tax_rates/txr_xxxxxxxxxxxxx")

    def test_taxrate_update(self, request_mock):
        t99.TaxRate.modify("txr_xxxxxxxxxxxxx", active=False)
        request_mock.assert_requested(
            "post", "/v1/tax_rates/txr_xxxxxxxxxxxxx"
        )

    def test_taxrate_list(self, request_mock):
        t99.TaxRate.list(limit=3)
        request_mock.assert_requested("get", "/v1/tax_rates")

    def test_account_create(self, request_mock):
        t99.Account.create(
            type="custom",
            country="US",
            email="jenny.rosen@example.com",
            capabilities={
                "card_payments": {"requested": True},
                "transfers": {"requested": True},
            },
        )
        request_mock.assert_requested("post", "/v1/accounts")

    def test_account_retrieve(self, request_mock):
        t99.Account.retrieve("acct_xxxxxxxxxxxxx")
        request_mock.assert_requested("get", "/v1/accounts/acct_xxxxxxxxxxxxx")

    def test_account_update(self, request_mock):
        t99.Account.modify(
            "acct_xxxxxxxxxxxxx", metadata={"order_id": "6735"}
        )
        request_mock.assert_requested(
            "post", "/v1/accounts/acct_xxxxxxxxxxxxx"
        )

    def test_account_delete(self, request_mock):
        t99.Account.delete("acct_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "delete", "/v1/accounts/acct_xxxxxxxxxxxxx"
        )

    def test_account_reject(self, request_mock):
        t99.Account.reject("acct_xxxxxxxxxxxxx", reason="fraud")
        request_mock.assert_requested(
            "post",
            "/v1/accounts/acct_xxxxxxxxxxxxx/reject",
        )

    def test_account_list(self, request_mock):
        t99.Account.list(limit=3)
        request_mock.assert_requested("get", "/v1/accounts")

    def test_accountlink_create(self, request_mock):
        t99.AccountLink.create(
            account="acct_xxxxxxxxxxxxx",
            refresh_url="https://example.com/reauth",
            return_url="https://example.com/return",
            type="account_onboarding",
        )
        request_mock.assert_requested("post", "/v1/account_links")

    def test_applicationfee_retrieve(self, request_mock):
        t99.ApplicationFee.retrieve("fee_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "get",
            "/v1/application_fees/fee_xxxxxxxxxxxxx",
        )

    def test_applicationfee_list(self, request_mock):
        t99.ApplicationFee.list(limit=3)
        request_mock.assert_requested("get", "/v1/application_fees")

    def test_applicationfee_feerefund_retrieve(self, request_mock):
        t99.ApplicationFee.retrieve_refund(
            "fee_xxxxxxxxxxxxx",
            "fr_xxxxxxxxxxxxx",
        )
        request_mock.assert_requested(
            "get",
            "/v1/application_fees/fee_xxxxxxxxxxxxx/refunds/fr_xxxxxxxxxxxxx",
        )

    def test_applicationfee_feerefund_update(self, request_mock):
        t99.ApplicationFee.modify_refund(
            "fee_xxxxxxxxxxxxx",
            "fr_xxxxxxxxxxxxx",
            metadata={"order_id": "6735"},
        )
        request_mock.assert_requested(
            "post",
            "/v1/application_fees/fee_xxxxxxxxxxxxx/refunds/fr_xxxxxxxxxxxxx",
        )

    def test_account_capability_retrieve(self, request_mock):
        t99.Account.retrieve_capability(
            "acct_xxxxxxxxxxxxx", "card_payments"
        )
        request_mock.assert_requested(
            "get",
            "/v1/accounts/acct_xxxxxxxxxxxxx/capabilities/card_payments",
        )

    def test_account_capability_update(self, request_mock):
        t99.Account.modify_capability(
            "acct_xxxxxxxxxxxxx",
            "card_payments",
            requested=True,
        )
        request_mock.assert_requested(
            "post",
            "/v1/accounts/acct_xxxxxxxxxxxxx/capabilities/card_payments",
        )

    def test_countryspec_list(self, request_mock):
        t99.CountrySpec.list(limit=3)
        request_mock.assert_requested("get", "/v1/country_specs")

    def test_countryspec_retrieve(self, request_mock):
        t99.CountrySpec.retrieve("US")
        request_mock.assert_requested("get", "/v1/country_specs/US")

    def test_account_person_retrieve(self, request_mock):
        t99.Account.retrieve_person(
            "acct_xxxxxxxxxxxxx", "person_xxxxxxxxxxxxx"
        )
        request_mock.assert_requested(
            "get",
            "/v1/accounts/acct_xxxxxxxxxxxxx/persons/person_xxxxxxxxxxxxx",
        )

    def test_account_person_update(self, request_mock):
        t99.Account.modify_person(
            "acct_xxxxxxxxxxxxx",
            "person_xxxxxxxxxxxxx",
            metadata={"order_id": "6735"},
        )
        request_mock.assert_requested(
            "post",
            "/v1/accounts/acct_xxxxxxxxxxxxx/persons/person_xxxxxxxxxxxxx",
        )

    def test_topup_create(self, request_mock):
        t99.Topup.create(
            amount=2000,
            currency="usd",
            description="Top-up for Jenny Rosen",
            statement_descriptor="Top-up",
        )
        request_mock.assert_requested("post", "/v1/topups")

    def test_topup_retrieve(self, request_mock):
        t99.Topup.retrieve("tu_xxxxxxxxxxxxx")
        request_mock.assert_requested("get", "/v1/topups/tu_xxxxxxxxxxxxx")

    def test_topup_update(self, request_mock):
        t99.Topup.modify("tu_xxxxxxxxxxxxx", metadata={"order_id": "6735"})
        request_mock.assert_requested("post", "/v1/topups/tu_xxxxxxxxxxxxx")

    def test_topup_list(self, request_mock):
        t99.Topup.list(limit=3)
        request_mock.assert_requested("get", "/v1/topups")

    def test_topup_cancel(self, request_mock):
        t99.Topup.cancel("tu_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "post", "/v1/topups/tu_xxxxxxxxxxxxx/cancel"
        )

    def test_transfer_create(self, request_mock):
        t99.Transfer.create(
            amount=400,
            currency="usd",
            destination="acct_xxxxxxxxxxxxx",
            transfer_group="ORDER_95",
        )
        request_mock.assert_requested("post", "/v1/transfers")

    def test_transfer_retrieve(self, request_mock):
        t99.Transfer.retrieve("tr_xxxxxxxxxxxxx")
        request_mock.assert_requested("get", "/v1/transfers/tr_xxxxxxxxxxxxx")

    def test_transfer_update(self, request_mock):
        t99.Transfer.modify(
            "tr_xxxxxxxxxxxxx", metadata={"order_id": "6735"}
        )
        request_mock.assert_requested("post", "/v1/transfers/tr_xxxxxxxxxxxxx")

    def test_transfer_list(self, request_mock):
        t99.Transfer.list(limit=3)
        request_mock.assert_requested("get", "/v1/transfers")

    def test_transfer_transferreversal_retrieve(self, request_mock):
        t99.Transfer.retrieve_reversal(
            "tr_xxxxxxxxxxxxx", "trr_xxxxxxxxxxxxx"
        )
        request_mock.assert_requested(
            "get",
            "/v1/transfers/tr_xxxxxxxxxxxxx/reversals/trr_xxxxxxxxxxxxx",
        )

    def test_transfer_transferreversal_update(self, request_mock):
        t99.Transfer.modify_reversal(
            "tr_xxxxxxxxxxxxx",
            "trr_xxxxxxxxxxxxx",
            metadata={"order_id": "6735"},
        )
        request_mock.assert_requested(
            "post",
            "/v1/transfers/tr_xxxxxxxxxxxxx/reversals/trr_xxxxxxxxxxxxx",
        )

    def test_radar_earlyfraudwarning_retrieve(self, request_mock):
        t99.radar.EarlyFraudWarning.retrieve("issfr_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "get",
            "/v1/radar/early_fraud_warnings/issfr_xxxxxxxxxxxxx",
        )

    def test_radar_earlyfraudwarning_list(self, request_mock):
        t99.radar.EarlyFraudWarning.list(limit=3)
        request_mock.assert_requested("get", "/v1/radar/early_fraud_warnings")

    def test_review_approve(self, request_mock):
        t99.Review.approve("prv_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "post",
            "/v1/reviews/prv_xxxxxxxxxxxxx/approve",
        )

    def test_review_retrieve(self, request_mock):
        t99.Review.retrieve("prv_xxxxxxxxxxxxx")
        request_mock.assert_requested("get", "/v1/reviews/prv_xxxxxxxxxxxxx")

    def test_review_list(self, request_mock):
        t99.Review.list(limit=3)
        request_mock.assert_requested("get", "/v1/reviews")

    def test_radar_valuelist_create(self, request_mock):
        t99.radar.ValueList.create(
            alias="custom_ip_xxxxxxxxxxxxx",
            name="Custom IP Blocklist",
            item_type="ip_address",
        )
        request_mock.assert_requested("post", "/v1/radar/value_lists")

    def test_radar_valuelist_retrieve(self, request_mock):
        t99.radar.ValueList.retrieve("rsl_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "get",
            "/v1/radar/value_lists/rsl_xxxxxxxxxxxxx",
        )

    def test_radar_valuelist_update(self, request_mock):
        t99.radar.ValueList.modify(
            "rsl_xxxxxxxxxxxxx",
            name="Updated IP Block List",
        )
        request_mock.assert_requested(
            "post",
            "/v1/radar/value_lists/rsl_xxxxxxxxxxxxx",
        )

    def test_radar_valuelist_delete(self, request_mock):
        t99.radar.ValueList.delete("rsl_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "delete",
            "/v1/radar/value_lists/rsl_xxxxxxxxxxxxx",
        )

    def test_radar_valuelist_list(self, request_mock):
        t99.radar.ValueList.list(limit=3)
        request_mock.assert_requested("get", "/v1/radar/value_lists")

    def test_radar_valuelistitem_create(self, request_mock):
        t99.radar.ValueListItem.create(
            value_list="rsl_xxxxxxxxxxxxx",
            value="1.2.3.4",
        )
        request_mock.assert_requested("post", "/v1/radar/value_list_items")

    def test_radar_valuelistitem_retrieve(self, request_mock):
        t99.radar.ValueListItem.retrieve("rsli_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "get",
            "/v1/radar/value_list_items/rsli_xxxxxxxxxxxxx",
        )

    def test_radar_valuelistitem_delete(self, request_mock):
        t99.radar.ValueListItem.delete("rsli_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "delete",
            "/v1/radar/value_list_items/rsli_xxxxxxxxxxxxx",
        )

    def test_radar_valuelistitem_list(self, request_mock):
        t99.radar.ValueListItem.list(
            limit=3, value_list="rsl_xxxxxxxxxxxxx"
        )
        request_mock.assert_requested("get", "/v1/radar/value_list_items")

    def test_issuing_authorization_retrieve(self, request_mock):
        t99.issuing.Authorization.retrieve("iauth_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "get",
            "/v1/issuing/authorizations/iauth_xxxxxxxxxxxxx",
        )

    def test_issuing_authorization_update(self, request_mock):
        t99.issuing.Authorization.modify(
            "iauth_xxxxxxxxxxxxx",
            metadata={"order_id": "6735"},
        )
        request_mock.assert_requested(
            "post",
            "/v1/issuing/authorizations/iauth_xxxxxxxxxxxxx",
        )

    def test_issuing_authorization_approve(self, request_mock):
        t99.issuing.Authorization.approve("iauth_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "post",
            "/v1/issuing/authorizations/iauth_xxxxxxxxxxxxx/approve",
        )

    def test_issuing_authorization_decline(self, request_mock):
        t99.issuing.Authorization.decline("iauth_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "post",
            "/v1/issuing/authorizations/iauth_xxxxxxxxxxxxx/decline",
        )

    def test_issuing_authorization_list(self, request_mock):
        t99.issuing.Authorization.list(limit=3)
        request_mock.assert_requested("get", "/v1/issuing/authorizations")

    def test_issuing_cardholder_create(self, request_mock):
        t99.issuing.Cardholder.create(
            type="individual",
            name="Jenny Rosen",
            email="jenny.rosen@example.com",
            phone_number="+18888675309",
            billing={
                "address": {
                    "line1": "1234 Main Street",
                    "city": "San Francisco",
                    "state": "CA",
                    "country": "US",
                    "postal_code": "94111",
                },
            },
        )
        request_mock.assert_requested("post", "/v1/issuing/cardholders")

    def test_issuing_cardholder_retrieve(self, request_mock):
        t99.issuing.Cardholder.retrieve("ich_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "get",
            "/v1/issuing/cardholders/ich_xxxxxxxxxxxxx",
        )

    def test_issuing_cardholder_update(self, request_mock):
        t99.issuing.Cardholder.modify(
            "ich_xxxxxxxxxxxxx",
            metadata={"order_id": "6735"},
        )
        request_mock.assert_requested(
            "post",
            "/v1/issuing/cardholders/ich_xxxxxxxxxxxxx",
        )

    def test_issuing_cardholder_list(self, request_mock):
        t99.issuing.Cardholder.list(limit=3)
        request_mock.assert_requested("get", "/v1/issuing/cardholders")

    def test_issuing_card_create(self, request_mock):
        t99.issuing.Card.create(
            cardholder="ich_xxxxxxxxxxxxx",
            currency="usd",
            type="virtual",
        )
        request_mock.assert_requested("post", "/v1/issuing/cards")

    def test_issuing_card_retrieve(self, request_mock):
        t99.issuing.Card.retrieve("ic_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "get", "/v1/issuing/cards/ic_xxxxxxxxxxxxx"
        )

    def test_issuing_card_update(self, request_mock):
        t99.issuing.Card.modify(
            "ic_xxxxxxxxxxxxx",
            metadata={"order_id": "6735"},
        )
        request_mock.assert_requested(
            "post", "/v1/issuing/cards/ic_xxxxxxxxxxxxx"
        )

    def test_issuing_card_list(self, request_mock):
        t99.issuing.Card.list(limit=3)
        request_mock.assert_requested("get", "/v1/issuing/cards")

    def test_issuing_dispute_create(self, request_mock):
        t99.issuing.Dispute.create(
            transaction="ipi_xxxxxxxxxxxxx",
            evidence={
                "reason": "fraudulent",
                "fraudulent": {"explanation": "Purchase was unrecognized."},
            },
        )
        request_mock.assert_requested("post", "/v1/issuing/disputes")

    def test_issuing_dispute_submit(self, request_mock):
        t99.issuing.Dispute.submit("idp_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "post",
            "/v1/issuing/disputes/idp_xxxxxxxxxxxxx/submit",
        )

    def test_issuing_dispute_retrieve(self, request_mock):
        t99.issuing.Dispute.retrieve("idp_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "get",
            "/v1/issuing/disputes/idp_xxxxxxxxxxxxx",
        )

    def test_issuing_dispute_update(self, request_mock):
        t99.issuing.Dispute.modify(
            "idp_xxxxxxxxxxxxx",
            evidence={
                "reason": "not_received",
                "not_received": {
                    "expected_at": 1590000000,
                    "explanation": "",
                    "product_description": "Baseball cap",
                    "product_type": "merchandise",
                },
            },
        )
        request_mock.assert_requested(
            "post",
            "/v1/issuing/disputes/idp_xxxxxxxxxxxxx",
        )

    def test_issuing_dispute_list(self, request_mock):
        t99.issuing.Dispute.list(limit=3)
        request_mock.assert_requested("get", "/v1/issuing/disputes")

    def test_issuing_transaction_retrieve(self, request_mock):
        t99.issuing.Transaction.retrieve("ipi_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "get",
            "/v1/issuing/transactions/ipi_xxxxxxxxxxxxx",
        )

    def test_issuing_transaction_update(self, request_mock):
        t99.issuing.Transaction.modify(
            "ipi_xxxxxxxxxxxxx",
            metadata={"order_id": "6735"},
        )
        request_mock.assert_requested(
            "post",
            "/v1/issuing/transactions/ipi_xxxxxxxxxxxxx",
        )

    def test_issuing_transaction_list(self, request_mock):
        t99.issuing.Transaction.list(limit=3)
        request_mock.assert_requested("get", "/v1/issuing/transactions")

    def test_terminal_connectiontoken_create(self, request_mock):
        t99.terminal.ConnectionToken.create()
        request_mock.assert_requested("post", "/v1/terminal/connection_tokens")

    def test_terminal_location_create(self, request_mock):
        t99.terminal.Location.create(
            display_name="My First Store",
            address={
                "line1": "1234 Main Street",
                "city": "San Francisco",
                "country": "US",
                "postal_code": "94111",
            },
        )
        request_mock.assert_requested("post", "/v1/terminal/locations")

    def test_terminal_location_retrieve(self, request_mock):
        t99.terminal.Location.retrieve("tml_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "get",
            "/v1/terminal/locations/tml_xxxxxxxxxxxxx",
        )

    def test_terminal_location_update(self, request_mock):
        t99.terminal.Location.modify(
            "tml_xxxxxxxxxxxxx",
            display_name="My First Store",
        )
        request_mock.assert_requested(
            "post",
            "/v1/terminal/locations/tml_xxxxxxxxxxxxx",
        )

    def test_terminal_location_delete(self, request_mock):
        t99.terminal.Location.delete("tml_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "delete",
            "/v1/terminal/locations/tml_xxxxxxxxxxxxx",
        )

    def test_terminal_location_list(self, request_mock):
        t99.terminal.Location.list(limit=3)
        request_mock.assert_requested("get", "/v1/terminal/locations")

    def test_terminal_reader_create(self, request_mock):
        t99.terminal.Reader.create(
            registration_code="puppies-plug-could",
            label="Blue Rabbit",
            location="tml_1234",
        )
        request_mock.assert_requested("post", "/v1/terminal/readers")

    def test_terminal_reader_retrieve(self, request_mock):
        t99.terminal.Reader.retrieve("tmr_P400-123-456-789")
        request_mock.assert_requested(
            "get",
            "/v1/terminal/readers/tmr_P400-123-456-789",
        )

    def test_terminal_reader_update(self, request_mock):
        t99.terminal.Reader.modify(
            "tmr_P400-123-456-789", label="Blue Rabbit"
        )
        request_mock.assert_requested(
            "post",
            "/v1/terminal/readers/tmr_P400-123-456-789",
        )

    def test_terminal_reader_delete(self, request_mock):
        t99.terminal.Reader.delete("tmr_P400-123-456-789")
        request_mock.assert_requested(
            "delete",
            "/v1/terminal/readers/tmr_P400-123-456-789",
        )

    def test_terminal_reader_list(self, request_mock):
        t99.terminal.Reader.list(limit=3)
        request_mock.assert_requested("get", "/v1/terminal/readers")

    def test_order_create(self, request_mock):
        t99.Order.create(
            currency="usd",
            email="jenny.rosen@example.com",
            items=[{"type": "sku", "parent": "sku_xxxxxxxxxxxxx"}],
            shipping={
                "name": "Jenny Rosen",
                "address": {
                    "line1": "1234 Main Street",
                    "city": "San Francisco",
                    "state": "CA",
                    "country": "US",
                    "postal_code": "94111",
                },
            },
        )
        request_mock.assert_requested("post", "/v1/orders")

    def test_order_retrieve(self, request_mock):
        t99.Order.retrieve("or_xxxxxxxxxxxxx")
        request_mock.assert_requested("get", "/v1/orders/or_xxxxxxxxxxxxx")

    def test_order_update(self, request_mock):
        t99.Order.modify("or_xxxxxxxxxxxxx", metadata={"order_id": "6735"})
        request_mock.assert_requested("post", "/v1/orders/or_xxxxxxxxxxxxx")

    def test_order_pay(self, request_mock):
        t99.Order.pay("or_xxxxxxxxxxxxx", source="tok_xxxx")
        request_mock.assert_requested(
            "post", "/v1/orders/or_xxxxxxxxxxxxx/pay"
        )

    def test_order_list(self, request_mock):
        t99.Order.list(limit=3)
        request_mock.assert_requested("get", "/v1/orders")

    def test_orderreturn_retrieve(self, request_mock):
        t99.OrderReturn.retrieve("orret_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "get",
            "/v1/order_returns/orret_xxxxxxxxxxxxx",
        )

    def test_orderreturn_list(self, request_mock):
        t99.OrderReturn.list(limit=3)
        request_mock.assert_requested("get", "/v1/order_returns")

    def test_sku_create(self, request_mock):
        t99.SKU.create(
            attributes={"size": "Medium", "gender": "Unisex"},
            price=1500,
            currency="usd",
            inventory={"type": "finite", "quantity": 500},
            product="prod_xxxxxxxxxxxxx",
        )
        request_mock.assert_requested("post", "/v1/skus")

    def test_sku_retrieve(self, request_mock):
        t99.SKU.retrieve("sku_xxxxxxxxxxxxx")
        request_mock.assert_requested("get", "/v1/skus/sku_xxxxxxxxxxxxx")

    def test_sku_update(self, request_mock):
        t99.SKU.modify("sku_xxxxxxxxxxxxx", metadata={"order_id": "6735"})
        request_mock.assert_requested("post", "/v1/skus/sku_xxxxxxxxxxxxx")

    def test_sku_list(self, request_mock):
        t99.SKU.list(limit=3)
        request_mock.assert_requested("get", "/v1/skus")

    def test_sku_delete(self, request_mock):
        t99.SKU.delete("sku_xxxxxxxxxxxxx")
        request_mock.assert_requested("delete", "/v1/skus/sku_xxxxxxxxxxxxx")

    def test_sigma_scheduledqueryrun_retrieve(self, request_mock):
        t99.sigma.ScheduledQueryRun.retrieve("sqr_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "get",
            "/v1/sigma/scheduled_query_runs/sqr_xxxxxxxxxxxxx",
        )

    def test_sigma_scheduledqueryrun_list(self, request_mock):
        t99.sigma.ScheduledQueryRun.list(limit=3)
        request_mock.assert_requested("get", "/v1/sigma/scheduled_query_runs")

    def test_reporting_reportrun_create(self, request_mock):
        t99.reporting.ReportRun.create(
            report_type="balance.summary.1",
            parameters={
                "interval_start": 1522540800,
                "interval_end": 1525132800,
            },
        )
        request_mock.assert_requested("post", "/v1/reporting/report_runs")

    def test_reporting_reportrun_retrieve(self, request_mock):
        t99.reporting.ReportRun.retrieve("frr_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "get",
            "/v1/reporting/report_runs/frr_xxxxxxxxxxxxx",
        )

    def test_reporting_reportrun_list(self, request_mock):
        t99.reporting.ReportRun.list(limit=3)
        request_mock.assert_requested("get", "/v1/reporting/report_runs")

    def test_reporting_reporttype_retrieve(self, request_mock):
        t99.reporting.ReportType.retrieve("balance.summary.1")
        request_mock.assert_requested(
            "get",
            "/v1/reporting/report_types/balance.summary.1",
        )

    def test_reporting_reporttype_list(self, request_mock):
        t99.reporting.ReportType.list()
        request_mock.assert_requested("get", "/v1/reporting/report_types")

    def test_webhookendpoint_create(self, request_mock):
        t99.WebhookEndpoint.create(
            url="https://example.com/my/webhook/endpoint",
            enabled_events=["charge.failed", "charge.succeeded"],
        )
        request_mock.assert_requested("post", "/v1/webhook_endpoints")

    def test_webhookendpoint_retrieve(self, request_mock):
        t99.WebhookEndpoint.retrieve("we_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "get",
            "/v1/webhook_endpoints/we_xxxxxxxxxxxxx",
        )

    def test_webhookendpoint_update(self, request_mock):
        t99.WebhookEndpoint.modify(
            "we_xxxxxxxxxxxxx",
            url="https://example.com/new_endpoint",
        )
        request_mock.assert_requested(
            "post",
            "/v1/webhook_endpoints/we_xxxxxxxxxxxxx",
        )

    def test_webhookendpoint_list(self, request_mock):
        t99.WebhookEndpoint.list(limit=3)
        request_mock.assert_requested("get", "/v1/webhook_endpoints")

    def test_webhookendpoint_delete(self, request_mock):
        t99.WebhookEndpoint.delete("we_xxxxxxxxxxxxx")
        request_mock.assert_requested(
            "delete",
            "/v1/webhook_endpoints/we_xxxxxxxxxxxxx",
        )

    def test_customer_list_payment_methods(self, request_mock):
        t99.Customer.list_payment_methods("cus_xyz", type="card")
        request_mock.assert_requested(
            "get",
            "/v1/customers/cus_xyz/payment_methods",
        )

    def test_checkout_session_expire(self, request_mock):
        t99.checkout.Session.expire("sess_xyz")
        request_mock.assert_requested(
            "post",
            "/v1/checkout/sessions/sess_xyz/expire",
        )
