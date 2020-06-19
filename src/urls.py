from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (RegisterView,
                    BillView,
                    ClientView,
                    ProductView,
                    ProductList,
                    BillList,
                    ClientList,
                    BillDetailView,
                    ProductDetailView,
                    ClientDetailView,
                    BillUpdateView,
                    ClientUpdateView,
                    ProductUpdateView,
                    BillDeleteView,
                    ClientDeleteView,
                    ProductDeleteView,
                    GeneratePDF,
                    BillDownloadView, BillFilterView)

app_name = 'src'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('bill/', BillView.as_view(), name='bill'),
    path('client/', ClientView.as_view(), name='client'),
    path('product/', ProductView.as_view(), name='product'),
    path('bill-list/', BillList.as_view(), name='bill-list'),
    path('client-list/', ClientList.as_view(), name='client-list'),
    path('product-list/', ProductList.as_view(), name='product-list'),
    path('bill-detail/<int:pk>/', BillDetailView.as_view(), name='bill-detail'),
    path('product-detail/<int:pk>/',
         ProductDetailView.as_view(), name='product-detail'),
    path('client-detail/<int:pk>/',
         ClientDetailView.as_view(), name='client-detail'),
    path('bill-update/<int:pk>/', BillUpdateView.as_view(), name='bill-update'),
    path('client-update/<int:pk>/',
         ClientUpdateView.as_view(), name='client-update'),
    path('product-update/<int:pk>/',
         ProductUpdateView.as_view(), name='product-update'),
    path('bill-delete/<int:pk>/', BillDeleteView.as_view(), name='bill-delete'),
    path('product-delete/<int:pk>/',
         ProductDeleteView.as_view(), name='product-delete'),
    path('client-delete/<int:pk>/',
         ClientDeleteView.as_view(), name='client-delete'),
    path('bill-download/', BillDownloadView.as_view(), name='bill-download'),
    path('bill-filter/', BillFilterView.as_view(), name='bill-filter'),
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('change-password/',
         auth_views.PasswordChangeView.as_view(
             template_name='change_password.html'),
         name='change-password'),
    path('password-change-done',
         auth_views.PasswordChangeDoneView.as_view(
             template_name='change_password_done.html'),
         name='password_change_done'),
    path('pdf/<int:pk>/', GeneratePDF.as_view(), name='pdf'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='password_reset.html'
         ),
         name='password_reset'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
