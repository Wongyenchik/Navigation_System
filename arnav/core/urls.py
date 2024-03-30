from django.urls import path
from django.contrib.auth import views as auth_views
from core import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add-user/", views.add_user, name="add-user"),
    path("sign-in/", views.signIn, name="sign-in"),
    path("add-item/", views.add_item, name="add-item"),
    path("forget-password/", auth_views.PasswordResetView.as_view(template_name="forget-password.html"), name="reset_password"),
    path("forget-password-sent/", auth_views.PasswordResetDoneView.as_view(template_name="password_reset.html"), name="password_reset_done"),
    path("forget-password/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="password_reseting.html"), name="password_reset_confirm"),
    path("forget-password-complete/", auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"), name="password_reset_complete"),
    path("logout/", views.log_out, name="log_out"),
    path("update-stock/", views.update_stock, name="update_stock"),
    path("update-detail/<str:pk>", views.update_product_detail, name="update-detail"),
    path("update-detail-done", views.update_detail_done, name="update-detail-done"),
    # path("update-user/<str:pk>", views.update_user, name="update-user"),
    path("delete-product/<str:pk>", views.delete_product, name="delete-product"),
    path("delete-user/<str:pk>", views.delete_user, name="delete-user"),
    path("scan-pick", views.scan_pick, name="scan-pick"),
    path("render-scan-page", views.render_scan_page, name="render-scan-page"),
    path("update-stock-picker/<str:pk>", views.update_stock_picker, name="update-stock-picker"),
    # path("search-results/", views.search_results, name="search-results"),
    path("add-to-pick/",views.add_to_pick, name="add-to-pick"),
    path("cart/",views.cart_view, name="cart"),
    path("navigation/",views.navigation_view, name="navigation"),
    path("delete-from-cart/",views.delete_item_from_cart, name="delete-from-cart"),
    path("start-location/",views.start_location, name="start-location"),
    path("clear-session/",views.clear_session, name="clear-session"),
    path("navigation-pick/<str:pk>",views.navigation_pick, name="navigation-pick"),
    path("depart/",views.depart, name="depart"),
    path("product-list/",views.product_list, name="product-list"),
    path("add-to-pick-list/",views.add_to_pick_list, name="add-to-pick-list"),
    path("item-pick/",views.item_pick, name="item-pick"),
    path("item-pick-scan/",views.item_pick_scan, name="item-pick-scan"),


]