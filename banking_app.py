import streamlit as st

# ------------------- DATA MODELS -------------------
class Account:
    def __init__(self, customer_name, account_number, balance, acc_type):
        self.customer_name = customer_name
        self.account_number = account_number
        self.balance = balance
        self.type = acc_type
        self.transactions = []

    def add_transaction(self, t):
        self.transactions.append(t)

    def show_transactions(self):
        return [str(t) for t in self.transactions]


class Transaction:
    def __init__(self, account, credited_amount=0.0, debited_amount=0.0):
        self.account = account
        self.credited_amount = credited_amount
        self.debited_amount = debited_amount
        self.balance = account.balance

    def credit(self, amount):
        self.account.balance += amount
        self.balance = self.account.balance
        self.credited_amount = amount
        self.debited_amount = 0.0

    def debit(self, amount):
        self.account.balance -= amount
        self.balance = self.account.balance
        self.debited_amount = amount
        self.credited_amount = 0.0

    def __str__(self):
        return f"{self.account.customer_name}\t{self.account.account_number}\t{self.credited_amount}\t{self.debited_amount}\t{self.balance}"


class Customer:
    def __init__(self, customer_id, password):
        self.customer_id = customer_id
        self.password = password
        self.accounts = []

    def add_account(self, acc):
        self.accounts.append(acc)

    def get_account(self, acc_number):
        for acc in self.accounts:
            if acc.account_number == acc_number:
                return acc
        return None


class Bank:
    def __init__(self):
        self.customers = {}
        self.accounts = {}
        self.customer_id_counter = 101
        self.account_number_counter = 913122106001

    def create_account(self, name, password, acc_type, amount):
        cust_id = self.customer_id_counter
        acc_number = self.account_number_counter
        customer = Customer(cust_id, password)
        account = Account(name, acc_number, 0.0, acc_type)
        customer.add_account(account)

        t = Transaction(account)
        t.credit(amount)
        account.add_transaction(t)

        self.customers[cust_id] = customer
        self.accounts[acc_number] = account

        self.customer_id_counter += 1
        self.account_number_counter += 1

        return cust_id, acc_number

    def deposit(self, acc_number, amount):
        acc = self.accounts.get(acc_number)
        if acc:
            t = Transaction(acc)
            t.credit(amount)
            acc.add_transaction(t)
            return t
        return None

    def withdraw(self, acc_number, amount):
        acc = self.accounts.get(acc_number)
        if acc and acc.balance - amount >= 1000:
            t = Transaction(acc)
            t.debit(amount)
            acc.add_transaction(t)
            return t
        return None

    def all_transactions(self):
        result = []
        for acc in self.accounts.values():
            result.extend(acc.show_transactions())
        return result

    def transactions_for_customer(self, acc_number):
        acc = self.accounts.get(acc_number)
        if acc:
            return acc.show_transactions()
        return []


# ------------------- STREAMLIT WEB APP -------------------
st.set_page_config(page_title="Banking System", page_icon="💰", layout="centered")

if "bank" not in st.session_state:
    st.session_state.bank = Bank()

bank = st.session_state.bank

st.title("🏦 Simple Banking System")
st.caption("Built using **Streamlit** | Inspired by your Java console project 💻")

menu = ["Create Account", "Deposit", "Withdraw", "Show All Transactions", "Customer Transactions"]
choice = st.sidebar.radio("📜 Menu", menu)

# ------------------- CREATE ACCOUNT -------------------
if choice == "Create Account":
    st.header("✨ Create New Account")
    name = st.text_input("Enter Customer Name")
    password = st.text_input("Set Password", type="password")
    acc_type = st.selectbox("Account Type", ["SAVING", "CURRENT"])
    amount = st.number_input("Initial Deposit (Min ₹1000)", min_value=1000.0, step=100.0)

    if st.button("Create Account"):
        cust_id, acc_number = bank.create_account(name, password, acc_type, amount)
        st.success("✅ Account Created Successfully!")
        st.info(f"Customer ID: {cust_id} | Account Number: {acc_number}")
        st.balloons()

# ------------------- DEPOSIT -------------------
elif choice == "Deposit":
    st.header("💵 Deposit Money")
    acc_number = st.number_input("Enter Account Number", min_value=913122106000)
    amount = st.number_input("Enter Deposit Amount", min_value=1.0)
    if st.button("Deposit"):
        txn = bank.deposit(acc_number, amount)
        if txn:
            st.success("💰 Deposit Successful!")
            st.write(f"**Transaction Details:** {txn}")
            st.balloons()
        else:
            st.error("❌ Invalid Account Number")

# ------------------- WITHDRAW -------------------
elif choice == "Withdraw":
    st.header("💸 Withdraw Money")
    acc_number = st.number_input("Enter Account Number", min_value=913122106000)
    amount = st.number_input("Enter Withdrawal Amount", min_value=1.0)
    if st.button("Withdraw"):
        txn = bank.withdraw(acc_number, amount)
        if txn:
            st.success("✅ Withdrawal Successful!")
            st.write(f"**Transaction Details:** {txn}")
            st.snow()
        else:
            st.error("⚠️ Insufficient Balance or Invalid Account")

# ------------------- ALL TRANSACTIONS -------------------
elif choice == "Show All Transactions":
    st.header("📋 All Bank Transactions")
    txns = bank.all_transactions()
    if txns:
        data = [t.split("\t") for t in txns]
        st.table(data)
    else:
        st.info("No transactions yet.")

# ------------------- CUSTOMER TRANSACTIONS -------------------
elif choice == "Customer Transactions":
    st.header("👤 Customer Transaction History")
    acc_number = st.number_input("Enter Account Number", min_value=913122106000)
    if st.button("Show Transactions"):
        txns = bank.transactions_for_customer(acc_number)
        if txns:
            data = [t.split("\t") for t in txns]
            st.table(data)
        else:
            st.warning("No transactions found for this account.")
