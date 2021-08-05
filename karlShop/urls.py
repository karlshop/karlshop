from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
admin.site.site_header="Karl Shop"

from mainApp import views as mainView
urlpatterns = [
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('process-payment/<int:num>/', mainView.process_payment, name='process_payment'),
    path('payment-done/', mainView.payment_done, name='payment_done'),
    path('payment-cancelled/', mainView.payment_canceled, name='payment_cancelled'),

    path('admin/', admin.site.urls),
    path('',mainView.home),
    path('shop/<str:m>/<str:s>/<str:b>/',mainView.shop),
    path('checkout/',mainView.checkout),
    path('productdetails/<int:num>/',mainView.productDetails),
    path('cart/',mainView.cart),
    path('login/',mainView.loginUser),
    path('signup/',mainView.signupUser),
    path('logout/',mainView.logoutUser),
    path('sellerprofile/',mainView.sellerProfile),
    path('buyerprofile/',mainView.buyerProfile),
    path('profile/',mainView.profile),
    path('addproduct/',mainView.addProduct),
    path('deleteproduct/<int:num>/',mainView.deleteProduct),
    path('editproduct/<int:num>/',mainView.editProduct),
    path('wishlist/<int:num>/',mainView.mywishlist),
    path('deletewishlist/<int:num>/',mainView.deleteWishlist),
    path('deletecart/',mainView.deleteCart),
    path('forgetPassword/',mainView.forgetPassword),
    path('confirmOTP/<str:username>/',mainView.confirmOTP),
    path('generatePassword/<str:username>/',mainView.generatePassword),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
