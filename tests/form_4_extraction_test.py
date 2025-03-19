import pytest
from common import extract


def test_form_4_standard_disposal():
    answer = [
        'Eschenbach Carl M. Workday, Inc. WDAY 20250307182858 Class A Common Stock 2025-03-05 None F 11084 D 253.63 627104 D'
    ]

    with open(r'workday_standard_disposal.xml') as file:
        xml_soup = extract.xml_to_soup(file)

    all_non_derivative_data = extract.extract_non_derivative_form_4_info(xml_soup)

    for i, non_derivative_data in enumerate(all_non_derivative_data):
        adjusted_non_derivative_data = ['None' if v is None else v for v in non_derivative_data]
        assert ' '.join(adjusted_non_derivative_data) == answer[i]


def test_form_4_multi_standard_acquisition():
    answer = [
        'Dodge R Stanton DraftKings Inc. DKNG 20250318200108 Class A Common Stock 2025-03-14 None S 49252 D 37.59 710145 D',
        'Dodge R Stanton DraftKings Inc. DKNG 20250318200108 Class A Common Stock 2025-03-14 None S 3525 D 38.05 706620 D',
        'Dodge R Stanton DraftKings Inc. DKNG 20250318200108 Class A Common Stock 2025-03-17 None S 52777 D 39 653843 D'
    ]

    with open(r'draftking_multi_disposal.xml') as file:
        xml_soup = extract.xml_to_soup(file)
    
    all_non_derivative_data = extract.extract_non_derivative_form_4_info(xml_soup)

    for i, non_derivative_data in enumerate(all_non_derivative_data):
        adjusted_non_derivative_data = ['None' if v is None else v for v in non_derivative_data]
        assert ' '.join(adjusted_non_derivative_data) == answer[i]


def test_RSU_acquisition():
    answer = []

    with open(r'jetblue_RSU_acquisition.xml') as file:
        xml_soup = extract.xml_to_soup(file)
    
    all_non_derivative_data = extract.extract_non_derivative_form_4_info(xml_soup)

    for i, non_derivative_data in enumerate(all_non_derivative_data):
        adjusted_non_derivative_data = ['None' if v is None else v for v in non_derivative_data]
        assert ' '.join(adjusted_non_derivative_data) == answer[i]

def test_RSU_disposal():
    answer = [
        'TRAVERS DAVID ZIPRECRUITER, INC. ZIP 20250318201444 Class A Common Stock 2025-03-15 None M 6250 A 0 1114607 D',
        'TRAVERS DAVID ZIPRECRUITER, INC. ZIP 20250318201444 Class A Common Stock 2025-03-15 None M 13347 A 0 1127954 D',
        'TRAVERS DAVID ZIPRECRUITER, INC. ZIP 20250318201444 Class A Common Stock 2025-03-15 None M 20691 A 0 1148645 D',
        'TRAVERS DAVID ZIPRECRUITER, INC. ZIP 20250318201444 Class A Common Stock 2025-03-15 None M 20444 A 0 1169089 D',
        'TRAVERS DAVID ZIPRECRUITER, INC. ZIP 20250318201444 Class A Common Stock 2025-03-15 None F 33148 D 5.96 1138960 D'
    ]

    with open(r'RSU_with_disposal.xml') as file:
        xml_soup = extract.xml_to_soup(file)
    
    all_non_derivative_data = extract.extract_non_derivative_form_4_info(xml_soup)

    for i, non_derivative_data in enumerate(all_non_derivative_data):
        adjusted_non_derivative_data = ['None' if v is None else v for v in non_derivative_data]
        assert ' '.join(adjusted_non_derivative_data) == answer[i]


def test_derivative_acquisition():
    answer = [
        'SOFTBANK GROUP CORP. Better Home & Finance Holding Co BETR 20250307210008 Class A Common Stock 2024-12-09 None C 628553 A None 628553 I'
    ]

    with open(r'softbank_derivative_acquisition.xml') as file:
        xml_soup = extract.xml_to_soup(file)
    
    all_non_derivative_data = extract.extract_non_derivative_form_4_info(xml_soup)

    for i, non_derivative_data in enumerate(all_non_derivative_data):
        adjusted_non_derivative_data = ['None' if v is None else v for v in non_derivative_data]
        assert ' '.join(adjusted_non_derivative_data) == answer[i]
