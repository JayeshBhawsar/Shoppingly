from django.urls import path
from app import views

from django.conf.urls.static import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm


urlpatterns = [
    # path('', views.home),
    path('', views.ProductView.as_view(), name='home'),

    # path('product-detail/', views.product_detail, name='product-detail'),
    path('product-detail/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),

    # Add Products in Cart
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    
    # Show Products in Cart
    path('cart/', views.show_cart, name='showcart'),
    
    # Product Quantity increasing using ajax
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    
    # Product quantyti remove by ajax
    path('removecart/', views.remove_cart, name='removecart'),
    
    # path('profile/', views.profile, name='profile'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    
    
    path('address/', views.address, name='address'),

    ###### path('changepassword/', views.change_password, name='changepassword'),

    

    

    # Bottomwear
    path('bottomwear/', views.bottomwear, name='bottomwear'),
    path('bottomwear/<slug:data>', views.bottomwear, name='bottomweardata'),
    
    # Topwear
    path('topwear/', views.topwear, name='topwear'),
    path('topwear/<slug:data>', views.topwear, name='topweardata'),
    
    # Mobile
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),

    # Laptop
    path('laptop/', views.laptop, name='laptop'),
    path('laptop/<slug:data>', views.laptop, name='laptopdata'),
    
    # Book
    path('book/', views.book, name='book'),
    path('book/<slug:data>', views.book, name='bookdata'),
    
    
    
    
    
    

    # Login views
    # path('login/', views.login, name='login'),
    # Without creating any view function, give url and mension class based views in path
    path('account/login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),

    # Logout views
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    # Registration
    # path('registration/', views.customerregistration, name='customerregistration'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),

    # PasswordChange
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'), name='passwordchange'),
    
    # After PasswordChange
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),
    
    # Reset Password
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    
    # After Password Reset
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
    
    # After Password Reset Done
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    
    # After Password Reset Confirm
    path('password-reset-complete', auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),
    
    
    
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    
    
    path('buy/', views.buy_now, name='buy-now'),
    
    path('orders/', views.orders, name='orders'),
    
    
    # REST-API 
    path('customer_api/customers/', views.customer_json_list),
    
    path('customer_api/customers/<int:id>/', views.customer_json_detail),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
