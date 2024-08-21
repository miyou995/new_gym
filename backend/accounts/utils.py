from django.shortcuts import render
from django.apps import apps
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType



def get_permissions():
    models = {
        model.__name__: model for model in apps.get_models(include_auto_created=False)
    }
    excluded_model_names = [
        'LogEntry', 'Prospect', 'HistoricalStockTransfer', 'HistoricalShippingAdress', 
        'HistoricalSalesOrder', 'HistoricalPurchaseOrder', 'HistoricalBillingAdress', 
        'Fonctionalite', 'Plan', 'Portfolio', 'Position', 'WishlistItem', 'ThemeScreenShot', 
        'Status', 'StockCheckItem', 'PurchaseOrder', 'StockTransfer', 'Tax', 'Notification',
        'StockTransferLineItem', 'PurchaseOrderLineItem', 'CategoryBanner', 'AtributesValue', 
        'CategorySpecs', 'EmailConfirmation', 'EmailAddress', 'DiscountLine', 'Theme', 
        'Comment', 'PhotoComment', 'Client', 'ContentType', 'Session', 
        'Supplier', 'SalesOrderLineItem', 'SocialAccount', 'StockCheck', 'ShippingAdress', 
        'PaymentMethod', 'BillingAdress', 'ProductDocument', 'SocialApp', 'SocialToken', 
        'PlanPrice', 'BasketLine', 'Site',
    ]

    excluded_content_types = ContentType.objects.filter(
        app_label__in=[model._meta.app_label for model in models.values()],
        model__in=excluded_model_names
    )
    content_types = ContentType.objects.exclude(id__in=excluded_content_types.values_list('id', flat=True))
    permissions = Permission.objects.filter(content_type__in=content_types).select_related('content_type')
    # print('permission---------------',permissions)

    permissions_dict = {}
    for permission in permissions:
        model_name = permission.content_type.model_class().__name__
        if model_name not in excluded_model_names:
            if model_name not in permissions_dict:
                permissions_dict[model_name] = []
            permissions_dict[model_name].append(permission)
        

    return permissions_dict