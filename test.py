from src.preprocessing import prepare_transactions
from src.apriori import apriori
from src.rules import (
    generate_rules,
    filter_performance_rules,
    sort_rules,
    format_rules
)


# Dataset path
file_path = "data/student_learning_patterns_10000.csv"


# -----------------------------
# 1. PREPROCESSING
# -----------------------------

df, transactions = prepare_transactions(file_path)

print("Total students:", len(df))
print("Total transactions:", len(transactions))


# -----------------------------
# 2. APRIORI
# -----------------------------

frequent_itemsets, levels = apriori(
    transactions,
    min_support=0.10,
    max_length=3
)

print("\nApriori Levels:")

for level in levels:

    print(
        f"L{level['level']}: "
        f"{level['frequent_count']} frequent itemsets"
    )


# -----------------------------
# 3. ASSOCIATION RULES
# -----------------------------

rules = generate_rules(
    frequent_itemsets,
    transactions,
    min_confidence=0.60
)


# Keep only learning → performance rules
performance_rules = filter_performance_rules(rules)


# Sort by lift
performance_rules = sort_rules(
    performance_rules,
    metric="lift"
)


# Format for displaying
formatted_rules = format_rules(
    performance_rules
)


# -----------------------------
# 4. DISPLAY TOP RULES
# -----------------------------

print("\nTop Association Rules:\n")

for rule in formatted_rules[:10]:

    print(rule)