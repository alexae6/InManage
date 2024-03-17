
import re 
import csv
import sys
#import sqlite3 as sq



def checkcms(text):
    cmsnames = [
        ["hemiplegia"],
        ['hemiparesis'],
        ['monoplegia'],
        ['intracerebral hemorrhage', r'non[- ]*traumatic'],
        ['subarachnoid hemorrhage'],
        ['subdural hemorrhage'],
        ['cerebral infarction'],
        [r'(stenosis|occlusion)[ of ]*precerbral arter[iesy]*', r'(embolism|thrombosis|obstruction of basilar)'],
        [r'occlusion[ of ]*cerebral arter[iesy]*', r'(embolism|thrombosis)'],
        ['hypertensive encephalopathy'],
        ['cerebral arteritis'],
        [r'late effect cva', r'(hemiplegia|monoplegia|paralysis)'],
        [r'(quadriplegia|paraplegia|diplegia)'],
        ['cauda equina syndrome'],
        [r'(spondylosis|stenosis)', 'with myelopathy'],
        ['intervertebral disc disorder', 'with myelopathy'],
        [r'fracture[ of ]*vertebral column', 'spinal cord injury'],
        [r'human t[- ]*cell lymphotrophic virus type (1|l|I|i|one)'],
        [r'(malignant neoplasms|tumors)', r'(vertebral column|spinal cord|causa equina|spinal meninges)'], #vertebral column not sacrum or coccyx
        [r'(benign neoplasms|tumors)', r'(spinal cord|cauda equina|meninges)'],
        ['encephalitis', 'viral disease'],
        ['intraspinal abscess'],
        [r'(syringomyelia|syringobulbia)'],
        ['acute poliomyelitis', r'(paralysis|paralyzed)'],
        ['late effect spinal cord injury'],
        ['polyarteritis', r'(disseminated necrotizing periarteritis|necrotizing angitis)'],
        ['lupus', 'sle'],
        ['dwarfism'],
        [r'(myelodysplasia|spinal cord anomoly)'],
        ['spinal muscular atrophy'],
        ['infantile cerebral palsy'],
        ['hereditary', 'idiopathic', 'peripheral neuropathy'],
        ['spina bifida'],
        ['hereditary spastic paraplegia'],
        ['amputation', r'((above|below)[ the ]*(elbow|knee)|foot)'],
        ['disarticulation', r'(shoulder|hip|ankle)'],
        ['stump complication'],
        [r'(fitting|adjustment)[ a-zA-Z]*prosthetic (arm|leg)'],
        ['pelvic factures'],
        [r'fracture[ A-Za-z]*both (upper limbs|arms)'],
        [r'(fracture|major multiple trauma)', r'(upper|lower) (limb|arm|leg)', r'(rib|sternum)'],
        [r'(fracture|major multiple trauma)', r'both (lower limb|leg)'],
        [r'(fracture|major multiple trauma)', r'(upper limb|arm)', r'(lower limb|leg)'],
        ['pneumothorax', r'fracture[A-Za-z]*[ ]*[A-Za-z]*[ ]*[A-Za-z]* femur'],
        [r'(two|2) fractures', r'(tbi|sci)'],
        [r'(2|two) amputations', 'sci'],
        ['burn', 'late effect'],
        ['burn', r'(3rd|third) degree'],
        ['burn', r'[10-100](%|[ ]*percent)[of ]*(body|surface)'],
        [r'(2nd|second) degree burns', r'(lower limb|leg)'],
        [r'acetabulum fracture'],
        [r'intracapsular fracture'],
        [r'epiphysis fracture'],
        [r'fracture', 'head of femur'],
        [r'subcapital fracture'],
        [r'trochanteric', 'fracture'],
        ['neck of femur', 'fracture'],
        ['meningitis', 'brain'],
        ['brain abscess'],
        ['intracranial abcess'],
        ['encephalitis'],
        ['meningoencephalitis'],
        ['encephalopathies', 'metabolic', r'(bacteria|infection|virus)'],
        ['encephalopathies', 'hepatic', r'(cirrhosis|elevated ltf|elevated ammonia|elevated inr)'], #not on coumadin
        ['encephalopathies', 'alcoholic', r'(chronic etoh abuse|wernicke-korsako)'],
        ['encephalopathies', 'anoxic', r'(brain deprived of (o2|oxygen)|hypoxic resp[iratory]* fail|cardiac arrest|low (o2|oxygen))'],
        ['encephalopathies', 'toxic', r'drug[ -]*induced'],
        ['encephalopathies', 'uremic', r'esrd'],
        ['neoplasms', 'malignant', 'brain'],
        ['hydrocephalus', 'normal', 'pressure'],
        ['cerebral cyst'],
        [r'traumatic (subdural|subarachnoid)', r'(hemorrhage|hematoma)'],
        [r'post[ -]*concussion syndrome'],
        [r'post[- ]*traumatic brain syndrome'],
        [r'anoxic brain damage'],
        [r'closed head injury'],
        [r'locked in[\'" ]*state'],
        [r'fracture', r'(vault|base)[ of]*skull', r'(frontal|parietal|occiput|orbital roof|sphenoid|temporal|sinus[ -]*ethmoid|frontal|fossa)'],
        [r'cerebral laceration', r'contusion', r'(cortex|cerebellum|brain stem)'],
        [r'intracranial', 'cerebral laceration', 'contusion'],
        [r'bilateral (hip|knee) replacement'], #must be immediately preceding
        [r'(knee|hip) replace', r'(BMI[: of]*[50-200]|Age[ :]*[85-200]'],
        [r'(post[ -]*polio|poliomyelitis'],
        ['parkinson'],
        ["fredreich's ataxia"],
        [r'[: ]+als[ ]+'],
        [r'primary lateral scelosis'],
        [r'motor neuron', 'adult'],
        ['progressive muscular atrophy'],
        ['bulbar palsy'],
        ['multiple sclerosis'],
        [r'(demyelinating|demyelinate)', 'cns'],
        ['brachial plexus lesion'],
        ['lumbosacral lesion'],
        ['cervical lesion'],
        ['thoracic lesion'],
        [r'neuropath(y|ies)', 
        r'(hereditary motor|critical illness|drug[ ]*induced|toxic|radiation[ -]*induced|chemo[ -]*induced|alcohol[ -]*induced|idiopathic progressive peripheral)'],
        ['acute infective polyneuritis'],
        ['myasthenia gravis'],
        [r'muscular dystroph(y|ies)'],
        [r'myopath(y|ies)', r'(critical|ICU|hx vent|proximal weakness|organ failure|steroid[ -]*induces|chemo[ -]*induced|thyroid[ -]*induced'],
        ['dermatomyositis'],
        ['polymyositis']


        #post-concussion syndrome



    ]

    text2 = text.lower()
    cms = False
    diagnosis = []
    for i in cmsnames:
        checker = True
        diag = []
        for j in i:
            try:
                designator = re.search(j, text2).group(0)
            except:
                designator = ""
            if (designator == ""):
                checker = False
            else:
                diag.append(designator)
        if (checker == True):
            cms = True
            diagnosis.append(' '.join(diag))
    if len(diagnosis) != 0:
        diagnosis =', '.join(diagnosis)
    else:
        diagnosis = ''
    return cms, diagnosis

def parser(text, filename):
    #minimize errors
    text = text.replace(';', ':')
    text = re.sub(r"[Ã¯Â¿Â½]", "", text)

    #dictionary of regular expressions
    regex = {
        #Demographics and Insurance
        "Patient Name": r'Patient Name:[ ]+[A-Za-z]+[, ]+[A-Za-z]+[ ]*[A-Z]*',
        "Insurances": r'[A-za-z ]+Insurance:[ ]+[A-za-z0-9 ]+\n',
        "Insurance Info": r'Insurance Name:[A-Za-z0-9 \t]+ID #:[ ]+[0-9A-Za-z]+[ \t]*GP #:[ ]*[0-9]*[ \t]*E[A-Z]*:[ ]*[/0-9]*[ \t]*EXP:[ ]*[/0-9]*\n',
        "Age": r'Age:[ ]*[0-9]+',
        'DOB': r'DOB:[ ]*[/0-9]+',
        "Sex": r'(Sex:|Patient Demographics)[ ]*[A-Za-z]+',
        "Referring MD": r'Referring MD:[ ]*[A-Za-z]+[, ]+[A-Za-z]+[ ]*[A-Za-z]*[ \t]*Phone:[ ]*[-0-9]*[ \t]*Fax:[ ]*[-0-9]*',
        #Patient Address
        "Address Line 1": r'(PATIENT INFORMATION.*[\n]*Address Line 1:|Patient Address\n)[ ]*[0-9]+[ ]*[A-Za-z]+[ ]+[0-9A-Za-z]*[ ]*[A-Za-z0-9]*',
        "Address Line 2": r'(PATIENT INFORMATION[\S\s]*Address Line 2:|Patient Address\n)[ ]*[0-9]+[ ]*[A-Za-z]+[ ]+[0-9A-Za-z]*[ ]*[A-Za-z0-9]*',
        "Work Phone": r'PATIENT INFORMATION[\S\s]*Employment Status:[ ]*[A-Za-z0-9 \t]*Work Phone:[ \t]*[0-9 ()-]*',
        "City/State/Country": r'PATIENT INFORMATION[\S\s]*City:[A-Za-z0-9 \t]*ST:[ \tA-Z]*Zip:[ \t0-9]*Country:[\t ]*[A-Za-z]*[ ]*[A-Za-z]*[ ]*(?=Religion)',
        "County": r"PATIENT INFORMATION[\S\s]*County:[\S\s]*?(?<=Home Phone)",
        "Home Phone": r"PATIENT INFORMATION[\S\s]*Home Phone:[ ]*[ 0-9()-]*(?=Church)",
        "Nearest Relative Name": r'NEAREST RELATIVE[\S\s]*Name:[ ]*[A-Za-z]*, [A-Za-z]*[ ]*[A-Za-z]*',
        "Nearest Relative Address": r'NEAREST RELATIVE[\S\s]*Address:[\S\s]*?(?<=Home Phone)',
        "Nearest Relative Home Phone":r'NEAREST RELATIVE[\S\s]*Home Phone:[ ]*[ 0-9()-]*',
        "Nearest Relative Relation":r'NEAREST RELATIVE[\S\s]*Relation:[ ]*[A-Za-z\']*',
        "Nearest Relative City":r'NEAREST RELATIVE[\S\s]*?City:[ ]*[A-Za-z0-9]+[ ]*[A-Za-z0-9]*[ ]*(?=ST:)',
        "Nearest Relative ST":r'NEAREST RELATIVE[\S\s]*?ST:[ ]*[A-Za-z]{0,4}',
        "Nearest Relative Zip":r'NEAREST RELATIVE[\S\s]*?Zip:[ ]*[0-9]+',
        "Nearest Relative Work Phone":r'NEAREST RELATIVE[\S\s]*?Work Phone:[ ]*[0-9 ()-]*Ext:[ ]*[+0-9 ()-]*',




    }
    regexhp = {
        "History of Present Illness":r'H&P[\S\s]*?History of Present Illness(/Subjective)?[\S\s]*?(?<=Histories)',
        "Past Medical History":r'(?=H&P[\S\s]*)?Past Medical History:[\S\s]*?(?<=Review of Systems)',
        "Cognitive/Behavioral":r'(?=H&P[\S\s]*)?Cognitive[\S\s]*?Behavioral:[\S\s]*?Orientation:[\S\s]*?Concentration:[\S\s]*?Memory:[\S\s]*?Language:[\S\s]*(?<=Psychiatric)',
        "Muskuloskeletal":r'(?=H&P[\S\s]*)?Musculoskeletal[\S\s]*?(?<=Results Review)',
        "Impression and Plan":r'(?=H&P[\S\s]*)?Impression and Plan[\S\s]*?(?<=Signature)'
        
    }

    regexpt = {
        "Impairments":r'(?=Physical Therapy[\S\s]*?Assessment and Plan[\S\s]*)?Impairments[\S\s]*?(?<=Treating Diagnosis)',
        "Treating Diagnosis":r'(?=Physical Therapy[\S\s]*?Impairments[\S\s]*)?Treating Diagnosis[\S\s]*?(?<=Rehab Potential)',
        "Rehab Potential":r'(?=Physical Therapy[\S\s]*)?Rehab Potential[ ]*[:]*[ ]*[A-Za-z,.]*',
        "Assesmment/Rationale":r'(?=Physical Therapy[\S\s]*)?Assessment/Rationale for Skilled PT[ ]*[:]*[\S\s]*?(?<=Disposition)',
        "Disposition Recommandations":r'(?=Physical Therapy[\S\s]*?)?Disposition Recommendations[ ]*[:]*[\S\s]*?(?<=History)',
        "Medical Diagnosis":r'(?=Physical Therapy[\S\s]*)?Medical Diagnosis[ ]*[:]*[\S\s]*?(?<=Onset)',
        "Onset Date":r'(?=Physical Therapy[\S\s]*)?Onset Date[ ]*[:]*[ ]*[0-9]*/[0-9]*/[0-9]*',
        "Patient Precautions":r'(?=Physical Therapy[\S\s]*)?Patient Precautions[ ]*[:]*[ ]*[A-Za-z, ]*',
        "Weight Bearing Precautions":r'(?=Physical Therapy[\S\s]*)?Weight Bearing Precautions[\S\s]*?Right[ ]*LE[ ]*[.:]*[ ]*[A-Za-z ]*',
        "Prior LOV":r'(?=Physical Therapy[\S\s]*)?Prior Level of Function[\S\s]*?Ambulation[ ]*[:]*[ ]*[A-Za-z\\.,]*',
        "Sensory Systems":r"(?=Physical Therapy[\S\s]*)?Sensory Systems[\S\s]*?Subjective Information[ ]*[.:]*[ ]*[A-Za-z,./' -0-9]*",
        "Living Situation":r"(?=Physical Therapy[\S\s]*?Home Environment[\S\s]*)?Living Situation 1[ ]*[.:]*[ ]*[A-Za-z, .:0-9-/']*",
        "Cognition":r"(?=Physical Therapy[\S\s]*)?Cognition[\S\s]*?Orientation[ ]*[.:]*[ ]*[A-Za-z, .:0-9-/']*",
        "Mobility Level":r"(?=Physical Therapy[\S\s]*)?Mobility Level[\S\s]*?Bed to Chair[ ]*[.:]*[ ]*[A-Z a-z.,0-9]*",
        "Gait Assessment":r"(?=Physical Therapy[\S\s]*)?Gait Assessment[\S\s]*?Comments[ ]*[.:]*[ ]*[A-Z a-z.,0-9]*"
    }

















    
    simpleinfo = []

    #get insurance info
    try:
        insurances = re.findall(regex["Insurances"], text)
        insuranceids = re.findall(regex["Insurance Info"], text)
    except:
        insurances = ""
        insuranceids = ""
        print('Insurance Information Not Found')
    if insurances != "" and insuranceids != "":
        for i in range(0, len(insurances)):
            insurances[i] = insurances[i].strip('\n').split(':')
            for j in range(0, len(insurances[i])):
                insurances[i][j] = insurances[i][j].strip()
        for i in range(0, len(insuranceids)):
            insuranceids[i] = re.sub(r'E[A-Z]*:', ';', insuranceids[i])
            insuranceids[i] = insuranceids[i].replace("Insurance Name:", '').replace("ID #:", ';').replace("GP #:", ';').split(';')
            
            insuranceids[i][0]= [f"InsuranceName{i+1}", insuranceids[i][0].strip()]
            insuranceids[i][1]= [f"ID{i+1}", insuranceids[i][1].strip()]
            try:
                insuranceids[i][2] = [f"GP{i+1}", insuranceids[i][2].strip()]  
            except:
                insuranceids[i].append([f"GP{i+1}", ''])
            try:
                insuranceids[i][3] = [f"EFF{i+1}", insuranceids[i][3].strip()] 
            except:
                insuranceids[i].append([f"EFF{i+1}", ''])
            try:
                insuranceids[i][4] = [f"EXP{i+1}", insuranceids[i][4].strip().strip('\n')] 
            except:
                insuranceids[i].append([f"EXP{i+1}", ''] )

    #get simple info
    try:
        name = re.search(regex["Patient Name"], text).group(0).split(': ')
        simpleinfo.append(name)
    except:
        simpleinfo.append(["Patient Name", ""])
        print("Patient Name Not Found.")
    try:
        age = re.search(regex["Age"], text).group(0).split(':')
        for i in range(0, len(age)):
            age[i] = age[i].strip().strip('\n')
    except:
        age = ["Age", ""]
    try:
        dob = re.search(regex["DOB"], text).group(0).split(':')
        for i in range(0, len(dob)):
            dob[i] = dob[i].strip().strip('\n')
    except:
        dob = ["DOB", ""]
        print("DOB Not Found.")
    simpleinfo.append(age)
    simpleinfo.append(dob)
    try:
        sex = re.search(regex["Sex"], text).group(0).split(':')
        for i in range(0, len(sex)):
            sex[i] = sex[i].strip().strip('\n')
    except:
        sex = ["Sex", ""]
        print("Sex Not Found.")
    simpleinfo.append(sex)

    #referring MD
    try:
        referringmd = re.search(regex['Referring MD'], text).group(0)
        referringmd = referringmd.replace("Referring MD:", '').replace('Phone:', ';').replace('Fax:',';').split(';')
    except:
        referringmd = ['', '', '']
    try:
        referringmd[0] = ['Referring MD:', referringmd[0]]
    except:
        referringmd[0] = ['Referring MD:', ""]
        print("Referring MD Not Found")
    try:
        referringmd[1]= ['Phone:', referringmd[1]]
    except:
        referringmd[1] = ['Phone:', '']
    try:
        referringmd[2]= ['Fax:', referringmd[2]]
    except:
        referringmd[2] = ['Fax:', '']

    #patient address
    address1 = re.search(regex['Address Line 1'], text)
    try: 
        address1 = address1.group(0)
        address1 = re.sub(r'.*[\n]*.*Address Line 1:', '', address1).strip()
        if address1[-1] == '8':
            address1 = address1[:-1] + 'S'
    except:
        address1 = ""
        print("Address Line Not Found.")
    simpleinfo.append(['Address Line 1', address1.strip()])
    address2 = re.search(regex['Address Line 2'], text)
    try:
        address2 = address2.group(0)
        address2 = re.sub(r'PATIENT INFORMATION[\S\s]*Address Line 2:', '', address2).strip()
    except:
        address2 = ''
    try:
        patientworkphone = re.search(regex['Work Phone'], text).group(0)
        #print(patientworkphone)
        splitpart = re.search(r'PATIENT INFORMATION[\S\s]*Employment Status:[ ]*[A-Za-z0-9 \t]*Work Phone:', patientworkphone).group(0)
        #print(splitpart)

        patientworkphone = patientworkphone.replace(splitpart, '').strip()
       # print("Work phone: ", patientworkphone)
    except:
        patientworkphone = ""
        print("Patient Work Phone Not Found.")
    simpleinfo.append(["Address Line 2", address2])
    simpleinfo.append(["Work Phone", patientworkphone])
    try:
        patientcsc = re.search(regex['City/State/Country'],text).group(0)
        patientcsc = re.sub(r'PATIENT INFORMATION[\S\s]*City:', '', patientcsc)
        patientcsc = patientcsc.replace('ST:', ';').replace('Zip:', ';').replace('Country:', ';').split(';')
        patientcsc[0] = ['City', patientcsc[0].strip()]
        patientcsc[1] = ['ST', patientcsc[1].strip()]
        patientcsc[2] = ['Zip', patientcsc[2].strip()]
        patientcsc[3] = ['Country', patientcsc[3].strip()]
    except:
        print("City/ST/Zip/Country Not Found.")
        patientcsc = [['City', ''], ['ST', ''], ['Zip', ''], ['Country', '']]
    for i in patientcsc:
        if i != '':
            simpleinfo.append(i)
    #county
    try:
        patientcounty = re.search(regex['County'], text).group(0).replace('Home Phone', '').strip().split('County:')
        simpleinfo.append(["County",patientcounty[1].strip()])
    except:
        print("County Not Found.")
        simpleinfo.append(["County", ''])
    #home phone
    try:
        patienthomephone = re.search(regex['Home Phone'], text).group(0).split('Home Phone:')
        simpleinfo.append(["Home Phone", patienthomephone[1].strip()])
    except:
        print("Patient Home Phone Not Found.")
        simpleinfo.append(["Home Phone", ''])
    #NEAREST RELATIVE INFORMATION
    nrinfo = []
    try:
        nrname = re.search(regex['Nearest Relative Name'], text).group(0).split('Name:')
        nrinfo.append(["Nearest Relative Name", nrname[1].strip()])
    except:
        print("Nearest Relative Name Not Found.")
        nrinfo.append(["Nearest Relative Name", ""])
    try:
        nrrelation = re.search(regex['Nearest Relative Relation'], text).group(0).split("Relation:")
        #print(nrrelation)
        nrinfo.append(['Nearest Relative Relation', nrrelation[1].split('City')[0].strip()])
    except:
        print("Relation Note Found.")
        nrinfo.append(["Nearest Relative Relation", ""])
    try:
        nraddress = re.search(regex['Nearest Relative Address'], text).group(0).split('Address:')
        #print(nraddress)
        nrinfo.append(['Nearest Relative Address', nraddress[1].split('Home Phone')[0].strip()])
    except:
        print("Relative Address Not Found.")
        nrinfo.append(['Nearest Relative Address', ""])
    try:
        nrhomephone = re.search(regex['Nearest Relative Home Phone'], text).group(0).split('Home Phone:')
        nrinfo.append(['Nearest Relative Home Phone', nrhomephone[1].strip()])
    except:
        print("Nearest Relative Home Phone Not Found.")
        nrinfo.append(['Nearest Relative Home Phone', ''])
    try:
        nrcity = re.search(regex['Nearest Relative City'], text)
        #print(nrcity.group(0))
        nrcity = nrcity.group(0).replace('ST:', "").split("City:")
        nrinfo.append(["Nearest Relative City", nrcity[1].strip()])
    except:
        print("Nearest Reltive City Not Found.")
        nrinfo.append(['Nearest Relative City', ""])
    try:
        nrstate = re.search(regex['Nearest Relative ST'], text)
        #print(nrstate.group(0))
        nrstate = nrstate.group(0).replace('Zip', '').split('ST:')
        nrinfo.append(['Nearest Relative ST', nrstate[1].strip()])
    except:
        nrinfo.append(["Nearest Relative ST", ''])
    try:
        nrzip = re.search(regex['Nearest Relative Zip'], text).group(0).split('Zip:')
        nrinfo.append(["Nearest Relative Zip", nrzip[1].strip()])
    except:
        print("Nearest Relative Zip Not Found")
        nrinfo.append(["Nearest Relative Zip", ''])
    try:
        nrworkphone = re.search(regex['Nearest Relative Work Phone'], text).group(0)
        nrworkphone = re.split(r'Work Phone:|Ext:', nrworkphone)
        #print(nrworkphone)

        nrinfo.append(['Nearest Relative Work Phone', nrworkphone[1].strip()])
        if len(nrworkphone) >= 2:
            nrinfo.append(['Nearest Relative Work Phone Ext', nrworkphone[-1].strip()])
        else:
            nrinfo.append(['Nearest Relative Work Phone Ext', ''])
    except:
        print("Nearest Relative Work Phone & Extension Not Found.")
        nrinfo.append(['Nearest Relative Work Phone', ''])
        nrinfo.append(['Nearest Relative Work Phone Ext', ''])

    # database = sq.connect('patients.db')
    # pat_table = f""" CREATE TABLE IF NOT EXISTS pat_{filename} (
    #                                     patientname text,
    #                                     age text,
    #                                     dob text,
    #                                     sex text,
    #                                     address1 text,
    #                                     address2 text,
    #                                     workphone text,
    #                                     city text,
    #                                     st text,
    #                                     zip text,
    #                                     country text,
    #                                     county text,
    #                                     homephone text
    #                                 ); """
    # try:
    #     c = database.cursor()
    #     c.execute(pat_table)
    # except:
    #     print("Could not create patient table")
    #     exit(2)

    #REGEX H&P
    hnp = []
    hnptitles = []
    try:
        history = re.search(regexhp['History of Present Illness'], text).group(0)
    #print(history)
        history = history.replace('Histories', '').replace('\n', ' ')

        history = re.split(r'History of Present Illness(/Subjective)?', history)
    
        try:
            history.remove(None)
        except ValueError: 
            pass
    except:
        print("History of Present Illness Not Found.")
        history= ["", ""]
    #print(history)
    #exit()
    # try:
    #     database.execute(f"ALTER TABLE pat_{filename} \
    #       ADD {'History'} bigtext;")
    # except:
    #     print("History Table Exists.")
    # database.execute(f"INSERT INTO pat_{filename} (History) \
    #   VALUES ('{history[1].strip()}'); ")

    
    
    try:
        pastmedical = re.search(regexhp['Past Medical History'], text).group(0).replace("Review of Systems", '').replace('\n', ' ')
        pastmedical = pastmedical.split('Past Medical History:')
        #print(pastmedical)
    except:
        print("Past Medical History Not Found")
        pastmedical = ["", ""]
    toremove = ""
    try:
        toremove = re.search(r"Printed by: [\s\S]*? * Final Report *", text).group(0).replace('\n', ' ')
        #print(toremove)
    except:
        pass
    
    hnp.append(history[1])
    hnp.append(pastmedical[1])
    hnptitles.append('History of Present Illness')
    hnptitles.append('Past Medical History')

    
    cognitive = ""
    try:
        cognitive = re.search(regexhp['Cognitive/Behavioral'], text).group(0)
        
        cognitive = cognitive.replace('Psychiatric', '').replace('Orientation:', '/split/')
        cognitive = cognitive.replace("Concentration:", '/split/').replace('Memory:', '/split/')
        #TODO fix replace
        cognitive = cognitive.replace('Language:', '/split/')
        cognitive = cognitive.split('/split/')
        cognames = ['Orientation', 'Concentration', 'Memory', 'Language']
        for i in range(1, len(cognitive)):
            hnp.append(cognitive[i].strip())
            hnptitles.append(cognames[i-1])
    except:
        print("Cognitive/Behavioral Not Found.")
    #dprint(cognitive)
    
    
    #musculoskeletal 
    try:
        muskulosketal = re.search(regexhp['Muskuloskeletal'], text).group(0)
        #print(muskulosketal)
        muskulosketal = muskulosketal.replace('Results Review', '')
        muskulosketal = muskulosketal.split('Musculoskeletal')
        #print(muskulosketal)
        hnp.append(muskulosketal[1].strip().replace('\n', ' '))
        hnptitles.append("Muskuloskeletal")

    except:
        print("Muskuloskeletal Not Found.")
        hnp.append("")
        hnptitles.append("Muskuloskeletal")

    try:
        impression = re.search(regexhp['Impression and Plan'], text).group(0)
        impression = impression.replace('Signature', '').replace('\n', ' ')
        impression = impression.split('Impression and Plan')
        hnp.append(impression[1].strip())
        hnptitles.append("Impression and Plan")
    except:
        print("Impression and Plan not found.")

    #PHYSICAL THERAPY 
    pt = []
    ptitle = []
    try:
        removept = re.search(r'(?=PT Eval[\S\s]*)?[A-Za-z]*, [A-Za-z]* [A-Za-z]*, PT - [0-9]*/[0-9]*/[0-9]* [0-9]*:[0-9]*', text).group(0)
    except:
        removept = ""
    #print(f"PT Remove: {removept}")
    try:
        impairments = re.search(regexpt['Impairments'], text).group(0)
        
        impairments = impairments.replace('Treating Diagnosis', '').replace('\n', ' ')
        #print(impairments)
        splitimpairments = re.search(r'Impairments[ ]*[:]*', impairments).group(0)
        #print(splitimpairments)
        impairments = impairments.split(splitimpairments)
        pt.append(impairments[1].strip())
        ptitle.append('Impairments')
    except:
        print("Impairments not Found")
        pt.append("")
        ptitle.append("Impairments")
    treatingd = ''
    try:
        treatingd = re.search(regexpt['Treating Diagnosis'], text).group(0)
        splittreat = re.search(r'Treating Diagnosis[ ]*[:]*[ ]*', treatingd).group(0)
        treatingd = treatingd.split(splittreat)

        
        treatingd = treatingd[-1]
        
        treatingd = treatingd.replace('Rehab Potential', '').replace('\n', ' ')
        #print(treatingd)
        
        # print("To Split: ", splittreat)
        # #print(splittreat)
        # treatingd = treatingd.split(splittreat)
        #print(treatingd)
        #treatingd.remove('')

        #print(treatingd)
        #print(treatingd)
        pt.append(treatingd.strip())
        ptitle.append("Treating Diagnosis")
    except:
        print("Treating Diagnosis Not Found.")
        pt.append("")
        ptitle.append("Treating Diagnosis")
    try:
        rehab = re.search(regexpt['Rehab Potential'], text).group(0)
        splitrehab = re.search(r'Rehab Potential[ ]*[:]*[ ]*', rehab).group(0)
        rehab = rehab.split(splitrehab)
        pt.append(rehab[1].strip())
        ptitle.append("Rehab Potential")
    except:
        print("Rehab Potential Not Found")
    try:
        rational = re.search(regexpt['Assesmment/Rationale'], text).group(0)
        rational = rational.replace('Disposition', '').replace('\n', ' ')
        splitrational=re.search(r'Assessment/Rationale for Skilled PT[ ]*[:]*[ ]*', rational).group(0)
        rational = rational.split(splitrational)
        pt.append(rational[1].strip())
        ptitle.append("Assessment/Rationale")
    except:
        print("Assessment/Rationale Not Found")
    try:
        disposition = re.search(regexpt['Disposition Recommandations'], text).group(0)
        #print(disposition)
        disposition = disposition.replace("History", '')
        disposition.replace(removept, '').replace('\n', '')
        disps = []
        disps.append(re.search(r'Disposition Recommendations[ ]*[:]*', disposition).group(0))
        disps.append(re.search(r'Frequency[ ]*[:]*[ ]*', disposition).group(0))
        disps.append(re.search(r'Duration[ ]*[:]*[ ]*', disposition).group(0))
        disps.append(re.search(r'Duration Unit[ ]*[:]*[ ]*', disposition).group(0))
        disps.append(re.search(r'Therapeutic Procedures Interventions Planned[ ]*[:]*[ ]*', disposition).group(0))
        disps.append(re.search(r'Pt/Caregiver Involved in Goal Setting & Tx Plan[ ]*[:]*[ ]*', disposition).group(0))
        #print(disps)
        for k in disps:
            disposition = disposition.replace(k, '\fQtz')

        #print(disposition)
        disposition = disposition.split('\fQtz')
        

        disposition.remove('')
        disptitles = [
            'Disposition Recommendations',
            'Frequency',
            'Duration',
            'Duration Unit',
            'Therapeutic Procedures Interventions Planned',
            'Pt/Caregiver Involved in Goal Setting & Tx Plan'
        ]
        for i in range(len(disptitles)):
            #print(disptitles[i],':', disposition[i])
            pt.append(disposition[i])
            ptitle.append(disptitles[i])
    except:
        disptitles = [
            'Disposition Recommendations',
            'Frequency',
            'Duration',
            'Duration Unit',
            'Therapeutic Procedures Interventions Planned',
            'Pt/Caregiver Involved in Goal Setting & Tx Plan'
        ]
        for i in range(len(disptitles)):
            pt.append("")
            ptitle.append(disptitles[i])
        print("Disposition Recommendations Not Found")
    medicaldiagnosis = ''
    try:
        medicaldiagnosis = re.search(regexpt['Medical Diagnosis'], text).group(0)
        medicaldiagnosis = medicaldiagnosis.replace('Onset', '').replace('\n', ' ')
        splitmedical = re.search(r'Medical Diagnosis[ ]*[:]*[ ]*', medicaldiagnosis).group(0)
        medicaldiagnosis = medicaldiagnosis.split(splitmedical)
        pt.append(medicaldiagnosis[1].strip())
        ptitle.append("Medical Diagnosis")
    except:
        pt.append("")
        ptitle.append("Medical Diagnosis")
        print("Medical Diagnosis Not Found.")

    try:
        onsetdate = re.search(regexpt['Onset Date'], text).group(0)
        splitonset = re.search(r'Onset Date[ ]*[:]*[ ]*', onsetdate).group(0)
        onsetdate = onsetdate.split(splitonset)
        pt.append(onsetdate[1].strip())
        ptitle.append("Onset Date")
    except:
        pt.append("")
        ptitle.append("Onset Date")
        print("Onset Date Not Found.")
    try:
        patientprec = re.search(regexpt['Patient Precautions'], text).group(0)
        #print(patientprec)
        splitpprec = re.search(r'Patient Precautions[ ]*[:]*[ ]*', patientprec).group(0)
        patientprec = patientprec.replace('\n', ' ').split(splitpprec)
        pt.append(patientprec[1].strip())
        ptitle.append("Patient Precautions")
    except:
        pt.append("")
        ptitle.append("Patient Precautions")
        print("Patient Precautions Not Found")
    try:
        weightbear = re.search(regexpt['Weight Bearing Precautions'], text).group(0)
        #print(weightbear)
        weights = []
        weights.append(re.search(r'Left[ ]*[UV]+E[ ]*[.:]*[ ]*', weightbear).group(0))
        weights.append(re.search(r'Right[ ]*[UV]+E[ ]*[.:]*[ ]*', weightbear).group(0))
        weights.append(re.search(r'Left[ ]*LE[ ]*[.:]*[ ]*', weightbear).group(0))
        weights.append(re.search(r'Right[ ]*LE[ ]*[.:]*[ ]*', weightbear).group(0))
        for i in weights:
            weightbear = weightbear.replace(i, '\fQrz')
        weightbear = weightbear.split('\fQrz')
        weightbear.remove(weightbear[0])
        wbnames = ['Left UE', 'Right UE', 'Left LE', 'Right LE']
        for i in range(len(weightbear)):
            pt.append(weightbear[i].strip())
            ptitle.append(wbnames[i])
    except:
        wbnames = ['Left UE', 'Right UE', 'Left LE', 'Right LE']
        for i in range(len(wbnames)):
            pt.append("")
            ptitle.append(wbnames[i])
        print("Weight Bearing Precautions Not Found.")
    try:
        priorlov = re.search(regexpt['Prior LOV'], text).group(0)
        #print(priorlov)
        priors = []
        priors.append(re.search(r'Transfers[ ]*[.:]*[ ]*', priorlov).group(0))
        priors.append(re.search(r'Bed Mobility[ ]*[.:]*[ ]*', priorlov).group(0))
        priors.append(re.search(r"ADL's[ ]*[.:]*[ ]*", priorlov).group(0))
        priors.append(re.search(r'Ambulation[ ]*[.:]*[ ]*', priorlov).group(0))
        for i in priors:
            priorlov = priorlov.replace(i, '\fQrz')
        
        priorlov = priorlov.split('\fQrz')
        priorlov.remove(priorlov[0])
        lovnames = [
            'Tranfers',
            'Bed Mobility',
            "ADL's",
            'Ambulation']
        for i in range(len(priorlov)):
            priorlov[i] = priorlov[i].strip().replace('\\', 'I')
            pt.append(priorlov[i].strip())
            ptitle.append(lovnames[i])
    except:
        lovnames = [
            'Tranfers',
            'Bed Mobility',
            "ADL's",
            'Ambulation']
        for i in range(len(lovnames)):
            
            pt.append("")
            ptitle.append(lovnames[i])
        print("Prior LOV Not Found.")
    try:
        sensory = re.search(regexpt['Sensory Systems'], text).group(0)
        #print(sensory)
        splitsens = []
        splitsens.append(re.search(r'Auditory[ ]*[.:]*[ ]*', sensory).group(0))
        splitsens.append(re.search(r'Vision[ ]*[.:]*[ ]*', sensory).group(0))
        splitsens.append(re.search(r'Subjective Information[ ]*[.:]*[ ]*', sensory).group(0))
        for i in splitsens:
            sensory = sensory.replace(i, '\fQrz')
        sensory = sensory.split('\fQrz')
        sensory.remove(sensory[0])
        sensnames = [
            'Auditory',
            'Vision',
            'Subjective Information'
        ]
        for i in range(len(sensory)):
            pt.append(sensory[i].strip())
            ptitle.append(sensnames[i])
    except:
        sensnames = [
            'Auditory',
            'Vision',
            'Subjective Information'
        ]
        for i in range(len(sensnames)):
            pt.append("")
            ptitle.append(sensnames[i])
        print("Sensory Systems Not Found.")
    try:
        living = re.search(regexpt['Living Situation'], text).group(0)
        splitliv = re.search(r'Living Situation 1[ ]*[.:]*[ ]*', living).group(0)
        living = living.split(splitliv)
        pt.append(living[1].strip())
        ptitle.append('Living Situation 1')
    except:
        pt.append("")
        ptitle.append('Living Situation 1')
        print("Living Situation 1 Not Found")
    try:
        cognition = re.search(regexpt['Cognition'], text).group(0)
        cogns = []
        cogns.append(re.search(r'Level of Consciousness[ ]*[.:]*[ ]*', cognition).group(0))
        cogns.append(re.search(r'Orientation[ ]*[.:]*[ ]*', cognition).group(0))
        for i in cogns:
            cognition = cognition.replace(i, '\fQrz')
        cognition = cognition.split('\fQrz')
        cognition.remove(cognition[0])
        cognames = ['Cognition Level of COnsciousness', 'Cognition Orientation']
        for i in range(len(cognition)):
            pt.append(cognition[i])
            ptitle.append(cognames[i])
    except:
        cognames = ['Cognition Level of COnsciousness', 'Cognition Orientation']
        for i in range(len(cognames)):
            pt.append("")
            ptitle.append(cognames[i])
        print("Cognition Not Found")
    

    try:
        mobility = re.search(regexpt['Mobility Level'], text).group(0)
        mobs = []
        mobs.append(re.search(r'Supine to Sit[ ]*[:.]*[ ]*', mobility).group(0))
        mobs.append(re.search(r'Sit to Stand[ ]*[:.]*[ ]*', mobility).group(0))
        mobs.append(re.search(r'Stand to Sit[ ]*[.:]*[ ]*', mobility).group(0))
        mobs.append(re.search(r'Bed to Chair[ ]*[:.]*[ ]*', mobility).group(0))
        mobility = mobility.replace('\n', ' ').replace('(', '').replace(')', '')
        mobility = mobility.replace('[', '').replace(']', '')
        #mobility.remove()
        for i in mobs:
            mobility = mobility.replace(i, '\fQrz')
        mobility = mobility.split('\fQrz')
        mobility.remove(mobility[0])
        mobnames = ['Supine to Sit', 'Sit to Stand', 'Stand to Sit', 'Bed to Chair']
        for i in range(len(mobs)):
            pt.append(mobility[i].strip())
            ptitle.append(mobnames[i])
    except:
        mobnames = ['Supine to Sit', 'Sit to Stand', 'Stand to Sit', 'Bed to Chair']
        for i in range(len(mobnames)):
            pt.append("")
            ptitle.append(mobnames[i])
        print('Mobility Level Not Found')
    try:
        gait = re.search(regexpt['Gait Assessment'], text).group(0)
        #print(gait)
        splitgait = re.search(r'Comments[ ]*[.:]*[ ]*', gait).group(0)
        gait = gait.split(splitgait)
        #print(gait)
        pt.append(gait[1].strip())
        ptitle.append('Gait Assessment Comments')
    except:
        pt.append("")
        ptitle.append('Gait Assessment Comments')
        print('Gait Assessment Not Found')

    




    for i in range(len(hnp)):
        try: 
            #print(hnp[i])
            hnp[i] = hnp[i].replace(toremove, '')
            #print(hnp[i])
        except:
            print(f'{hnptitles[i]} fail.')
    for i in range(len(pt)):
        try: 
            #print(hnp[i])
            pt[i] = pt[i].replace(toremove, '').strip()
            pt[i] = pt[i].replace(removept, '').strip()
            #print(hnp[i])
        except:
            print(f'{ptitle[i]} fail.')
    
    # for i in hnp:

    # try:
    #     database.execute(f"ALTER TABLE pat_{filename} \
    #       ADD {'PastMedical'} bigtext;")
    # except:
    #     print("Past Medical History Table Exists.")
    # database.execute(f"INSERT INTO pat_{filename} (PastMedical) \
    #   VALUES ('{pastmedical[1].strip()}'); ")
    # f = open('naming_guide.txt', 'a')
    # f.write('#History\nHistory\nPastMedical\n')
    # f.close()










    #database creation
    #nrinfo: list of nearest relative info
    #simplinfo: lift of demographic info
    #insurances: kinda messed up list of insurance info 
    #id integer PRIMARY KEY,
    
    
    
    # extractedsimple = []
    # for i in simpleinfo:
    #     extractedsimple.append(i[1])
    # database.execute(f"INSERT INTO pat_{filename} (patientname, age, dob, sex, address1, address2, workphone, city, st, zip, country, county, homephone) \
    #   VALUES ({str(extractedsimple)[1:-1]}); ")
    # cursor = database.execute(f"SELECT , workphone, city, st, zip, country, county, homephone from pat_{filename}")
    # for row in cursor:
    #     print(row)

    #insert insurance info
    # sqlinsurance = []
    # innames = []
    # for i in range(0, 3):
    #     if i < len(insurances) and insurances != "":
    #         sqlinsurance.append(insurances[i][1])
    #         innames.append(insurances[i][0].replace(' ', ''))
    #         for j in insuranceids[i]:
    #             sqlinsurance.append(j[1])
    #             innames.append(j[0].replace(' ', '').replace('#', ''))
    #     else:
    #         k = ["Primary Insurance", "Secondary Insurance", "Tertiary Insurance"]
    #         sqlinsurance.append('')
    #         innames.append(k[i].replace(' ', ''))
    #         innames.append(f'InsuranceName{i+1}')
    #         sqlinsurance.append('')
    #         innames.append(f"ID{i+1}")
    #         sqlinsurance.append('')
    #         innames.append(f"GP{i+1}")
    #         sqlinsurance.append('')
    #         innames.append(f"EFF{i+1}")
    #         sqlinsurance.append('')
    #         innames.append(f"EXP{i+1}")
    #         sqlinsurance.append('')
    # f = open('naming_guide.txt', 'a')
    # f.write('#Insurance Info:\n')
    # for i in innames:
    #     #f.write(i+'\n')
    #     try:
    #         database.execute(f"ALTER TABLE pat_{filename} \
    #         ADD {i} text;")
    #     except:
    #         print(f"Table for {i} already exists.")
    # database.execute(f"INSERT INTO pat_{filename} ({str(innames)[1:-1]}) \
    #   VALUES ({str(sqlinsurance)[1:-1]}); ")
    # cursor = database.execute(f"SELECT InsuranceName1, ID1, GP1, EFF1, EXP1 from pat_{filename}")
    # for row in cursor:
    #     print(row)
    # for i in referringmd:
    #     writer.writerow(i)
    # for i in nrinfo:
    #     writer.writerow(i)
    #f.write('#Referring MD:\n')
    # referringnames = []
    # referringdat = []
    # for i in referringmd:
    #     referringnames.append(i[0].replace(':', '').replace(' ', ''))
    #     referringdat.append(i[1])
    # for i in referringnames:
    #     #f.write(i+'\n')
    #     try:
    #         database.execute(f"ALTER TABLE pat_{filename} \
    #         ADD {i} text;")
    #     except:
    #         print(f"Table for {i} already exists.")
    # database.execute(f"INSERT INTO pat_{filename} ({str(referringnames)[1:-1]}) \
    #   VALUES ({str(referringdat)[1:-1]}); ")
    # nrnames = []
    # nrdat = []
    # #f.write('#Nearest Relative Info:')
    # for i in nrinfo:
        
    #     nrnames.append(i[0].replace(':', '').replace(' ', ''))
    #     nrdat.append(i[1])
    # for i in nrnames:
    #     #f.write(i+'\n')
    #     try:
    #         database.execute(f"ALTER TABLE pat_{filename} \
    #         ADD {i} text;")
    #     except:
    #         print(f"Table for {i} already exists")
    # database.execute(f"INSERT INTO pat_{filename} ({str(nrnames)[1:-1]}) \
    #   VALUES ({str(nrdat)[1:-1]}); ")

    


    #write info to file
    #f = open('pat_' + filename + '.csv', 'w', encoding = 'UTF8', newline = '')
    f = open('pat_patientfile1' + '.csv', 'a', encoding='UTF8', newline='')
    writer = csv.writer(f)
    row1 = []
    row2 = []

    # write the header
    for i in simpleinfo:
        row1.append(i[0])
        row2.append(i[1])
        #writer.writerow(i)
    #CHECK MEDICARE
    Medicare = False
    medicarenames = ['Medicare', 'medicare']
    for i in medicarenames:
        try:
            designator = re.search(i, text).group(0)
        except:
            designator = ''
        if (designator != ''):
            Medicare = True
    
    #CHECK CMS
    cms, cmsdiagnosis = checkcms(text)
    #print(cmsdiagnosis)
    
    


    # write the data
    for i in range(0, 3):
        if i < len(insurances) and insurances != "":
            row1.append(insurances[i][0])
            row2.append(insurances[i][1])
            #writer.writerow(insurances[i])
            if i < len(insuranceids):
                for j in insuranceids[i]:
                    row1.append(j[0])
                    row2.append(j[1])
            else:
                row2.append("")
                row2.append("")
                #writer.writerow(j)
        else:
            k = ["Primary Insurance", "Secondary Insurance", "Tertiary Insurance"]
            row1.append(k[i])
            row2.append('')
            row1.append("Insurance Name")
            row2.append('')
            row1.append("ID #")
            row2.append('')
            row1.append("GP #")
            row2.append('')
            row1.append('EFF')
            row2.append('')
            row1.append('EXP')
            row2.append('')

            # writer.writerow([k[i], ''])
            # writer.writerow(["Insurance Name", ''])
            # writer.writerow(["ID #", ''])
            # writer.writerow(["GP #", ''])
            # writer.writerow(["EFF", ''])
            # writer.writerow(["EXP", ''])
    
    for i in range(len(referringmd)):
        row1.append(referringmd[i][0])
        row2.append(referringmd[i][1])
        if i == 0:
            row1.append('Referring Hospital')
            row2.append('')

    
        #writer.writerow(i)
    for i in nrinfo:
        row1.append(i[0])
        row2.append(i[1])
        #writer.writerow(i)
    #append Status	Diagnosis	CMS Diagnosis	Rejection Disposition	Referral Date	Assignee
    row1.append('Status')
    row2.append('')
    row1.append('Diagnosis')
    row1.append("CMS Diagnosis")
    row2.append(cmsdiagnosis)
    if Medicare == True:
        if cms == True:
            row2.append("Yes")
        else:
            row2.append("No")
    else:
        row2.append("N/A")
    

    toappend = ['Rejection Disposition', 'Referral Date', 'Assignee']
    #H&P Formatting
    for i in toappend:
        row1.append(i)
        row2.append('')

    for i in hnptitles:
        row1.append(i)
    for i in hnp:
        row2.append(i)
    for i in pt:
        row2.append(i)
    for i in ptitle:
        row1.append(i)
    writer.writerow(row1)
    writer.writerow(row2)

    f.close()
    
#parse, text, filename = sys.argv
outputFile = 'patient_patient1'
f = open(outputFile + '.txt', 'r')
text = f.read()#, "pat_" + inputFile)
parser(text, 'patient1')
# parser(text, filename)