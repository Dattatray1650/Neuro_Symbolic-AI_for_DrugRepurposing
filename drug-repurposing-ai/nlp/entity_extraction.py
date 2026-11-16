"""Clinical NLP — extracts entities from medical text using keyword + pattern matching.

Uses regex patterns and curated medical term lists as a lightweight alternative
to scispaCy (which requires large model downloads). Detects:
- Diseases / diagnoses
- Symptoms
- Medications
- Genes / biomarkers
- Lab values
- Negations and uncertainty markers
"""

import re
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

# ---------------------------------------------------------------------------
# Term dictionaries (curated subset of real biomedical terms)
# ---------------------------------------------------------------------------

DISEASE_PATTERNS = [
    # Neurodegenerative
    r"\balzheimer(?:'s)?\s*disease\b", r"\bparkinson(?:'s)?\s*disease\b",
    r"\bhuntington(?:'s)?\s*disease\b", r"\bamyotrophic lateral sclerosis\b", r"\bals\b",
    r"\bmultiple sclerosis\b", r"\bms\b",
    # Cancer
    r"\bbreast cancer\b", r"\blung cancer\b", r"\bcolorectal cancer\b",
    r"\bglioblastoma\b", r"\bleukemia\b", r"\blymphoma\b", r"\bmelanoma\b",
    r"\bpancreatic cancer\b", r"\bprostate cancer\b", r"\bovarian cancer\b",
    # Metabolic
    r"\btype\s*2\s*diabetes\b", r"\btype\s*1\s*diabetes\b", r"\bdiabetes mellitus\b",
    r"\bdiabetes\b", r"\bobesity\b", r"\bhyperlipidemia\b",
    # Cardiovascular
    r"\bheart failure\b", r"\bmyocardial infarction\b", r"\bcoronary artery disease\b",
    r"\bhypertension\b", r"\batrial fibrillation\b", r"\batherosclerosis\b",
    r"\bstroke\b",
    # Inflammatory / Autoimmune
    r"\brheumatoid arthritis\b", r"\blupus\b", r"\bcrohn(?:'s)?\s*disease\b",
    r"\bulcerative colitis\b", r"\bpsoriasis\b", r"\basthma\b", r"\bcopd\b",
    # Psychiatric
    r"\bdepression\b", r"\banxiety\s*disorder\b", r"\bschizophrenia\b",
    r"\bbipolar disorder\b",
    # Infectious
    r"\bcovid[-\s]*19\b", r"\btuberculosis\b", r"\bhiv\b", r"\bhepatitis\b",
    # Kidney / Liver
    r"\bchronic kidney disease\b", r"\bckd\b", r"\bchronic renal failure\b",
    r"\bliver cirrhosis\b", r"\bnon.alcoholic fatty liver\b", r"\bnafld\b",
]

SYMPTOM_PATTERNS = [
    r"\bmemory loss\b", r"\bcognitive decline\b", r"\bcognitive impairment\b",
    r"\btremor[s]?\b", r"\bbradykinesia\b", r"\brigidity\b",
    r"\bfatigue\b", r"\bweakness\b", r"\bdyspnea\b", r"\bshortness of breath\b",
    r"\bchest pain\b", r"\bpalpitation[s]?\b",
    r"\bnausea\b", r"\bvomiting\b", r"\bdiarrhea\b", r"\bconstipation\b",
    r"\bheadache[s]?\b", r"\bdizziness\b", r"\bseizure[s]?\b",
    r"\bjaundice\b", r"\bedema\b", r"\bweight loss\b", r"\banorexia\b",
    r"\bpolyuria\b", r"\bpolydipsia\b", r"\bpolyphagia\b",
    r"\bjoint pain\b", r"\barthralgia\b", r"\bmyalgia\b",
    r"\bdepressed mood\b", r"\banhedonia\b", r"\binsomnia\b",
    r"\bconfusion\b", r"\bdisorientation\b", r"\bparalysis\b",
]

MEDICATION_PATTERNS = [
    # Neurodegenerative
    r"\bdonepezil\b", r"\bmemantin[e]?\b", r"\brivastigmine\b", r"\bgalantamine\b",
    r"\blevodopa\b", r"\bcarbidopa\b", r"\bramipexole\b", r"\bropinirole\b",
    # Diabetes
    r"\bmetformin\b", r"\binsulin\b", r"\bglipizide\b", r"\bglibenclamide\b",
    r"\bsitagliptin\b", r"\bempagliflozin\b", r"\bliraglutide\b", r"\bsemaglutide\b",
    # Cardiovascular
    r"\batorvastatin\b", r"\brosuvastatin\b", r"\blisinopril\b", r"\bamlodipine\b",
    r"\bmetoprolol\b", r"\bwarfarin\b", r"\baspirin\b", r"\bapixaban\b",
    # Cancer
    r"\bimatinib\b", r"\btrastuzumab\b", r"\bpembrolizumab\b", r"\bnivolumab\b",
    r"\bpaclitaxel\b", r"\bdocetaxel\b", r"\bcisplatin\b", r"\bcarboplatin\b",
    # Autoimmune
    r"\bmethotrexate\b", r"\badalimumab\b", r"\betanercept\b", r"\binfliximab\b",
    r"\bprednisolone\b", r"\bprednisone\b",
    # Psychiatric
    r"\bsertraline\b", r"\bfluoxetine\b", r"\bescitalopram\b", r"\bolanzapine\b",
    r"\bquetiapine\b", r"\blithium\b",
    # Antibiotics / Antivirals
    r"\bamoxicillin\b", r"\bazithromycin\b", r"\btenofovir\b", r"\bremdesivir\b",
]

GENE_PATTERNS = [
    r"\bAPOE[- ]?(?:ε|e|epsilon)?[234]\b", r"\bAPOE\b",
    r"\bBRCA[12]\b", r"\bTP53\b", r"\bEGFR\b", r"\bKRAS\b", r"\bHER2\b",
    r"\bPTEN\b", r"\bRB1\b", r"\bMLH1\b", r"\bMSH2\b",
    r"\bPARK\d+\b", r"\bLRRK2\b", r"\bSNCA\b",
    r"\bCFTR\b", r"\bHBB\b", r"\bFMR1\b",
    r"\bACE2\b", r"\bTNF\b", r"\bIL-?6\b", r"\bIL-?1[Bb]\b",
    r"\bINSR\b", r"\bPPAR[Gg]\b",
]

BIOMARKER_PATTERNS = [
    r"\bHbA1c\b", r"\bblood glucose\b", r"\bfasting glucose\b",
    r"\bLDL\b", r"\bHDL\b", r"\btriglycerides?\b",
    r"\bcreatinine\b", r"\bGFR\b", r"\beGFR\b",
    r"\bALT\b", r"\bAST\b", r"\bALP\b",
    r"\bCRP\b", r"\bESR\b", r"\bWBC\b", r"\bRBC\b", r"\bhemoglobin\b",
    r"\bPSA\b", r"\bCA[\s-]?125\b", r"\bCA[\s-]?19[\s-]?9\b",
    r"\bamyloid[-\s]beta\b", r"\btau protein\b", r"\balpha[\s-]synuclein\b",
    r"\bCD4\b", r"\bviral load\b",
    r"\bINR\b", r"\bPT\b", r"\baPTT\b",
]

NEGATION_WORDS = [
    "no", "not", "without", "denies", "denied", "absent", "negative for",
    "no evidence of", "rules out", "ruled out", "never", "none",
    "no history of", "not consistent with",
]

UNCERTAINTY_WORDS = [
    "possible", "possibly", "probable", "probably", "likely", "suspected",
    "query", "question of", "cannot exclude", "may", "might", "could",
    "rule out", "differential", "consider",
]


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class Entity:
    text: str
    label: str           # DISEASE, SYMPTOM, MEDICATION, GENE, BIOMARKER
    start: int
    end: int
    negated: bool = False
    uncertain: bool = False
    normalized: Optional[str] = None


@dataclass
class ClinicalExtraction:
    diseases: List[Entity] = field(default_factory=list)
    symptoms: List[Entity] = field(default_factory=list)
    medications: List[Entity] = field(default_factory=list)
    genes: List[Entity] = field(default_factory=list)
    biomarkers: List[Entity] = field(default_factory=list)
    primary_disease: Optional[str] = None
    disease_confidence: str = "uncertain"   # confirmed / probable / uncertain


# ---------------------------------------------------------------------------
# Core extraction
# ---------------------------------------------------------------------------

def _check_negation(text: str, start: int) -> bool:
    """Check if the mention at `start` is preceded by a negation word."""
    window = text[max(0, start - 60):start].lower()
    for neg in NEGATION_WORDS:
        if neg in window:
            # Make sure the negation is on the same sentence
            last_period = window.rfind(".")
            if window.rfind(neg) > last_period:
                return True
    return False


def _check_uncertainty(text: str, start: int) -> bool:
    """Check if the mention at `start` is preceded by an uncertainty word."""
    window = text[max(0, start - 60):start].lower()
    for word in UNCERTAINTY_WORDS:
        if word in window:
            last_period = window.rfind(".")
            if window.rfind(word) > last_period:
                return True
    return False


def _extract_by_patterns(text: str, patterns: List[str], label: str) -> List[Entity]:
    """Extract entities from text using regex pattern list."""
    entities = []
    text_lower = text.lower()

    for pattern in patterns:
        for m in re.finditer(pattern, text_lower):
            # Get original-case text
            original = text[m.start():m.end()]
            negated = _check_negation(text, m.start())
            uncertain = _check_uncertainty(text, m.start())
            entities.append(Entity(
                text=original,
                label=label,
                start=m.start(),
                end=m.end(),
                negated=negated,
                uncertain=uncertain,
            ))

    # Deduplicate overlapping matches (keep longest)
    entities.sort(key=lambda e: (e.start, -(e.end - e.start)))
    deduped = []
    last_end = -1
    for ent in entities:
        if ent.start >= last_end:
            deduped.append(ent)
            last_end = ent.end

    return deduped


def extract_entities(text: str) -> ClinicalExtraction:
    """Extract all clinical entities from medical text.

    Args:
        text: Cleaned document text.

    Returns:
        ClinicalExtraction with all entity types.
    """
    if not text:
        return ClinicalExtraction()

    diseases   = _extract_by_patterns(text, DISEASE_PATTERNS, "DISEASE")
    symptoms   = _extract_by_patterns(text, SYMPTOM_PATTERNS, "SYMPTOM")
    medications = _extract_by_patterns(text, MEDICATION_PATTERNS, "MEDICATION")
    genes      = _extract_by_patterns(text, GENE_PATTERNS, "GENE")
    biomarkers = _extract_by_patterns(text, BIOMARKER_PATTERNS, "BIOMARKER")

    # Determine primary disease (first non-negated, non-uncertain disease)
    primary_disease = None
    disease_confidence = "uncertain"

    confirmed = [d for d in diseases if not d.negated and not d.uncertain]
    probable  = [d for d in diseases if not d.negated and d.uncertain]

    if confirmed:
        primary_disease = confirmed[0].text.title()
        disease_confidence = "confirmed"
    elif probable:
        primary_disease = probable[0].text.title()
        disease_confidence = "probable"
    elif diseases:
        # Even negated diseases are worth reporting as "negated"
        primary_disease = diseases[0].text.title()
        disease_confidence = "uncertain"

    return ClinicalExtraction(
        diseases=diseases,
        symptoms=symptoms,
        medications=medications,
        genes=genes,
        biomarkers=biomarkers,
        primary_disease=primary_disease,
        disease_confidence=disease_confidence,
    )


def to_dict(extraction: ClinicalExtraction) -> dict:
    """Convert ClinicalExtraction to JSON-serializable dict."""
    def ent_list(entities: List[Entity]) -> List[dict]:
        return [
            {
                "text": e.text,
                "label": e.label,
                "negated": e.negated,
                "uncertain": e.uncertain,
            }
            for e in entities
        ]

    return {
        "primary_disease": extraction.primary_disease,
        "disease_confidence": extraction.disease_confidence,
        "diseases": ent_list(extraction.diseases),
        "symptoms": ent_list([s for s in extraction.symptoms if not s.negated]),
        "medications": ent_list([m for m in extraction.medications if not m.negated]),
        "genes": ent_list(extraction.genes),
        "biomarkers": ent_list(extraction.biomarkers),
        "total_entities": (
            len(extraction.diseases) + len(extraction.symptoms) +
            len(extraction.medications) + len(extraction.genes) +
            len(extraction.biomarkers)
        ),
    }
