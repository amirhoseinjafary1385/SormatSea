#Activate Iranian National Bank

import requests
from django.contrib import settings
from django.urls import reverse
from django.shortcuts import get_object_or_404
from .models import NFT, Transaction
import json
from datetime import datetime



class BankMeliPaymentGateway:
    """
    Handles NFT purchases using Bank Melli payment gateway
    """

    def __init__(self):
        self.merchant_id = settings.BANK_MELLI_MERCHANT_ID
        self.terminal_id = settings.BANK_MELLI_TERMINAL_ID
        self.redirect_url = settings.BASE_URL + reverse('payment_verify')
        self.api_url = "https://bankmelli.com/pg/services/rest/"
    

    def generate_payment_request(self, nft_id, user_id, amount):

        """
        Generate payment request to Bank Melli gateway
        """

        nft = NFT.objects.get(pk = nft_id)

        # Create Transaction form

        transaction = Transaction.objects.create(
            nft = nft,
            user_id = user_id,
            amount = amount,
            status = "Pending",
            payment_gateway = 'bank_melli',
        )

        payload = {

            "MerchantID": self.merchant_id,
            "TerminalID": self.terminal_id,
            "Amount": int(amount * 10) # Convert to IRR
            "Amount": int(amount * 10000),  # Convert to IRT
            "OrderID": transaction.id,
            "LocalDateTime": datetime.now().strftime("%Y%m%d%H%M%S"),
            "ReturnURL": self.redirect_url,
            "AdditionalData": json.dumps({
            "nft_id": nft_id,
            "user_id": user_id,
        #    "admin_id": admin_id,

            })

        }


        try:
            response = requests.post(f"{self.api_url}request",
            json = payload,
            headers = {'Content-Type': 'application/json'}
            )
            response.raise_for_status()

            data = response.json()
            if data.get('Status')
 

                




def verify_payment(self, authority, amount):

    """
    Verify payment with Bank Melli after user returns from gateway
    """

    try:
        transaction = Transaction.objects.get(bank_reference=authority)

    payload= {
        "MerchantID": self.merchant_id,
        "TerminalID": self.terminal_id,
        "Authority": authority,
        "Amount": int(amount * 10)
    }

    response = requests.post(
        f"{self.api_url}verify",
        json = payload,
        headers = {'Content-Type': 'application/json'}
    )

    response.raise_for_status()

    data = response.json()
    if data.get('Status') == 1:
        #Success 
        transaction.status = 'completed'
        transaction.bank_trace_number = data.get('TraceNumber')
        transaction.save()

        nft = transaction.nft
        nft.owner = transaction.user
        nft.save()

        return{
            'success': True,
            'transaction': transaction,
            'nft': nft,

        }
    raise Exception(data.get('Message', 'Payment verification failed'))

except Exception as e:
    if 'transaction' in locals():
        transaction.status = 'failed'
        transaction.error_message = str(e)
        transaction.save()
    return {'success': False, 'message': str(e)}


class ZarinpalPaymentGateway:
    """
    Simple Zarinpal gateway helper.

    Uses Zarinpal's REST API (https://zarinpal.com) to create a payment
    and verify it. This implementation is intentionally minimal and
    synchronous — for production use you should harden error handling,
    retries, logging, and secure configuration.
    """

    def __init__(self):
        self.merchant_id = getattr(settings, 'ZARINPAL_MERCHANT_ID', None)
        self.callback_path = reverse('zarinpal_verify')
        self.callback_url = getattr(settings, 'BASE_URL', '') + self.callback_path
        # use sandbox or production depending on settings
        self.sandbox = getattr(settings, 'ZARINPAL_SANDBOX', True)
        self.request_url = 'https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json' if self.sandbox else 'https://api.zarinpal.com/pg/rest/WebGate/PaymentRequest.json'
        self.verify_url = 'https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json' if self.sandbox else 'https://api.zarinpal.com/pg/rest/WebGate/PaymentVerification.json'

    def create_payment(self, nft_id, user, amount, description=None):
        """Create a Zarinpal payment and return the payment URL.

        - nft_id: NFT primary key
        - user: Django user instance
        - amount: Decimal/float amount in IRT (toman) or as agreed in your app
        Returns: dict with keys: success, payment_url (if success), transaction
        """
        nft = get_object_or_404(NFT, pk=nft_id)
        # create Transaction
        transaction = Transaction.objects.create(
            nft=nft,
            user=user,
            amount=amount,
            currency='IRT',
            payment_gateway='zarinpal',
            status='pending',
        )

        payload = {
            'MerchantID': self.merchant_id,
            'Amount': int(float(amount)),
            'CallbackURL': self.callback_url,
            'Description': description or f'Purchase NFT {nft.pk}',
            'Metadata': json.dumps({'transaction_id': transaction.id, 'nft_id': nft_id, 'user_id': user.id}),
        }

        try:
            resp = requests.post(self.request_url, json=payload, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            if data.get('Status') in (100, '100'):
                authority = data.get('Authority')
                payment_url = f'https://sandbox.zarinpal.com/pg/StartPay/{authority}' if self.sandbox else f'https://www.zarinpal.com/pg/StartPay/{authority}'
                transaction.bank_reference = authority
                transaction.save()
                return {'success': True, 'payment_url': payment_url, 'transaction': transaction}
            else:
                transaction.mark_as_failed(f"Zarinpal request failed: {data}")
                return {'success': False, 'message': data}
        except Exception as e:
            transaction.mark_as_failed(str(e))
            return {'success': False, 'message': str(e)}

    def verify_payment(self, authority, amount):
        """Verify a Zarinpal payment using Authority and Amount.

        Returns dict {success: bool, transaction: Transaction or None, message: str}
        """
        try:
            transaction = Transaction.objects.get(bank_reference=authority, payment_gateway='zarinpal')
        except Transaction.DoesNotExist:
            return {'success': False, 'message': 'Transaction not found'}

        payload = {
            'MerchantID': self.merchant_id,
            'Authority': authority,
            'Amount': int(float(amount)),
        }
        try:
            resp = requests.post(self.verify_url, json=payload, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            if data.get('Status') in (100, 101, '100', '101'):
                # success
                transaction.mark_as_completed()
                transaction.bank_trace_number = str(data.get('RefID') or data.get('RefID'))
                transaction.save()
                # transfer ownership
                if transaction.nft:
                    transaction.nft.owner = transaction.user
                    transaction.nft.save()
                return {'success': True, 'transaction': transaction, 'message': data}
            else:
                transaction.mark_as_failed(str(data))
                return {'success': False, 'message': data}
        except Exception as e:
            transaction.mark_as_failed(str(e))
            return {'success': False, 'message': str(e)}

class NFTPaymentManager:

    def __init__(self):
        self.zarinpal = ZarinpalPaymentGateway()
    
    def _get_amount_for_nft(self, nft):

        try:
            if getattr(nft, "price_irt", None):
                return float(nft.price_irt)
            except Exception:
                pass
            try:
                return float(nft.price_polygon or 0)
            except Exception:
                return 0.0
    def process_payment(self, nft_id, user_or_userid):
        nft = get_object_or_404(NFT, pk=nft_id)
        User = get_user_model()
        user = user_or_userid
        if not hasattr(user, "pk"):
            user = get_object_or_404(User, pk=user_or_userid)

        amount = self._get_amount_for_nft(nft)
        transaction = Transaction.objects.create(
            nft=nft,
            user=user,
            amount=amount,
            currency='IRT',
            payment_gateway='zarinpal',
            status='pending'
        )

        return self.zarinpal.create_payment(nft, transaction, amount , description=f'Buy NFT {nft.pk}')
    def verify_payment(self, authority, amount=None):
        try:
            transaction = Transaction.objects.get(bank_reference=authority)
        except Transaction.DoesNotExist:
            return {'success': False, 'message': 'Transaction not found'}

        amount = amount if amount is not None else float(transaction.amount)
        return self.zarinpal.verify_payment(transaction, amount)
