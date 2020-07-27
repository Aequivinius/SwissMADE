Please find attached the code lists to identify the different ADEs using hospital discharge summaries coded sith ICD-10-GM and CHOP.

 

You can also find below decision rules to identify the ADEs using the lists:

- To identify haemorrhages (all) associated with antithrombotics (ATTs), use the Hemo and ADE_Hemo lists: at least one code from each list coded in the discharge summary).

- To identify traumatic haemorrhages associated with ATTs, use the Hemo_Traum and ADE_Hemo lists: at least one diagnostic code from each list coded in the discharge summary)

- To identify severe bleeding, whether traumatic or not, associated with ATTs:

o first, identify hospital stays (discharge summaries) with severe haemorrhage: [at least one code from the Sev_Hemo list] or [at least one code from the Hemo list and (mode of discharge = death (óvariable 1.5.V02 Discharge decision = 5) or at least one treatment code from the Transfu list)]

o then, match with the ADE_Hemo list: among above stays, select those with at least one diagnosis in the ADE_Hemo list

- To identify deep vein thrombosis of the lower limbs associated with ATTs, use DVT and ADE_VTE lists: at least one diagnostic code from each list coded in the stay

- To identify pulmonary embolisms associated with ATTs, use PE and ADE_VTE: at least one diagnostic code from each list coded in the stay

- To identify arterial thromboembolic events associated with ATTs, use ATE and ADE_ATE lists: at least one diagnostic code from each coded list in the stay

- To identify acute myocardial infarction (AMI) associated with ATTs, use AMI and ADE_ATE lists: at least one diagnostic code from each coded list in the stay

- To identify ischemic stroke associated with ATTs, use stroke and ADE_ATE lists: at least one diagnostic code from each coded list in the stay

>>> ADE_VTE and ADE_ATE lists are the same!

This method should be able to identify ADEs associated with ATTs (even though there may be false negatives) and thus obtain a sample of "positive" stays.

For "negative" stays, we would need stays that do not have any of the codes from the different lists (diagnosis or treatment).