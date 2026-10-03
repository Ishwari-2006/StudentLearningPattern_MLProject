from itertools import combinations


def calculate_support(itemset, transactions):
    """
    Calculate support of an itemset.

    Support =
    Number of transactions containing itemset
    ------------------------------------------------
                    Total transactions
    """

    count = 0

    for transaction in transactions:
        if itemset.issubset(transaction):
            count += 1

    return count / len(transactions)


def get_all_items(transactions):
    """Get all unique items from all transactions."""

    items = set()

    for transaction in transactions:
        items.update(transaction)

    return items


def generate_candidates(previous_frequent_itemsets, k):
    """
    Generate candidate k-itemsets from
    frequent (k-1)-itemsets.
    """

    candidates = set()

    previous_list = list(previous_frequent_itemsets)

    for i in range(len(previous_list)):
        for j in range(i + 1, len(previous_list)):

            union = previous_list[i] | previous_list[j]

            if len(union) == k:
                candidates.add(frozenset(union))

    return candidates


def has_infrequent_subset(candidate, previous_frequent_itemsets):
    """
    Apriori pruning:

    If any (k-1) subset of a candidate is not frequent,
    then the candidate cannot be frequent.
    """

    k = len(candidate)

    for subset in combinations(candidate, k - 1):

        subset = frozenset(subset)

        if subset not in previous_frequent_itemsets:
            return True

    return False


def apriori(transactions, min_support=0.10, max_length=3):
    """
    Main Apriori algorithm.

    Returns:
        frequent_itemsets
        level_information
    """

    # ---------------------------------
    # C1: Generate 1-item candidates
    # ---------------------------------

    all_items = get_all_items(transactions)

    candidates = {
        frozenset([item])
        for item in all_items
    }

    frequent_itemsets = {}
    level_information = []

    # ---------------------------------
    # Find L1
    # ---------------------------------

    current_frequent = set()

    for candidate in candidates:

        support = calculate_support(candidate, transactions)

        if support >= min_support:
            current_frequent.add(candidate)

    frequent_itemsets[1] = current_frequent

    level_information.append({
        "level": 1,
        "candidate_count": len(candidates),
        "frequent_count": len(current_frequent)
    })

    # ---------------------------------
    # Generate L2, L3, ...
    # ---------------------------------

    k = 2

    while current_frequent and k <= max_length:

        # Generate candidates
        candidates = generate_candidates(
            current_frequent,
            k
        )

        # Apriori pruning
        pruned_candidates = set()

        for candidate in candidates:

            if not has_infrequent_subset(
                candidate,
                current_frequent
            ):
                pruned_candidates.add(candidate)

        # Support counting
        next_frequent = set()

        for candidate in pruned_candidates:

            support = calculate_support(
                candidate,
                transactions
            )

            if support >= min_support:
                next_frequent.add(candidate)

        frequent_itemsets[k] = next_frequent

        level_information.append({
            "level": k,
            "candidate_count": len(pruned_candidates),
            "frequent_count": len(next_frequent)
        })

        current_frequent = next_frequent

        k += 1

    return frequent_itemsets, level_information


def get_frequent_itemsets_with_support(
    frequent_itemsets,
    transactions
):
    """
    Convert frequent itemsets into a list
    containing itemset and support.
    """

    results = []

    for level in frequent_itemsets:

        for itemset in frequent_itemsets[level]:

            support = calculate_support(
                itemset,
                transactions
            )

            results.append({
                "itemset": itemset,
                "length": len(itemset),
                "support": support
            })

    return results