// ============================================================
// ELEMENTS
// ============================================================

const supportSlider =
    document.getElementById("support");

const confidenceSlider =
    document.getElementById("confidence");

const supportValue =
    document.getElementById("supportValue");

const confidenceValue =
    document.getElementById("confidenceValue");

const maxItemset =
    document.getElementById("maxItemset");

const runButton =
    document.getElementById("runButton");

const loading =
    document.getElementById("loading");


// ============================================================
// SLIDER UPDATES
// ============================================================

supportSlider.addEventListener(
    "input",
    () => {

        supportValue.textContent =
            supportSlider.value + "%";

    }
);


confidenceSlider.addEventListener(
    "input",
    () => {

        confidenceValue.textContent =
            confidenceSlider.value + "%";

    }
);


// ============================================================
// RUN
// ============================================================

runButton.addEventListener(
    "click",
    runApriori
);


async function runApriori() {

    runButton.disabled = true;

    loading.classList.remove("hidden");


    const minSupport =
        Number(supportSlider.value) / 100;

    const minConfidence =
        Number(confidenceSlider.value) / 100;

    const maxSize =
        Number(maxItemset.value);


    try {

        const response = await fetch(
            "/api/run",
            {

                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    min_support:
                        minSupport,

                    min_confidence:
                        minConfidence,

                    max_itemset_size:
                        maxSize

                })

            }
        );


        const result =
            await response.json();


        if (!result.success) {

            throw new Error(
                result.error
            );

        }


        displaySummary(
            result.summary
        );


        displayFeaturedRule(
            result.rules
        );


        displayRules(
            result.rules
        );


        displayItemsets(
            result.itemsets
        );


        document
            .getElementById("results")
            .classList.remove("hidden");

    }


    catch (error) {

        alert(
            "Unable to discover patterns.\n\n" +
            error.message
        );

    }


    finally {

        runButton.disabled = false;

        loading.classList.add(
            "hidden"
        );

    }

}


// ============================================================
// SUMMARY
// ============================================================

function displaySummary(summary) {

    document.getElementById(
        "students"
    ).textContent =
        summary.students.toLocaleString();


    document.getElementById(
        "transactions"
    ).textContent =
        summary.transactions.toLocaleString();


    document.getElementById(
        "itemsetCount"
    ).textContent =
        summary.frequent_itemsets;


    document.getElementById(
        "ruleCount"
    ).textContent =
        summary.total_rules;

}


// ============================================================
// FEATURED RULE
// ============================================================

function displayFeaturedRule(rules) {

    if (!rules || rules.length === 0) {

        document.getElementById(
            "featuredAntecedent"
        ).textContent =
            "No pattern found";


        document.getElementById(
            "featuredConsequent"
        ).textContent =
            "Try lowering the thresholds";


        document.getElementById(
            "featuredSupport"
        ).textContent =
            "-";


        document.getElementById(
            "featuredConfidence"
        ).textContent =
            "-";


        document.getElementById(
            "featuredLift"
        ).textContent =
            "-";

        return;
    }


    const rule = rules[0];


    const parts =
        splitRule(rule.Rule);


    document.getElementById(
        "featuredAntecedent"
    ).textContent =
        parts.antecedent;


    document.getElementById(
        "featuredConsequent"
    ).textContent =
        parts.consequent;


    document.getElementById(
        "featuredSupport"
    ).textContent =
        rule.Support + "%";


    document.getElementById(
        "featuredConfidence"
    ).textContent =
        rule.Confidence + "%";


    document.getElementById(
        "featuredLift"
    ).textContent =
        rule.Lift;

}


// ============================================================
// SPLIT RULE
// ============================================================

function splitRule(ruleText) {

    const parts =
        ruleText.split(" → ");


    return {

        antecedent:
            parts[0] || "",

        consequent:
            parts[1] || ""

    };

}


// ============================================================
// ASSOCIATION RULE TABLE
// ============================================================

function displayRules(rules) {

    const table =
        document.getElementById(
            "ruleTable"
        );


    table.innerHTML = "";


    if (!rules || rules.length === 0) {

        table.innerHTML = `

            <tr>

                <td colspan="5">

                    No learning-performance
                    associations were found.

                    Try lowering minimum confidence.

                </td>

            </tr>

        `;

        return;
    }


    const visibleRules =
        rules.slice(0, 50);


    visibleRules.forEach(
        (rule, index) => {

            const parts =
                splitRule(rule.Rule);


            const row =
                document.createElement("tr");


            row.innerHTML = `

                <td>
                    ${parts.antecedent}
                </td>

                <td>
                    ${parts.consequent}
                </td>

                <td>
                    ${rule.Support}%
                </td>

                <td>
                    ${rule.Confidence}%
                </td>

                <td>
                    ${rule.Lift}
                </td>

            `;


            row.addEventListener(
                "click",
                () => {

                    showRuleExplanation(
                        rule
                    );

                }
            );


            table.appendChild(row);

        }
    );

}


// ============================================================
// FREQUENT ITEMSETS
// ============================================================

function displayItemsets(itemsets) {

    const table =
        document.getElementById(
            "itemsetTable"
        );


    table.innerHTML = "";


    if (!itemsets ||
        itemsets.length === 0) {

        table.innerHTML = `

            <tr>

                <td colspan="3">

                    No frequent patterns found.

                </td>

            </tr>

        `;

        return;
    }


    const visible =
        itemsets.slice(0, 50);


    visible.forEach(
        item => {

            const row =
                document.createElement("tr");


            row.innerHTML = `

                <td>
                    ${item.itemset.join(" + ")}
                </td>

                <td>
                    ${item.size}
                </td>

                <td>
                    ${item.support}%
                </td>

            `;


            table.appendChild(row);

        }
    );

}


// ============================================================
// RULE EXPLANATION
// ============================================================

function showRuleExplanation(rule) {

    const section =
        document.getElementById(
            "explanationSection"
        );


    const container =
        document.getElementById(
            "explanation"
        );


    const parts =
        splitRule(rule.Rule);


    const liftMeaning =
        rule.Lift > 1
            ? "This indicates a positive association."
            : rule.Lift === 1
                ? "This indicates little association beyond the baseline."
                : "This indicates a weaker-than-baseline association.";


    container.innerHTML = `

        <h3>
            ${parts.antecedent}
            → 
            ${parts.consequent}
        </h3>


        <p>

            In this dataset, students showing
            <strong>${parts.antecedent}</strong>
            are associated with
            <strong>${parts.consequent}</strong>.

            The pattern appears in
            <strong>${rule.Support}%</strong>
            of all learning records.

        </p>


        <div class="explanation-grid">

            <div class="explanation-metric">

                <span>
                    Support
                </span>

                <strong>
                    ${rule.Support}%
                </strong>

            </div>


            <div class="explanation-metric">

                <span>
                    Confidence
                </span>

                <strong>
                    ${rule.Confidence}%
                </strong>

            </div>


            <div class="explanation-metric">

                <span>
                    Lift
                </span>

                <strong>
                    ${rule.Lift}
                </strong>

            </div>

        </div>


        <p style="margin-top:20px;">

            <strong>Lift interpretation:</strong>
            ${liftMeaning}

        </p>

    `;


    section.classList.remove(
        "hidden"
    );


    section.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });

}