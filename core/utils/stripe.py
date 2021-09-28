import stripe
from django.conf import settings

class MyStripe():

    def __init__(self):
        stripe.api_key = settings.API_KEY

    def createCustomer(self,user):

        # description
        # email
        # metadata
        # name
        # payment_method
        # phone
        # shipping    

        return stripe.Customer.create(email=user.email,name=user.name)

    def updateCustomer(self,customerId,user):

        # description
        # email
        # metadata
        # name
        # payment_method
        # phone
        # shipping    

        return stripe.Customer.modify(customerId,
            metadata={"email": user.email,"name": user.name},
        )

    def deleteCustomer(self,customerId):

        return stripe.Customer.delete(customerId)

    def createCard(self,customerId, data):
        return stripe.Customer.create_source(customerId, source=data["source"])

    def deleteCard(self, customerId, cardId):
        return stripe.Customer.delete_source(customerId, cardId)

    def createBank(self, customerId, bank_data):
        return stripe.Customer.create_source(customerId, source=bank_data)

    def retrieveBank(self, customerId, bankId):
        return stripe.Customer.retrieve_source(customerId, bankId)

    def updateBank(self, customerId, bankId, order):
        return stripe.Customer.modify_source(customerId, bankId, metadata={"order_id": order.id})

    def verifyBnak(self, customerId, bankId):
        bank_account = stripe.Customer.retrieve_source(customerId, bankId)
        return bank_account.verify(amounts=[32, 45])

    def deleteBank(self, customerId, bankId):
        return stripe.Customer.delete_source(customerId, bankId)

    def createCharge(self, amount, card, customerId):
        return stripe.Charge.create(amount=int(amount)*100, currency=settings.CURRENCY, source=card, customer=customerId)

    def retrieveCharge(self, chargeId):
        return stripe.Charge.retrieve(chargeId)

    def updateCharge(self, chargeId, order):
        return stripe.Charge.modify(chargeId, metadata={"order_id": order.id})

    def captureCharge(self, chargeId):
        return stripe.Charge.capture(chargeId)


    def createProduct(self, name):
        return  stripe.Product.create(name=name)

    def createPlan(self, amount, interval, product_id ):
        return  stripe.Plan.create(amount=amount, currency=settings.CURRENCY, interval=interval, product=product_id)

    def deletePlan(self, plan_id):
        return stripe.Plan.delete(str(plan_id),)

    def deleteProduct(self, product_id):
        return stripe.Product.delete(str(product_id),)

    def modifyProduct(self,product_id, name):

        return stripe.Product.modify(product_id, name=name)    

    def subscribePlan(self, customerId, plan_id,payment_method):

        return stripe.Subscription.create(customer=customerId, default_payment_method=payment_method, items=[{'price':plan_id}], )


    def CancelSubscriptionPlan(self, subscription_id):

        return stripe.Subscription.delete(subscription_id)

    def CreatePaymentMethod(self, token):
        return stripe.PaymentMethod.create(type="card", card={"token": token},)

    def PaymentMethodAttach(self, payment_method_id, customer_id):

        return stripe.PaymentMethod.attach(payment_method_id, customer=customer_id)


    def RetrieveSubscription(self, sub_id):

        return stripe.Subscription.retrieve(sub_id)

    def InvoiceStatus(self, invoice_id):
        return stripe.Invoice.retrieve(invoice_id)


#  stripe.Customer.modify("cus_INpRNROozma8dW", invoice_settings={"default_payment_method":"pm_1Hn3mdHn8nuO8gnZNWddfPhV"})