def clean_list(text_list):
    """Removes '\r\n' items and replaces '\xa0' with a space in all text elements."""
    return [text.replace("\xa0", " ") for text in text_list if text != '\r\n']

def list_to_string(cleaned_list, separator="-"):
    """Joins the cleaned list into a single string with a given separator."""
    return separator.join(cleaned_list)

# Input list
description = [
    'Our ALTs (Assistant Language Teachers) are a part of\xa0elementary, junior high, and\xa0high school\xa0communities\xa0all across Japan.', 
    '\r\n', 
    '\r\nIn your schools, you’ll\xa0work with Japanese teachers\xa0to facilitate smooth presentation of the school’s assigned\xa0English curriculum. This may include preparing worksheets, model pronunciation and reading, demonstration of target language dialogs and similar tasks.', 
    '\r\n', 
    '\r\nIn addition, ALTs are commonly asked to review and comment on students’ homework notebooks and other written work, as well as conducting one-to-one or small group progress assessments.', 
    '\r\n', 
    '\r\nBut the heart of the ALT position is so much more – aside from just being a\xa0language instructor\xa0you are also a\xa0cultural ambassador. Sharing your own background and culture becomes a canvas for using English and gives meaning to what your students are studying.', 
    '\r\n', 
    '\r\n“ALT”\xa0is a title coined by the Japanese Ministry of Education, Culture, Sports, Science and Technology (MEXT) to describe\xa0native-level speakers of English working in Japanese classrooms. As an Interac ALT, you are not a member of the schools’ staff but an employee of Interac, and therefore,\xa0you work under the guidance of Interac.'
]

# Apply functions
cleaned_description = clean_list(description)
final_string = list_to_string(cleaned_description)




print(final_string)