import pandas as pd

def calculate_cashback(df, rules):
    cashback_data = []
    category_caps = {}

    # Prepare cap trackers
    for rule in rules:
        for category in rule["categories"]:
            category_caps[category] = {"cap": rule["monthly_cap"], "earned": 0}

    for _, row in df.iterrows():
        txn_type = row["Transaction Type"]
        amount = row["Amount"]
        cashback_percent = 0
        cap = -1
        matched = False

        for rule in rules:
            for category in rule["categories"]:
                if txn_type == category:
                    cashback_percent = rule["cashback_percent"]
                    cap = rule["monthly_cap"]
                    matched = True
                    break
            if matched:
                break

        if not matched:
            for rule in rules:
                if "Others" in rule["categories"]:
                    cashback_percent = rule["cashback_percent"]
                    cap = rule["monthly_cap"]
                    category = "Others"
                    break

        cashback = (cashback_percent / 100) * amount

        if cap >= 0:
            category_caps[txn_type]["earned"] += cashback
            if category_caps[txn_type]["earned"] > cap:
                cashback = max(0, cap - (category_caps[txn_type]["earned"] - cashback))

        cashback_data.append({
            "Date": row["Date"],
            "Transaction Type": txn_type,
            "Amount": amount,
            "Cashback %": cashback_percent,
            "Cashback": round(cashback, 2)
        })

    cashback_df = pd.DataFrame(cashback_data)
    summary = cashback_df.groupby("Transaction Type")["Cashback"].sum().reset_index()
    return cashback_df, summary
