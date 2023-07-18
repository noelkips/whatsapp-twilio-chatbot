from django.db import models

"""Line 4 to 9 – we create a class called BaseModel which subclasses
    from the Django model. The main reason for doing this is to 
    track at what time a record was recorded in the database without repetition
    """


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# M-pesa Payment models
""""we create a class called MpesaCalls. This class has four fields for capturing 
    the IP address, caller, conversation_id, content. In case you need to do validation
     before accepting payments, you can use this model to store the MpesaCalls for later analysis.
     """


class MpesaCalls(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()

    class Meta:
        verbose_name = 'Mpesa Call'
        verbose_name_plural = 'Mpesa Calls'


""""we create a class called MpesaCallBacks which has similar fields as MpesaCalls. 
This is used to store accepted Mpesa transactions without accessing each field in the body"""


class MpesaCallBacks(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()

    class Meta:
        verbose_name = 'Mpesa Call Back'
        verbose_name_plural = 'Mpesa Call Backs'


"""" we create a class called MpesaPayment which we use to store 
successful transactions. We store the amount, description of the payment,
type of payment, reference, first name, middle name, last name,
phone number used for payment and organization mpesa balance."""


class MpesaPayment(BaseModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    type = models.TextField()
    reference = models.TextField()
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.TextField()
    organization_balance = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Mpesa Payment'
        verbose_name_plural = 'Mpesa Payments'

    def __str__(self):
        return self.first_name
