#Handles interactions with Plaid API. To authenticate with plaid using API keys.
import plaid
import plaid.model
import config
import time
from plaid.api import plaid_api
from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.products import Products
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.sandbox_item_fire_webhook_request import SandboxItemFireWebhookRequest
import json
from datetime import date
from plaid.model.webhook_type import WebhookType

from plaid.model.item_webhook_update_request import ItemWebhookUpdateRequest
from plaid.model.transactions_refresh_request import TransactionsRefreshRequest
from plaid.model.liabilities_get_request import LiabilitiesGetRequest

configuration = plaid.Configuration(
    host = plaid.Environment.Sandbox, 
    api_key = {
        "clientId": config.PLAID_CLIENT_ID,
        "secret": config.PLAID_SECRET_SANDBOX
    }
)
plaid_api_client = plaid.ApiClient(configuration)
wrapper_client = plaid_api.PlaidApi(plaid_api_client)
print("Plaid api host: ", configuration.host)

#client = Client(client_id = config.PLAID_CLIENT_ID,
#                secret = config.PLAID_SECRET_SANDBOX,
#                environment = config.PLAID_ENV,
#               ) # this is to initate a client  instance to interact with the plaid api.

def create_sandbox_public_token():
# Create the request to be sent to function to create the public token
    sandbox_token_request = SandboxPublicTokenCreateRequest(
        institution_id = 'ins_109508',  # Example test institution in Sandbox. First playypus Bank.
        initial_products = [Products('transactions'), Products('statements'), Products('identity'), Products('liabilities')],     # Products you want to use
        options = {
        "statements": {
                "start_date": date(2024, 1, 1),  # Specify the start date in the required format
                "end_date": date(2024, 10, 30)     # Specify the end date in the required format
        }  # Add this to satisfy the API requirements
        }
    )

    #print("Request being sent to Plaid:")
    #print(json.dumps(sandbox_token_request, indent=4))

    # Generate public token fron the link token.
    pt_response = wrapper_client.sandbox_public_token_create(sandbox_token_request)
    return pt_response
#Get the public token from the response.
#public_token = pt_response['public_token']
#print(f'Public Token: {public_token}')

#exchange this public_token for a permanent access_token that you can use for API requests.
# exchanged for an access_token, create the request.
def exchange_public_for_access_token(public_token):
    exchange_request = ItemPublicTokenExchangeRequest(
        public_token=public_token['public_token']
    ) # this function is a data struture, a model. not an actual method for the api

    exchange_response = wrapper_client.item_public_token_exchange(exchange_request)

    #access_token = exchange_response['access_token']
    access_token = exchange_response.access_token # now returns response objects, not dictionaries.
    return access_token

#Now let you retrieve the credit card account that we want 
def get_accounts(access_token):
    acc_request = AccountsGetRequest(access_token = access_token)
    acc_response = wrapper_client.accounts_get(acc_request)
    return acc_response.accounts


def update_item_webhook(access_token):
    request = ItemWebhookUpdateRequest(
        access_token=access_token,
        webhook="https://webhook.site/f2552a3b-5d5a-4cee-abed-6716b128a0f8"  # Replace with a valid URL
    )
    response = wrapper_client.item_webhook_update(request)
    print("Webhook updated:", response)

def trigger_sandbox_transactions(access_token):
    request = SandboxItemFireWebhookRequest(
        access_token=access_token,
        webhook_type=WebhookType("TRANSACTIONS"), 
        webhook_code='DEFAULT_UPDATE'
    )
    response = wrapper_client.sandbox_item_fire_webhook(request)
    print("Sandbox transactions triggered:", response)



def refresh_transactions(access_token):
    request = TransactionsRefreshRequest(access_token=access_token)
    response = wrapper_client.transactions_refresh(request)
    print("Sandbox transactions refreshed:", response)


def wait_for_transactions():
    print("Waiting for transactions to be processed...")
    time.sleep(15)  # Wait 5 seconds before retrying

def get_transactions(access_token):
    transaction_request = TransactionsSyncRequest (
        access_token = access_token
    )
    transaction_response = wrapper_client.transactions_sync(transaction_request)
    #print(transaction_response)
    #return transaction_response.transactions
    return transaction_response
    
def get_liabilities(access_token):
    request = LiabilitiesGetRequest(
        access_token = access_token
        )
    response = wrapper_client.liabilities_get(request)
    return response
