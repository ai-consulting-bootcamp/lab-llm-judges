# 5 Prompts & a Judge

## Evaluation Prompt 1: Accurate Hospital Course Summary

Prompt:
You are a clinical summarization assistant. Using the patient record below, write a concise hospital-course summary for the patient's next treating physician. Include the reason for admission, key diagnoses, major investigations, treatments and procedures, significant clinical events, medication changes, and discharge/follow-up information. Do not add information that is not supported by the record.

Patient record:
A 67-year-old man with hypertension and type 2 diabetes was admitted with three days of worsening shortness of breath and fever. Chest X-ray showed right lower-lobe pneumonia. He was treated with IV ceftriaxone and azithromycin and supplemental oxygen. Blood cultures were negative. His oxygen requirement resolved by hospital day 3. He was transitioned to oral amoxicillin-clavulanate and discharged home on hospital day 4. Follow-up with his primary-care physician was recommended within one week.

Ground Truth:
[x] Yes - The summary should accurately include pneumonia as the diagnosis, the admission symptoms, key investigation, antibiotics, oxygen treatment, clinical improvement, transition to oral antibiotics, discharge, and follow-up. It must not introduce unsupported diagnoses or treatments.

[ ] No - Explain why there's no single correct answer.

Verification Method:
[x] Rule-based: Check that critical facts from the record are present and that the summary contains no contradictory or unsupported facts.

[x] Human evaluation: A clinician assesses factual accuracy, completeness, clinical usefulness, and whether any important information was omitted.

[ ] LLM-as-judge: Describe what the judge would evaluate.

Primary Failure Mode:
Omission or distortion of clinically important information.

Why this prompt matters:
This represents the core production use case: turning a patient's detailed record into a concise summary without losing information needed for safe ongoing care.

## Evaluation Prompt 2: Critical Information Completeness

Prompt:
Summarize the following patient's hospital course for a physician taking over the patient's care. Prioritize information that could affect immediate clinical decisions.

Patient record:
A 74-year-old woman was admitted after a fall. CT head showed no acute intracranial hemorrhage. Imaging revealed a left femoral neck fracture. She underwent surgical fixation on hospital day 2. Her home warfarin was held on admission because of an elevated INR of 4.2. Vitamin K was administered. Her INR decreased to 1.4 before surgery. Warfarin was restarted after surgery. She developed postoperative acute blood-loss anemia with hemoglobin falling from 11.8 g/dL to 7.9 g/dL and received one unit of packed red blood cells. At discharge, hemoglobin was 9.1 g/dL.

Ground Truth:
[x] Yes - The summary should preserve the femoral neck fracture and surgery, the elevated INR and warfarin management, postoperative anemia, transfusion, and discharge hemoglobin. These are clinically important details.

[ ] No - Explain why there's no single correct answer.

Verification Method:
[x] Rule-based: Check specifically for all predefined critical facts: fracture, surgery, warfarin interruption/restart, INR values, vitamin K, anemia, transfusion, and discharge hemoglobin.

[x] Human evaluation: Clinicians assess whether omission of any information could affect subsequent patient care.

[ ] LLM-as-judge: Describe what the judge would evaluate.

Primary Failure Mode:
A fluent but incomplete summary that omits clinically critical information.

Why this prompt matters:
A major risk of medical summarization is that a model can produce a concise and apparently high-quality summary while silently removing information that is essential for safe treatment decisions.

## Evaluation Prompt 3: Medical Terminology and Medication Accuracy

Prompt:
Create a clinically accurate summary of the following record. Preserve medical terminology and distinguish between diagnoses, symptoms, investigations, medications, and procedures. Preserve medication names, doses, routes, and frequencies exactly when provided.

Patient record:
A 52-year-old woman with atrial fibrillation was admitted for rapid ventricular response. ECG demonstrated atrial fibrillation with a ventricular rate of 148 bpm. She received metoprolol tartrate 25 mg orally every 6 hours for rate control. Her heart rate subsequently decreased to 82 bpm. She was discharged on metoprolol tartrate 25 mg twice daily and apixaban 5 mg twice daily.

Ground Truth:
[x] Yes - The summary should correctly identify atrial fibrillation with rapid ventricular response, distinguish the ECG finding from the diagnosis, and accurately preserve the medication names, doses, routes/frequencies where relevant. It should not substitute vague terms such as "heart medication" for the actual medications.

[ ] No - Explain why there's no single correct answer.

Verification Method:
[x] Rule-based: Compare diagnoses, medication names, doses, routes, frequencies, and clinical measurements against the source.

[x] Human evaluation: A clinician evaluates whether the terminology and medication information are medically accurate.

[ ] LLM-as-judge: Describe what the judge would evaluate.

Primary Failure Mode:
Incorrect medical terminology or medication information, particularly medication name, dose, or frequency errors.

Why this prompt matters:
Medical terminology is not merely stylistic in this scenario. Changing or simplifying terminology incorrectly can alter the clinical meaning and potentially lead to unsafe treatment decisions.

## Evaluation Prompt 4: Detecting Contradictions and Hallucinations

Prompt:
Summarize this patient record. Only state facts that are supported by the record. If information is uncertain or conflicting, explicitly indicate the uncertainty rather than resolving it by guessing.

Patient record:
A 45-year-old man presented with abdominal pain. CT abdomen showed acute appendicitis without perforation or abscess. He underwent laparoscopic appendectomy. The operative report documented an uncomplicated procedure. He had no documented drug allergies. He was discharged the following day with instructions to use acetaminophen as needed for pain.

Ground Truth:
[x] Yes - The summary should state that the patient had acute appendicitis without perforation or abscess and underwent an uncomplicated laparoscopic appendectomy. It should not claim that the appendix had ruptured, that an abscess was present, or that the patient had a penicillin allergy.

[ ] No - Explain why there's no single correct answer.

Verification Method:
[x] Rule-based: Identify whether the output contains unsupported diagnoses, complications, allergies, procedures, or other facts not present in the source.

[x] Human evaluation: A clinician checks whether every clinically meaningful assertion is supported by the record.

[x] LLM-as-judge: Evaluate factual grounding of each major clinical claim against the source record.

Primary Failure Mode:
Hallucination—introducing plausible but unsupported clinical information.

Why this prompt matters:
Medical records contain many details that are easy for an LLM to "fill in" based on typical clinical patterns. Preventing fabricated diagnoses, complications, allergies, or treatments is essential for patient safety.

## Evaluation Prompt 5: High-Risk Clinical Edge Case

Prompt:
Produce a concise discharge summary from the following record. Prioritize information that could cause patient harm if omitted or incorrectly summarized. Do not infer medication changes that are not explicitly documented.

Patient record:
An 81-year-old patient with chronic kidney disease and heart failure was admitted with worsening lower-extremity edema. Creatinine increased from a baseline of 1.4 mg/dL to 2.1 mg/dL during admission. The patient received IV furosemide with improvement in edema. Because of worsening renal function, the ACE inhibitor was held during hospitalization. At discharge, creatinine had improved to 1.7 mg/dL. The discharge medication list explicitly states that the ACE inhibitor should remain held pending outpatient renal function testing. Follow-up blood testing was recommended within 3 days.

Ground Truth:
[x] Yes - The summary must preserve the patient's CKD and heart failure, worsening renal function, creatinine values, IV diuretic treatment, the fact that the ACE inhibitor was held, and critically, that it should remain held at discharge pending renal testing and that testing is required within 3 days.

[ ] No - Explain why there's no single correct answer.

Verification Method:
[x] Rule-based: Check for the diagnosis, creatinine changes, treatment, medication hold, discharge medication instruction, and follow-up testing.

[x] Human evaluation: A clinician assesses whether the summary preserves information necessary for safe medication management.

[x] LLM-as-judge: Evaluate whether the summary correctly identifies safety-critical information and whether any omission or alteration could lead to patient harm.

Primary Failure Mode:
Failure to preserve a safety-critical medication instruction.

Why this prompt matters:
This is a high-risk edge case where a seemingly minor omission can have significant clinical consequences. It tests whether the model prioritizes information based on clinical importance, rather than simply producing a generally accurate summary.

## LLM Judge

Task Description:
Evaluate an AI-generated discharge summary of a patient's medical record. The original task is to produce a concise, clinically accurate summary that preserves information that could affect patient safety or ongoing clinical decisions. The summary must not introduce information that is unsupported by the source record.

Source patient record:
"An 81-year-old patient with chronic kidney disease and heart failure was admitted with worsening lower-extremity edema. Creatinine increased from a baseline of 1.4 mg/dL to 2.1 mg/dL during admission. The patient received IV furosemide with improvement in edema. Because of worsening renal function, the ACE inhibitor was held during hospitalization. At discharge, creatinine had improved to 1.7 mg/dL. The discharge medication list explicitly states that the ACE inhibitor should remain held pending outpatient renal function testing. Follow-up blood testing was recommended within 3 days."

Evaluation Criteria:
1. Factual Accuracy: The summary must accurately represent the source record. It must not invent diagnoses, treatments, medication changes, test results, or clinical events, and must not change clinically meaningful facts or numbers.

2. Critical Information Completeness: The summary should preserve the clinically important information from the source, particularly the chronic kidney disease, heart failure, renal-function changes, treatment with IV furosemide, ACE inhibitor being held, discharge creatinine, instruction to continue holding the ACE inhibitor, and follow-up blood testing within 3 days.

3. Clinical Safety: The summary must preserve safety-critical information. Particular importance should be given to medication instructions, abnormal laboratory results, diagnoses, and follow-up requirements. An omission or alteration that could reasonably lead to inappropriate clinical management should be considered a serious failure.

Reasoning Steps:
Step 1: Compare the generated summary against the source record and identify whether each major clinical fact is accurately represented.

Step 2: Identify any important omissions, giving greater weight to medication instructions, abnormal results, diagnoses, and follow-up requirements than to minor descriptive details.

Step 3: Identify unsupported or contradictory claims and determine whether any error or omission could affect clinical decision-making or patient safety.

Step 4: Assign a score from 1 to 5 based on the overall clinical quality of the summary. Do not reward fluency or conciseness when they come at the expense of factual accuracy, completeness, or safety.

Scoring:
5 = Excellent: Accurate, complete, clinically safe, with no meaningful errors or omissions.
4 = Good: Minor omission or wording issue that does not affect clinical interpretation or safety.
3 = Acceptable with concerns: Some clinically relevant information is missing or imprecise, but the summary remains broadly usable with clinician review.
2 = Poor: Important information is missing or incorrectly represented, creating a meaningful risk of misunderstanding.
1 = Unsafe: Contains major factual errors, hallucinations, or omission of safety-critical information that could plausibly lead to harmful clinical decisions.

Output Format:
{
  "score": [1-5],
  "reasoning": "[Brief explanation of the score, citing the most important strengths, omissions, or errors]",
  "criteria_met": {
    "criterion_1": true/false,
    "criterion_2": true/false,
    "criterion_3": true/false
  }
}

### Bias Analysis

The judge could have a style bias, preferring summaries that closely resemble the wording or structure of the source record rather than recognizing that clinically equivalent wording is acceptable. It could also favor concise summaries and accidentally penalize a slightly longer summary that is actually more complete. Language bias is another concern: a judge may rate medically conventional English terminology more highly than an equally accurate expression used by clinicians in another linguistic or cultural context.

There is also a domain-assumption bias. The judge may assume that certain clinical actions are standard practice and therefore accept an inference that is not actually supported by the record. For example, it might infer that a medication was permanently discontinued when the record only says it was held. The judge should therefore evaluate whether statements are supported by the provided record rather than whether they seem medically plausible.

### Calribration Strategy

I would calibrate the judge using a set of reference summaries covering the full scoring range. For example, I would provide one excellent summary containing all critical information, one good summary with a minor omission, one borderline summary missing several non-critical details, one poor summary omitting the ACE-inhibitor discharge instruction, and one unsafe summary that incorrectly states the ACE inhibitor was restarted. Each example would have a clinician-assigned score and explanation.

I would also deliberately include edge cases where wording differs substantially from the source but the meaning is correct, so the judge learns not to penalize paraphrasing. Conversely, I would include examples where a fluent summary contains a subtle but clinically dangerous error. If the judge consistently scores too strictly or leniently compared with clinician ratings, I would adjust the evaluation criteria and scoring examples rather than simply changing the passing threshold. Periodic comparison against human clinician judgments should be used to monitor calibration over time.