# Replace the API Key and Shared Secret with the one given for your
# App by Shopify.
#
# To create an application, or find the API Key and Secret, visit:
# - for private Apps:
# https://${YOUR_SHOP_NAME}.myshopify.com/admin/api
# - for partner Apps:
# https://www.shopify.com/services/partners/api_clients
#
# You can ignore this file in git using the following command:
#   git update-index --assume-unchanged shopify_settings.py
import os

SHOPIFY_API_KEY = "17b9cd9cbbabc1272a1ad42206221fff"
SHOPIFY_API_SECRET = "65c6ae1bc7e012144ef27507416de2e1"

# See http://api.shopify.com/authentication.html for available scopes
# to determine the permisssions your app will need.
SHOPIFY_API_SCOPE = ['read_products', 'read_orders', 'write_products', 'write_orders']
