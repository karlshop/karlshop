from django import template
from mainApp.models import Product
register = template.Library()

@register.filter(name='getQ')
def getQ(request,i):
    cart = request.session.get('cart',None)
    if(cart):
        q=cart[str(i)]
        return q
    else:
        return None

@register.filter(name='calculateTotal')
def calculateTotal(request,i):
    product = Product.objects.get(pid=i)
    cart = request.session.get('cart', None)
    if (cart):
        q = cart[str(i)]
        return q*product.finalPrice
    else:
        return None