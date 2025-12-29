import sys
from typing import TextIO

import pytest
from deepeval import evaluate
from deepeval.evaluate.types import TestResult
from deepeval.metrics import (
    AnswerRelevancyMetric,
    ContextualPrecisionMetric,
    ContextualRecallMetric,
    ContextualRelevancyMetric,
    FaithfulnessMetric,
    GEval,
)
from deepeval.test_case import LLMTestCaseParams


def print_evaluation_summary(test_results: list[TestResult], file: TextIO = sys.stdout):
    if not test_results:
        print("⚠️ No results found.", file=file)
        return

    print("\n📊 EVALUATION SUMMARY", file=file)
    print("-" * 60, file=file)

    for test_result in test_results:
        # 標題
        name = test_result.name.replace("test_", "").replace("_", " ").title()
        print(f"🔹 {name}", file=file)

        # 推論速度
        metadata = test_result.additional_metadata or {}
        if "inference_speed" in metadata:
            print(f"⏱️ Inference Speed: {metadata['inference_speed']:.4f}s", file=file)

        # 實際輸出
        print(f"🤖 Acutal Output:\n{test_result.actual_output}", file=file)

        # 指標
        if test_result.metrics_data:
            for metric in test_result.metrics_data:
                icon = "✅" if metric.success else "❌"
                print(f"{icon} {metric.name}: {metric.score:.4f} (>{metric.threshold})", file=file)

                if metric.reason:
                    print(f"📝 {metric.reason}", file=file)

        print("-" * 60, file=file)


@pytest.mark.deepeval
@pytest.mark.asyncio
async def test_scenario_1_simple_math(rag_tester, eval_model):
    """Scenario 1: Simple Math (Without RAG)"""

    input = "A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost?"
    test_case = await rag_tester(input)
    metrics = [
        AnswerRelevancyMetric(threshold=0.7, model=eval_model, include_reason=True),
        GEval(
            name="Math Correctness",
            criteria="Determine if the actual output contains the correct numerical answer: The ball costs $0.05.",
            evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
            model="gpt-4o",
        ),
    ]
    result = evaluate([test_case], metrics=metrics)
    with open("reports/result.log", "a+", encoding="utf-8") as f:
        print_evaluation_summary(result.test_results, file=f)


@pytest.mark.deepeval
@pytest.mark.asyncio
async def test_scenario_2_complex_calc(rag_tester, eval_model):
    """Scenario 2: Complex AI Calculation (Without RAG)"""

    input = """
    A Naive Bayes classifier is being used to classify emails as either Spam or Not Spam based on the
    presence of certain words. We observe that an email contains the words "Free" and "Win". The
    classifier has the following information:
    + Prior Probabilities:
        + P(Spam)=0.4 , P(Not Spam)=0.6
    + Likelihoods:
        + P(Free | Spam)=0.5, P(Free | Not Spam)=0.2
        + P(Win | Spam)=0.6, P(Win | Not Spam)=0.1
    Based on this information, calculate the posterior probability P(Spam | Free and Win) for the email.
    Should the classifier label this email as Spam or Not Spam?
    """
    test_case = await rag_tester(input)
    metrics = [
        AnswerRelevancyMetric(threshold=0.7, model=eval_model, include_reason=True),
        GEval(
            name="AI Calculation Correctness",
            criteria="Check if the explanation of the Naive Bayes classifier is conceptually correct and logical.",
            evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT],
            model="gpt-4o",
        ),
    ]

    result = evaluate([test_case], metrics=metrics)
    with open("reports/result.log", "a+", encoding="utf-8") as f:
        print_evaluation_summary(result.test_results, file=f)


@pytest.mark.deepeval
@pytest.mark.asyncio
async def test_scenario_3_rag_explain(file_knowledge_base, rag_tester, eval_model):
    """
    Scenario 3: RAG Explanation (With PDF File)
    """
    input = "\n".join(
        [
            "根據我的知識庫",
            "Please explain Question 1: predicting whether a customer renews a subscription.",
            "(Please answer in English)",
        ]
    )

    expected_ans = """
    # Question 1: Gini Index Calculation

    **Objective:**
    Compute the weighted Gini index for the dataset after splitting by the attribute "Payment Method".

    **Formula:**
    1. Gini Impurity for a single group: Gini(D) = 1 - Σ (p_i)^2
    2. Weighted Gini Index (Split): Gini_split = Σ (Size_i / Total_Size) * Gini(D_i)

    ---

    ### Step 1: Calculate Totals

    First, find the total number of observations for each payment method and the grand total.

    * **Credit Card:** 30 (Yes) + 10 (No) = 40
    * **Bank Transfer:** 10 (Yes) + 10 (No) = 20
    * **PayPal:** 20 (Yes) + 30 (No) = 50
    * **Grand Total (D):** 40 + 20 + 50 = 110

    ---

    ### Step 2: Calculate Gini Impurity for Each Group

    **1. Group: Credit Card**
    * P(Yes) = 30 / 40 = 0.75
    * P(No) = 10 / 40 = 0.25
    * Gini(Credit Card) = 1 - [(0.75)^2 + (0.25)^2]
    * Gini(Credit Card) = 1 - [0.5625 + 0.0625]
    * Gini(Credit Card) = 1 - 0.625 = 0.375

    **2. Group: Bank Transfer**
    * P(Yes) = 10 / 20 = 0.5
    * P(No) = 10 / 20 = 0.5
    * Gini(Bank Transfer) = 1 - [(0.5)^2 + (0.5)^2]
    * Gini(Bank Transfer) = 1 - [0.25 + 0.25]
    * Gini(Bank Transfer) = 1 - 0.5 = 0.5

    **3. Group: PayPal**
    * P(Yes) = 20 / 50 = 0.4
    * P(No) = 30 / 50 = 0.6
    * Gini(PayPal) = 1 - [(0.4)^2 + (0.6)^2]
    * Gini(PayPal) = 1 - [0.16 + 0.36]
    * Gini(PayPal) = 1 - 0.52 = 0.48

    ---

    ### Step 3: Calculate Weighted Gini Index

    We weight each group's Gini impurity by the proportion of samples in that group.

    * Weight(Credit Card) = 40 / 110
    * Weight(Bank Transfer) = 20 / 110
    * Weight(PayPal) = 50 / 110

    **Calculation:**
    Gini_split = (40/110 * 0.375) + (20/110 * 0.5) + (50/110 * 0.48)

    Let's simplify the terms:
    1.  40 * 0.375 = 15
    2.  20 * 0.5 = 10
    3.  50 * 0.48 = 24

    Summing the numerators:
    Gini_split = (15 + 10 + 24) / 110
    Gini_split = 49 / 110

    **Final Answer:**
    Gini_split ≈ 0.445
    """

    test_case = await rag_tester(input, expected_output=expected_ans)

    metrics = [
        FaithfulnessMetric(threshold=0.7, model=eval_model, include_reason=True),
        AnswerRelevancyMetric(threshold=0.7, model=eval_model, include_reason=True),
        ContextualRelevancyMetric(threshold=0.5, model=eval_model, include_reason=True),
        ContextualRecallMetric(threshold=0.5, model=eval_model, include_reason=True),
        ContextualPrecisionMetric(threshold=0.5, model=eval_model, include_reason=True),
    ]

    result = evaluate([test_case], metrics=metrics)

    with open("reports/result.log", "a+", encoding="utf-8") as f:
        print_evaluation_summary(result.test_results, file=f)


@pytest.mark.deepeval
@pytest.mark.asyncio
async def test_scenario_4_ambiguous(file_knowledge_base, rag_tester, eval_model):
    """
    Scenario 4: Ambiguous Question (With PDF File)
    """
    input = "\n".join(
        [
            "根據我的知識庫",
            "Please explain Question 1.",
            "(Please answer in English)",
        ]
    )

    test_case = await rag_tester(input)

    metrics = [
        FaithfulnessMetric(threshold=0.7, model=eval_model, include_reason=True),
        AnswerRelevancyMetric(threshold=0.7, model=eval_model, include_reason=True),
        ContextualRelevancyMetric(threshold=0.5, model=eval_model, include_reason=True),
    ]

    result = evaluate([test_case], metrics=metrics)

    with open("reports/result.log", "a+", encoding="utf-8") as f:
        print_evaluation_summary(result.test_results, file=f)
