from itertools import combinations

from .apriori import calculate_support


def generate_subsets(itemset):
    """
    Generate all non-empty proper subsets
    of an itemset.
    """

    subsets = []

    items = list(itemset)

    for r in range(1, len(items)):

        for combination in combinations(items, r):

            subsets.append(frozenset(combination))

    return subsets


def generate_rules(
    frequent_itemsets,
    transactions,
    min_confidence=0.60
):
    """
    Generate association rules from frequent itemsets.

    Metrics:
        Support
        Confidence
        Lift
    """

    rules = []

    # Go through each level
    for level in frequent_itemsets:

        # Rules need at least 2 items
        if level < 2:
            continue

        for itemset in frequent_itemsets[level]:

            itemset_support = calculate_support(
                itemset,
                transactions
            )

            subsets = generate_subsets(itemset)

            for antecedent in subsets:

                consequent = itemset - antecedent

                if len(consequent) == 0:
                    continue

                antecedent_support = calculate_support(
                    antecedent,
                    transactions
                )

                consequent_support = calculate_support(
                    consequent,
                    transactions
                )

                if antecedent_support == 0:
                    continue

                # Confidence
                confidence = (
                    itemset_support /
                    antecedent_support
                )

                # Lift
                if consequent_support == 0:
                    continue

                lift = (
                    confidence /
                    consequent_support
                )

                # Keep only rules above confidence threshold
                if confidence >= min_confidence:

                    rules.append({
                        "antecedent": antecedent,
                        "consequent": consequent,
                        "support": itemset_support,
                        "confidence": confidence,
                        "lift": lift
                    })

    return rules


def filter_performance_rules(rules):
    """
    Keep rules where the consequent is a performance outcome.

    Example:

    Practice Problems + Revision
                ↓
        Performance: High
    """

    filtered_rules = []

    for rule in rules:

        consequent = rule["consequent"]

        if any(
            item.startswith("Performance:")
            for item in consequent
        ):
            filtered_rules.append(rule)

    return filtered_rules


def sort_rules(rules, metric="lift"):
    """Sort rules by support, confidence or lift."""

    return sorted(
        rules,
        key=lambda x: x[metric],
        reverse=True
    )


def format_rules(rules):
    """
    Convert rules into a DataFrame-friendly
    list of dictionaries.
    """

    formatted = []

    for rule in rules:

        antecedent = ", ".join(
            sorted(rule["antecedent"])
        )

        consequent = ", ".join(
            sorted(rule["consequent"])
        )

        formatted.append({
            "Rule": f"{antecedent} → {consequent}",
            "Support": round(
                rule["support"] * 100, 2
            ),
            "Confidence": round(
                rule["confidence"] * 100, 2
            ),
            "Lift": round(
                rule["lift"], 2
            )
        })

    return formatted