from flask import Flask, render_template, request, jsonify
import os

from src.preprocessing import prepare_transactions
from src.apriori import (
    apriori,
    get_frequent_itemsets_with_support
)
from src.rules import (
    generate_rules,
    filter_performance_rules,
    sort_rules,
    format_rules
)


app = Flask(__name__)


# ============================================================
# DATASET
# ============================================================

DATA_PATH = os.path.join(
    "data",
    "student_learning_patterns_10000.csv"
)


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():
    return render_template("index.html")


# ============================================================
# DATASET INFORMATION
# ============================================================

@app.route("/api/dataset")
def dataset_info():

    try:
        df, transactions = prepare_transactions(
            DATA_PATH
        )

        return jsonify({
            "success": True,
            "students": len(df),
            "transactions": len(transactions),
            "features": len(df.columns)
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ============================================================
# RUN APRIORI
# ============================================================

@app.route("/api/run", methods=["POST"])
def run_apriori():

    try:

        data = request.get_json()

        min_support = float(
            data.get("min_support", 0.10)
        )

        min_confidence = float(
            data.get("min_confidence", 0.60)
        )

        max_length = int(
            data.get("max_itemset_size", 3)
        )


        # ----------------------------------------------------
        # PREPROCESSING
        # ----------------------------------------------------

        df, transactions = prepare_transactions(
            DATA_PATH
        )


        # ----------------------------------------------------
        # APRIORI
        # ----------------------------------------------------

        frequent_itemsets, levels = apriori(
            transactions,
            min_support=min_support,
            max_length=max_length
        )


        # ----------------------------------------------------
        # FREQUENT ITEMSETS
        # ----------------------------------------------------

        itemset_data = (
            get_frequent_itemsets_with_support(
                frequent_itemsets,
                transactions
            )
        )

        itemsets = []

        for item in itemset_data:

            itemsets.append({
                "itemset": sorted(
                    list(item["itemset"])
                ),
                "size": item["length"],
                "support": round(
                    item["support"] * 100,
                    2
                )
            })


        # ----------------------------------------------------
        # ASSOCIATION RULES
        # ----------------------------------------------------

        rules = generate_rules(
            frequent_itemsets,
            transactions,
            min_confidence=min_confidence
        )


        # ----------------------------------------------------
        # PERFORMANCE RULES
        # ----------------------------------------------------

        performance_rules = filter_performance_rules(
            rules
        )

        performance_rules = sort_rules(
            performance_rules,
            metric="lift"
        )

        formatted_rules = format_rules(
            performance_rules
        )


        # ----------------------------------------------------
        # SUMMARY
        # ----------------------------------------------------

        total_itemsets = sum(
            len(level)
            for level in frequent_itemsets.values()
        )


        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        return jsonify({

            "success": True,

            "summary": {
                "students": len(df),
                "transactions": len(transactions),
                "frequent_itemsets": total_itemsets,
                "total_rules": len(rules),
                "performance_rules": len(
                    performance_rules
                )
            },

            "levels": levels,

            "itemsets": itemsets,

            "rules": formatted_rules

        })


    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )