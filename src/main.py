#This is the starting point of the project
import plaid_client
import reminders

def main():
    print("Getting the public token")
    public_token = plaid_client.create_sandbox_public_token()

    print("Exchanging for access token")
    access_token = plaid_client.exchange_public_for_access_token(public_token=public_token)

    print("Fetching accounts")
    accounts = plaid_client.get_accounts(access_token)
    #print(accounts)

    print("Update item webhook")
    plaid_client.update_item_webhook(access_token)

    print("Triggering sandbox transactions update...")
    plaid_client.trigger_sandbox_transactions(access_token)  # Fire webhook

    print("refresh transactions")
    plaid_client.refresh_transactions(access_token)

    plaid_client.wait_for_transactions()

    print("Fetching transactions")
    transactions = plaid_client.get_transactions(access_token)
    #print("Fetched Transactions:", len(transactions['added']))
    #print("Fetched Transactions: ", transactions)

    print("Fetch the liability accounts")
    liabilities = plaid_client.get_liabilities(access_token)

    account_id = 0.0
    next_payment_due_date  = 0.0
    card_limit = 0.0
    last_statement_balance = 0.0

    for liability in liabilities['liabilities']['credit']:
        print("liability: " ,liability)
        account_id = liability['account_id']
        next_payment_due_date = liability['next_payment_due_date']
        last_statement_balance = liability['last_statement_balance']
        print("credit card account number ", account_id)
        print("when your next payment is due ", next_payment_due_date)

    for account in liabilities['accounts']:
        if account['account_id'] == account_id:
            card_limit = account['balances']['limit']
    amount_due = card_limit - last_statement_balance
    print("The limit for this credit card is: ", card_limit)
    #print("Fetched liablities: ",liabilities)
     # Step 2: Fetch transactions from Plaid
   # transactions = plaid_client.get_transactions(access_token)
    #print("Fetched Transactions:", transactions)
    
    reminders.set_reminder(next_payment_due_date, account_id, amount_due)

    # Extract relevant details (e.g., due dates, amounts)
    ##due_dates = reminders.extract_due_dates(transactions)

     # Trigger reminder notifications
    ##for due_date, amount in due_dates:
    ##    reminders.send_reminder(due_date, amount)
    
    

#acc_request = client.AccountsGetRequest(access_token = access_token)
#acc_response = client.accounts_get(acc_request)
#accounts = acc_response['accounts']
#print(accounts)

#for account in accounts:
#    if account['type'] == 'credit' and account['subtype'] == 'credit card':
#        print(account)

if __name__ == "__main__":
    main() 