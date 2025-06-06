from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from groq import Groq
import json

app = FastAPI()

# Load drug interaction data
with open('data_partitioned.json', 'r') as f:
    drug_interactions = json.load(f)

# Clean up drug list by removing duplicates and incomplete entries
drug_list = [
    "ACE inhibitors",
    "ACE inhibitors and other antihypertensives",
    "ACE inhibitors or Angiotensin II receptor antagonists",
    "Abatacept",
    "Acacia or Guar gum",
    "Acamprosate",
    "Acarbose",
    "Acetazolamide",
    "Acetylcysteine",
    "Aciclovir",
    "Aciclovir and related drugs",
    "Acipimox",
    "Adefovir",
    "Ademetionine",
    "Adenosine",
    "Agalsidase",
    "Ajmaline",
    "Albendazole",
    "Albendazole or Mebendazole",
    "Albendazole with Ivermectin",
    "Alcohol",
    "Alemtuzumab",
    "Alendronate",
    "Aliskiren",
    "Allopurinol",
    "Alosetron",
    "Alpha blockers",
    "Alprostadil",
    "Aluminium hydroxide",
    "Amantadine",
    "Amfetamines",
    "Amfetamines and related drugs",
    "Amifostine",
    "Amiloride",
    "Aminoglutethimide",
    "Aminoglycosides",
    "Aminosalicylic acid",
    "Amiodarone",
    "Amisulpride",
    "Amodiaquine",
    "Amphotericin B",
    "Ampicillin",
    "Anabolic steroids",
    "Anabolic steroids or Androgens",
    "Anaesthesia",
    "Anagrelide",
    "Anakinra",
    "Anastrozole",
    "Androgens",
    "Angiotensin II receptor antagonists",
    "Anorectics",
    "Antacids",
    "Antacids or Antidiarrhoeals",
    "Antacids or Calcium compounds",
    "Antacids or Kaolin",
    "Antacids or Urinary alkalinisers",
    "Anthelmintics",
    "Anthracyclines",
    "Antiarrhythmics",
    "Antiasthma drugs",
    "Antibacterials",
    "Anticholinesterases",
    "Antidepressants",
    "Antidiabetics",
    "Antiemetics",
    "Antiepileptics",
    "Antifibrinolytics",
    "Antifungals",
    "Antigout drugs",
    "Antihistamines",
    "Antihistamines and related drugs",
    "Antihypertensives",
    "Antimalarials",
    "Antimuscarinics",
    "Antimuscarinics or Diphenoxylate",
    "Antimycobacterials",
    "Antineoplastics",
    "Antiplatelet drugs",
    "Antiplatelet drugs or NSAIDs",
    "Antipsychotics",
    "Antiretrovirals",
    "Antithyroid drugs",
    "Apomorphine",
    "Aprepitant",
    "Aprindine",
    "Aprotinin",
    "Argatroban",
    "Aripiprazole",
    "Armodafinil",
    "Aromatase inhibitors",
    "Artemether",
    "Artemisinin derivatives",
    "Aspirin",
    "Aspirin or NSAIDs",
    "Aspirin or other Salicylates",
    "Atomoxetine",
    "Atovaquone",
    "Atropine",
    "Ayahuasca",
    "Azathioprine",
    "Azathioprine or Mercaptopurine",
    "Azimilide",
    "Azithromycin",
    "Azoles",
    "Aztreonam",
    "BCG vaccine",
    "Baclofen",
    "Barbiturates",
    "Barbiturates or Phenytoin",
    "Basiliximab",
    "Benfluorex",
    "Benzbromarone",
    "Benzbromarone or Benziodarone",
    "Benzethonium chloride",
    "Benziodarone",
    "Benzodiazepines",
    "Benzodiazepines and related drugs",
    "Berberine",
    "Beta blockers",
    "Betacarotene",
    "Betahistine",
    "Bevacizumab",
    "Beverages",
    "Bexarotene",
    "Bicalutamide",
    "Bifendate",
    "Bismuth compounds",
    "Bisphosphonates",
    "Bleomycin",
    "Boldo or Fenugreek",
    "Bortezomib",
    "Bosentan",
    "Bretylium",
    "Brimonidine or Latanoprost",
    "Bromocriptine",
    "Bromocriptine and other dopamine agonists",
    "Broxuridine",
    "Bucolome",
    "Buflomedil",
    "Bupropion",
    "Buspirone",
    "Busulfan",
    "Butyraldoxime",
    "CNS depressants",
    "COMT inhibitors",
    "CYP2C9 substrates",
    "CYP2D6 inhibitors",
    "CYP2D6 inhibitors or substrates",
    "CYP2D6 substrates",
    "CYP3A4 inducers",
    "CYP3A4 inducers or inhibitors",
    "CYP3A4 inhibitors",
    "CYP3A4 inhibitors or substrates",
    "CYP3A4 substrates",
    "Caffeine",
    "Caffeine or Choline theophyllinate",
    "Calcium carbimide",
    "Calcium compounds",
    "Candesartan",
    "Cannabinoids",
    "Cannabis",
    "Cannabis or Tobacco",
    "Capsaicin",
    "Carbamazepine",
    "Carbamazepine or Oxcarbazepine",
    "Carbamazepine or Phenytoin",
    "Carbapenems",
    "Carbenoxolone",
    "Carbimazole",
    "Carbon tetrachloride",
    "Carbonic anhydrase inhibitors",
    "Carisoprodol",
    "Carmofur",
    "Cefalexin",
    "Cefradine",
    "Celecoxib",
    "Cephalosporins",
    "Cetuximab",
    "Chamomile",
    "Chinese herbal medicines",
    "Chitosan",
    "Chlorambucil",
    "Chloramphenicol",
    "Chlorobutanol",
    "Chloroquine",
    "Chloroquine or Hydroxychloroquine",
    "Chloroquine with Proguanil",
    "Chlorothiazide",
    "Chlorphenamine",
    "Chlorpromazine",
    "Chlorzoxazone",
    "Chromium compounds",
    "Ciclosporin",
    "Ciclosporin or Tacrolimus",
    "Cidofovir",
    "Cilostazol",
    "Cimetidine",
    "Cimetidine or Omeprazole",
    "Cinacalcet",
    "Ciprofloxacin",
    "Cisapride",
    "Cisplatin",
    "Cisplatin and other platinum compounds",
    "Clarithromycin",
    "Class Ic antiarrhythmics",
    "Clindamycin",
    "Clindamycin or Lincomycin",
    "Clodronate",
    "Clofazimine",
    "Clomethiazole",
    "Clomipramine",
    "Clonidine",
    "Clonidine and related drugs",
    "Clopidogrel",
    "Clopidogrel or Ticlopidine",
    "Cloral hydrate",
    "Cloral hydrate and related drugs",
    "Clozapine",
    "Cocaine",
    "Codeine",
    "Coffee or Tea",
    "Cola drinks",
    "Colchicine",
    "Colesevelam",
    "Colestipol",
    "Colestyramine",
    "Colistin",
    "Colloids",
    "Combined hormonal contraceptives",
    "Corticosteroids",
    "Corticosteroids or Corticotropin",
    "Coumarins",
    "Coumarins and related drugs",
    "Coxibs",
    "Cranberry juice",
    "Curbicin",
    "Cyclobenzaprine",
    "Cyclophosphamide",
    "Cyclophosphamide or Ifosfamide",
    "Cycloserine",
    "Cyproheptadine",
    "Cyproterone acetate",
    "Cytarabine",
    "Cytochrome P450 substrates",
    "Cytokines",
    "Dacarbazine",
    "Dairy products",
    "Danaparoid",
    "Danazol",
    "Danazol or Gestrinone",
    "Dantrolene",
    "Dantrolene and Oxybutynin",
    "Dapsone",
    "Daptomycin",
    "Darifenacin or Solifenacin",
    "Dasatinib",
    "Desmopressin",
    "Dexamethasone",
    "Dexamfetamine",
    "Dexfenfluramine or Fenfluramine",
    "Dexmedetomidine",
    "Dextrans",
    "Dextromethorphan",
    "Dialysis or Transfusion membranes",
    "Diazepam",
    "Diazoxide",
    "Dichloralphenazone",
    "Diclofenac",
    "Didanosine",
    "Dietary fibre or Laxatives",
    "Diethylcarbamazine",
    "Digoxin",
    "Digoxin and related drugs",
    "Dihydroergocryptine",
    "Diltiazem",
    "Dimethylformamide",
    "Diosmin",
    "Diphenhydramine",
    "Dipyridamole",
    "Disopyramide",
    "Disopyramide or Procainamide",
    "Distigmine",
    "Disulfiram",
    "Ditazole",
    "Diuretics",
    "Dobutamine",
    "Dofetilide",
    "Domperidone",
    "Doxapram",
    "Doxofylline",
    "Doxorubicin",
    "Dronedarone",
    "Drotrecogin alfa",
    "Drugs that affect calcium",
    "Drugs that affect gastric pH",
    "Drugs that affect renal clearance",
    "Drugs that alter its renal clearance",
    "Drugs that cause bone marrow suppression",
    "Drugs that cause pancreatitis",
    "Drugs that lower potassium levels",
    "Drugs that prolong the QT interval",
    "Duloxetine",
    "Dutasteride",
    "Dutasteride or Finasteride",
    "Echinocandins",
    "Ecothiopate iodide",
    "Edible fungi",
    "Edrophonium",
    "Emergency hormonal contraceptives",
    "Endothelin receptor antagonists",
    "Enfuvirtide",
    "Enoximone",
    "Entecavir",
    "Enteral feeds or Food",
    "Enzastaurin",
    "Enzyme inducers",
    "Ephedrine",
    "Eplerenone",
    "Epoetins",
    "Epoprostenol",
    "Ergot derivatives",
    "Erlotinib",
    "Erythromycin",
    "Eslicarbazepine",
    "Estramustine",
    "Etanercept",
    "Ethambutol",
    "Ethchlorvynol",
    "Ethionamide",
    "Ethosuximide",
    "Ethylene dibromide",
    "Etoposide",
    "Evening primrose oil",
    "Everolimus",
    "Exemestane",
    "Exenatide",
    "Ezetimibe",
    "Famciclovir",
    "Febuxostat",
    "Felbamate",
    "Felodipine",
    "Fenfluramine",
    "Fenoldopam",
    "Fibrates",
    "Fibre or Pectin",
    "Fish oils",
    "Flecainide",
    "Fluconazole",
    "Flucytosine",
    "Fludarabine",
    "Fludarabine with Cytarabine",
    "Flunarizine",
    "Fluorouracil",
    "Fluorouracil and related prodrugs",
    "Fluorouracil prodrugs",
    "Fluoxetine",
    "Fluoxetine and Droperidol",
    "Flupentixol and related drugs",
    "Flupirtine",
    "Flutamide",
    "Fluvastatin",
    "Fluvoxamine",
    "Folic acid",
    "Folinates",
    "Fondaparinux",
    "Food",
    "Food or Guar gum",
    "Foscarnet",
    "Fosfomycin",
    "Fosphenytoin",
    "Fulvestrant",
    "Furazolidone",
    "Furosemide",
    "Fusidic acid",
    "Gabapentin",
    "Ganciclovir",
    "Ganciclovir or Valganciclovir",
    "Garlic",
    "Gemcitabine",
    "Gemfibrozil",
    "Gestrinone",
    "Geum chiloense",
    "Ginger",
    "Ginseng",
    "Glucagon",
    "Glutethimide",
    "Gold",
    "Granisetron",
    "Grapefruit",
    "Grapefruit and other fruit juices",
    "Grapefruit juice",
    "Griseofulvin",
    "Guanadrel",
    "Guanethidine",
    "Guanethidine and related drugs",
    "Guanfacine",
    "Guar gum or Glucomannan",
    "HRT",
    "Halofantrine",
    "Haloperidol",
    "Haloperidol and related drugs",
    "Heparin",
    "Heparin and LMWHs",
    "Heparinoids",
    "Heparins",
    "Herbal medicines",
    "Herbal medicines or Foods",
    "Herbicides",
    "Hormonal contraceptives",
    "Hormonal contraceptives and Progestogens",
    "Hormonal contraceptives or HRT",
    "Hormonal contraceptives or Sex hormones",
    "Hydralazine",
    "Hydrochlorothiazide",
    "Hydroxycarbamide",
    "Ibuprofen",
    "Ibutilide",
    "Idenafil",
    "Idoxuridine",
    "Idrocilamide",
    "Imatinib",
    "Imatinib and Sunitinib",
    "Imipenem",
    "Imipramine",
    "Immunoglobulins",
    "Immunosuppressants",
    "Indanediones",
    "Indinavir",
    "Indometacin",
    "Influenza vaccines",
    "Inotropes and Vasopressors",
    "Insect allergen extracts",
    "Insecticides",
    "Insulin",
    "Interferon alfa",
    "Interferons",
    "Ipriflavone",
    "Irbesartan",
    "Irinotecan",
    "Iron chelators",
    "Iron compounds",
    "Iron or Zinc compounds",
    "Isoniazid",
    "Isotretinoin",
    "Itraconazole",
    "Ivabradine",
    "Ivermectin",
    "Kaolin",
    "Kava",
    "Ketanserin",
    "Ketobemidone",
    "Ketoconazole",
    "Ketoconazole and other CYP3A4 inhibitors",
    "Ketotifen",
    "Lacosamide",
    "Lamivudine",
    "Lamotrigine",
    "Lanthanum",
    "Lapatinib",
    "Lasofoxifene",
    "Laxatives",
    "Leflunomide",
    "Lenalidomide",
    "Leukotriene antagonists",
    "Levamfetamine",
    "Levamisole",
    "Levetiracetam",
    "Levocarnitine",
    "Levodopa",
    "Levomepromazine",
    "Levosimendan",
    "Lidocaine",
    "Linezolid",
    "Liquorice",
    "Liraglutide",
    "Lithium",
    "Liv 52",
    "Local anaesthetics",
    "Loop diuretics",
    "Loperamide",
    "Loracarbef",
    "Loxapine",
    "Lumefantrine",
    "MAOIs",
    "MAOIs or RIMAs",
    "Macrolides",
    "Magnesium compounds",
    "Magnesium sulfate",
    "Mannitol",
    "Maprotiline",
    "Maraviroc",
    "Mazindol",
    "Mecamylamine",
    "Medroxyprogesterone",
    "Medroxyprogesterone or Megestrol",
    "Mefloquine",
    "Megestrol",
    "Melatonin",
    "Melperone",
    "Melphalan",
    "Memantine",
    "Menthol",
    "Meprobamate",
    "Mesuximide",
    "Metformin",
    "Methaqualone",
    "Methenamine",
    "Methotrexate",
    "Methoxsalen",
    "Methyldopa",
    "Methylnaltrexone",
    "Methylphenidate",
    "Metoclopramide",
    "Metoclopramide or Propantheline",
    "Metrifonate",
    "Metronidazole",
    "Metronidazole and related drugs",
    "Metyrapone",
    "Mexiletine",
    "Mexiletine or Tocainide",
    "Miconazole",
    "Mifepristone",
    "Milk",
    "Milk thistle",
    "Minocycline",
    "Minoxidil",
    "Mirtazapine",
    "Miscellaneous",
    "Misoprostol",
    "Mitomycin",
    "Mitotane",
    "Mizolastine",
    "Moclobemide",
    "Modafinil",
    "Molindone",
    "Monoclonal antibodies",
    "Monosodium glutamate",
    "Montelukast",
    "Moracizine",
    "Morphine",
    "Mosapride",
    "Moxisylyte",
    "Moxonidine",
    "Muscle relaxants",
    "Mycophenolate",
    "NNRTIs",
    "NRTIs",
    "NSAIDs",
    "NSAIDs or Aspirin",
    "NSAIDs or Salicylates",
    "Naloxone",
    "Naltrexone",
    "Nasal decongestants",
    "Nasal decongestants and related drugs",
    "Nateglinide or Repaglinide",
    "Nefazodone",
    "Nefazodone or Trazodone",
    "Nefopam",
    "Neomycin",
    "Neuromuscular blockers",
    "Niclosamide",
    "Nicorandil",
    "Nicotine",
    "Nifedipine",
    "Nilotinib",
    "Nitrates",
    "Nitrofurantoin",
    "Nitrosoureas",
    "Nitrous oxide",
    "Nitroxoline",
    "Nystatin",
    "Octreotide",
    "Oestrogens",
    "Olanzapine",
    "Omeprazole",
    "Ondansetron",
    "Opioids",
    "Orange juice",
    "Organophosphorus compounds",
    "Orlistat",
    "Oseltamivir",
    "Oseltamivir and Zanamivir",
    "Other antibacterials",
    "Other antiepileptics",
    "Other antimycobacterials",
    "Other antineoplastics",
    "Other drugs that affect blood pressure",
    "Other drugs that affect coagulation",
    "Other drugs that prolong the QT interval",
    "Other drugs with hyperglycaemic",
    "Oxaceprol",
    "Oxaliplatin",
    "Oxazepam",
    "Oxcarbazepine",
    "Oxiracetam",
    "Oxolamine",
    "Oxybutynin",
    "Oxygen",
    "Ozagrel",
    "PUVA",
    "Paliperidone",
    "Pancreatic enzymes",
    "Panitumumab",
    "Papaverine",
    "Paraldehyde",
    "Parathyroid hormones",
    "Paricalcitol",
    "Pemetrexed",
    "Penicillamine",
    "Penicillins",
    "Pentamidine",
    "Pentazocine",
    "Pentostatin",
    "Pentoxifylline",
    "Perospirone",
    "Phenelzine",
    "Pheneturide",
    "Phenmetrazine",
    "Phenobarbital",
    "Phenobarbital or Phenytoin",
    "Phenobarbital or Primidone",
    "Phenothiazines",
    "Phenoxybenzamine",
    "Phenylbutazone",
    "Phenylpropanolamine",
    "Phenytoin",
    "Phosphate binders",
    "Picotamide",
    "Pilocarpine",
    "Pimozide",
    "Pinaverium",
    "Pioglitazone or Rosiglitazone",
    "Piperazine",
    "Piracetam",
    "Pirenzepine",
    "Piribedil",
    "Pirmenol",
    "Pizotifen",
    "Pneumococcal vaccine",
    "Policosanol",
    "Polycarbophil calcium",
    "Polystyrene sulfonate",
    "Polyvalent cations",
    "Potassium compounds",
    "Pramipexole",
    "Pramlintide",
    "Prasugrel",
    "Praziquantel",
    "Prazosin",
    "Prednisolone",
    "Prednisone",
    "Pregabalin",
    "Primaquine",
    "Primidone",
    "Probenecid",
    "Probucol",
    "Procainamide",
    "Procarbazine",
    "Prochlorperazine",
    "Progabide",
    "Proguanil",
    "Prolintane",
    "Propafenone",
    "Propantheline",
    "Propofol",
    "Propranolol",
    "Prostaglandins",
    "Protease inhibitors",
    "Protionamide",
    "Proton pump inhibitors",
    "Proton pump inhibitors and other CYP2C19 inhibitors",
    "Pseudoephedrine",
    "Pseudoephedrine and related drugs",
    "Psoralens",
    "Pyrantel",
    "Pyrazinamide",
    "Pyridoxal",
    "Pyrimethamine",
    "Quetiapine",
    "Quinapril",
    "Quinidine",
    "Quinidine or Quinine",
    "Quinine",
    "Quinine and related drugs",
    "Quinolones",
    "Raloxifene",
    "Raltegravir",
    "Raltitrexed",
    "Ramelteon",
    "Ranitidine",
    "Ranolazine",
    "Rasagiline",
    "Rauwolfia alkaloids",
    "Rauwolfia alkaloids or Tetrabenazine",
    "Reboxetine",
    "Remacemide",
    "Repaglinide",
    "Reserpine",
    "Retapamulin",
    "Retigabine",
    "Retinoids",
    "Ribavirin",
    "Rifabutin",
    "Rifamycins",
    "Rifaximin",
    "Rimantadine",
    "Rimonabant",
    "Risperidone",
    "Ritanserin",
    "Ritodrine",
    "Ritonavir",
    "Rivaroxaban",
    "Roflumilast",
    "Ropinirole",
    "Rotigotine",
    "Royal jelly",
    "Rufinamide",
    "SNRIs",
    "SSRIs",
    "SSRIs and related antidepressants",
    "SSRIs or SNRIs",
    "Salicylates",
    "Schisandra",
    "Selenium",
    "Semaxanib",
    "Senna",
    "Serotonergic drugs",
    "Sertindole",
    "Sertraline",
    "Sevelamer",
    "Sibutramine",
    "Sirolimus",
    "Sirolimus and related drugs",
    "Sirolimus or Tacrolimus",
    "Sodium bicarbonate",
    "Sodium compounds",
    "Sodium edetate",
    "Sodium nitroprusside",
    "Sodium oxybate",
    "Somatostatin analogues",
    "Somatropin",
    "Sorafenib",
    "Sorbitol",
    "Sorivudine",
    "Spermicides",
    "Spiramycin",
    "Spironolactone",
    "Statins",
    "Stiripentol",
    "Streptozocin",
    "Strontium ranelate",
    "Succimer",
    "Sucralfate",
    "Sucrose polyesters",
    "Sugammadex",
    "Sulfasalazine",
    "Sulfinpyrazone",
    "Sulfiram",
    "Sulfonamides",
    "Sulfonylureas",
    "Sulpiride",
    "Sultiame",
    "Sunitinib",
    "Sympathomimetics",
    "Tacrine",
    "Tacrolimus",
    "Tacrolimus or Pimecrolimus",
    "Tadalafil",
    "Tamarindus indica",
    "Tamoxifen",
    "Tamoxifen or Toremifene",
    "Tamsulosin",
    "Taxanes",
    "Tegafur with Uracil",
    "Tegaserod",
    "Teicoplanin",
    "Telbivudine",
    "Temozolomide",
    "Temsirolimus",
    "Tenofovir",
    "Terbinafine",
    "Terbutaline",
    "Terfenadine",
    "Testosterone",
    "Tetrabenazine",
    "Tetracyclic antidepressants",
    "Tetracycline",
    "Tetracyclines",
    "Thalidomide",
    "Theophylline",
    "Theophylline or Diprophylline",
    "Thiazide diuretics",
    "Thiazolidinediones",
    "Thioctic acid",
    "Thiomersal",
    "Thiopurines",
    "Thiotepa",
    "Thrombin inhibitors",
    "Thrombolytics",
    "Thyroid hormones",
    "Thyroid hormones and Antithyroid drugs",
    "Tiabendazole",
    "Tiagabine",
    "Tianeptine",
    "Tibolone",
    "Ticlopidine",
    "Tiludronate",
    "Timolol",
    "Tioguanine",
    "Tiotixene",
    "Tirilazad",
    "Tizanidine",
    "Tobacco",
    "Tobacco or Cannabis",
    "Tobacco or Nicotine",
    "Tocainide",
    "Tolazoline",
    "Tolterodine",
    "Tolvaptan",
    "Topiramate",
    "Topotecan",
    "Toremifene",
    "Trabectedin",
    "Tramadol",
    "Tranylcypromine",
    "Trastuzumab",
    "Trazodone",
    "Tretinoin",
    "Trichloroethylene",
    "Tricyclic antidepressants",
    "Trientine",
    "Trifluoperazine",
    "Trimetaphan",
    "Trimetazidine",
    "Trimethoprim",
    "Triptans",
    "Troleandomycin",
    "Trospium",
    "Tryptophan",
    "Tumour necrosis factor antagonists",
    "Tyramine",
    "Ulinastatin",
    "Urapidil",
    "Uricosuric drugs",
    "Urinary acidifiers or alkalinisers",
    "Urinary alkalinisers",
    "Urinary antimuscarinics",
    "Vaccines",
    "Valaciclovir",
    "Valnoctamide",
    "Valproate",
    "Valspodar",
    "Vancomycin",
    "Vardenafil",
    "Varenicline",
    "Vasodilators",
    "Vasopressin",
    "Venlafaxine",
    "Verapamil",
    "Vidarabine",
    "Vigabatrin",
    "Viloxazine",
    "Vinca alkaloids",
    "Vinpocetine",
    "Vitamin E substances",
    "Vitamin K substances",
    "Vitamins",
    "Voriconazole",
    "Vorinostat",
    "Xanthines",
    "Yohimbine",
    "Zafirlukast",
    "Ziconotide",
    "Zidovudine",
    "Zileuton",
    "Zinc compounds",
    "Zinc sulphate",
    "Ziprasidone",
    "Zonisamide",
    "Zopiclone",
    "Zotepine"
]

client = Groq(api_key="PUT_YOUR_API_KEY_HERE")


class DrugQuery(BaseModel):
    drug_name: str

@app.post("/classify")
async def classify_drug(payload: DrugQuery):
    if not drug_list:
        raise HTTPException(status_code=400, detail="Drug list is empty. Please set it first.")
    
    # Format the drug list into a string for prompt
    drugs_str = ", ".join(f'"{drug}"' for drug in drug_list)
    
    system_message = (
        "You are a drug classification expert. Given a drug name, determine its class based on the provided list. "
        "If the drug is in the list, respond with the drug name. "
        "If the drug is not in the list but you can determine its class, respond with the class name. "
        "If the drug is not in the list and you cannot determine its class, respond with 'unknown'. "
        "Respond with ONLY the drug name or class name, no additional text."
    )
    
    user_message = f"Drug name: {payload.drug_name}\nAvailable drugs and classes: [{drugs_str}]"

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.1,
            max_tokens=100
        )
        # Extract response content from Groq API
        response_text = chat_completion.choices[0].message.content.strip()
        return {"drug_name": payload.drug_name, "classification": response_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class DrugInteractionQuery(BaseModel):
    drug1: str
    drug2: str

async def enhance_interaction_data(drug1, drug2, classification1, classification2, interaction_data):
    """Use LLM to enhance and structure the interaction data for better readability"""
    
    system_message = (
    "You are a pharmacology expert specializing in drug interactions. "
    "Provide a brief, clear explanation of the interaction in one paragraph, directly stating the clinical relevance and mechanism."
    "Keep it short and concise."
)
    
    # Limit the content to avoid sending too much data to the LLM
    max_word_count = 700
    original_content = interaction_data['content']
    words = original_content.split()
    
    if len(words) > max_word_count:
        limited_words = words[:max_word_count]
        limited_content = " ".join(limited_words) + "... [content truncated]"
    else:
        limited_content = original_content
    
    user_message = (
        f"Drug 1: {drug1} (Class: {classification1})\n"
        f"Drug 2: {drug2} (Class: {classification2})\n\n"
        f"Interaction Information:\n{limited_content}"
    )
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=500
        )
        
        enhanced_data = chat_completion.choices[0].message.content.strip()
        return enhanced_data
    except Exception as e:
        # If LLM processing fails, return the original data
        return f"Error enhancing interaction data: {str(e)}"

@app.post("/interaction")
async def get_drug_interaction(payload: DrugInteractionQuery):
    # Get classifications for both drugs
    drug1_class = await classify_drug(DrugQuery(drug_name=payload.drug1))
    drug2_class = await classify_drug(DrugQuery(drug_name=payload.drug2))
    
    # Try both combinations of drug names
    interaction_key1 = f"{payload.drug1} + {payload.drug2}"
    interaction_key2 = f"{payload.drug2} + {payload.drug1}"
    
    # Search for interaction in the data
    interaction = None
    for entry in drug_interactions:
        if entry["title"].lower() in [interaction_key1.lower(), interaction_key2.lower()]:
            interaction = entry
            break
    
    if interaction:
        # Process the interaction data through the LLM
        enhanced_interaction = await enhance_interaction_data(
            payload.drug1, 
            payload.drug2, 
            drug1_class["classification"], 
            drug2_class["classification"], 
            interaction
        )
        
        return {
            "drug1": {
                "name": payload.drug1,
                "classification": drug1_class["classification"]
            },
            "drug2": {
                "name": payload.drug2,
                "classification": drug2_class["classification"]
            },
            "interaction": {
                "title": interaction["title"],
                "content": interaction["content"],
                "page": interaction["page"],
                "enhanced_explanation": enhanced_interaction
            }
        }
    else:
        return {
            "drug1": {
                "name": payload.drug1,
                "classification": drug1_class["classification"]
            },
            "drug2": {
                "name": payload.drug2,
                "classification": drug2_class["classification"]
            },
            "interaction": None,
        } 