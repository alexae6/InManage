import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
import sys
import django
django.setup()
import pandas as pd
from base.models import Patient


sys.path.append("C:/InManage/venv/Scripts/project")


def run():

    patient_df = pd.read_csv("pat_patientfile1.csv")  
    patient_array = patient_df.to_dict(orient="records")
    for entry in patient_array: 
        patient = Patient(
                    patientname = entry["Patient Name"],
                    age = entry["Age"],
                    dob = entry["DOB"],
                    sex = entry["Sex"],
                    adress1 = entry["Address Line 1"],
                    adress2 = entry["Address Line 2"],
                    workphone = entry["Work Phone"],
                    city = entry["City"],
                    st = entry["ST"],
                    zip = entry["Zip"],
                    country = entry["Country"],
                    county =entry["County"],
                    homephone = entry["Home Phone"],
                    primaryinsurance = entry["Primary Insurance"],
                    insurancename1 = entry["InsuranceName1"],
                    ID1 = entry["ID1"],
                    GP1 = entry["GP1"],
                    EFF1 = entry["EFF1"],
                    EXP1 = entry["EXP1"],
                    secondaryinsurance = entry["Secondary Insurance"],
                    insurancename2 = entry["InsuranceName2"],
                    ID2 = entry["ID2"],
                    GP2 = entry["GP2"],
                    EFF2 = entry["EFF2"],
                    EXP2 = entry["EXP2"],
                    tertiaryinsurance = entry["Tertiary Insurance"],
                    insurancename3 = entry["Insurance Name"],
                    ID3 = entry["ID #"],
                    GP3 = entry["GP #"],
                    EFF3 = entry["EFF"],
                    EXP3 = entry["EXP"],
                    referringmd = entry["Referring MD:"],
                    ReferringHospital = entry["Referring Hospital"],
                    phone = entry["Phone:"],
                    fax = entry["Fax:"],
                    NearestRelativeName = entry["Nearest Relative Name"],
                    NearestRelativeRelation = entry["Nearest Relative Relation"],
                    NearestRelativeAddress = entry["Nearest Relative Address"],
                    NearestRelativeHomePhone = entry["Nearest Relative Home Phone"],
                    NearestRelativeCity = entry["Nearest Relative City"],
                    NearestRelativeST = entry["Nearest Relative ST"],
                    NearestRelativeZip = entry["Nearest Relative Zip"],
                    NearestRelativeWorkPhone = entry["Nearest Relative Work Phone"],
                    NearestRelativeWorkPhoneExt = entry["Nearest Relative Work Phone Ext"],  
                    Status = entry["Status"],
                    Diagnosis = entry["Diagnosis"],
                    CMS = entry["CMS Diagnosis"],
                    Rejectiondis = entry["Rejection Disposition"],
                    ReferralDate = entry["Referral Date"],
                    Assignee = entry["Assignee"],
                    PresentHistory = entry["History of Present Illness"],
                    PastHistory = entry["Past Medical History"],
                    Orientation = entry["Orientation"],
                    Concentration = entry["Concentration"],
                    Memory = entry["Memory"],
                    Langauge = entry["Language"],
                    muskuloskeletal = entry["Muskuloskeletal"],
                    ImpressionAndPlan = entry["Impression and Plan"],
                    impairments = entry["Impairments"],
                    TreatingDiagnosis = entry["Treating Diagnosis"],
                    RehabPotential = entry["Rehab Potential"],
                    AssessmentAndRationale = entry["Assessment/Rationale"],
                    DispositionRecommendations = entry["Disposition Recommendations"],
                    frequency = entry["Frequency"],
                    duration = entry["Duration"],
                    DurationUnit = entry["Duration Unit"],
                    TPIPlanned = entry["Therapeutic Procedures Interventions Planned"],
                    caregiver = entry["Pt/Caregiver Involved in Goal Setting & Tx Plan"],
                    MedicalDiagnosis = entry["Medical Diagnosis"],
                    OnsetDate = entry["Onset Date"],
                    PatientPrecautions = entry["Patient Precautions"],
                    LeftUE = entry["Left UE"],
                    RightUE = entry["Right UE"],
                    LeftLE = entry["Left LE"],
                    RightLE = entry["Right LE"],
                    transfers = entry["Tranfers"],
                    BedMobility = entry["Bed Mobility"],
                    ADLs = entry["ADL's"],
                    ambulation = entry["Ambulation"],
                    auditory = entry["Auditory"],
                    vision = entry["Vision"],
                    SubjectiveInformation = entry["Subjective Information"],
                    LivingSituation = entry["Living Situation 1"],
                    CognitionLOC = entry["Cognition Level of Consciousness"],
                    CognitionOrientation = entry["Cognition Orientation"],
                    SupineToSit = entry["Supine to Sit"],
                    SitToStand = entry["Sit to Stand"],
                    StandToSit = entry["Stand to Sit"],
                    BedToChair = entry["Bed to Chair"],
                    gait = entry["Gait Assessment Comments"]                    
        )
        patient.save()
    print("Saved all")
    return
if __name__ ==  "__main__":
    run()