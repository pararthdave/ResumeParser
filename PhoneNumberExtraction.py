import re
import subprocess
import os
from pdfminer.high_level import extract_text
import phonenumbers


def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

def doc_to_text_catdoc(file_path):
    try:
        process = subprocess.Popen(  # noqa: S607,S603
            ['catdoc', '-w', file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
    except (
        FileNotFoundError,
        ValueError,
        subprocess.TimeoutExpired,
        subprocess.SubprocessError,
    ) as err:
        return (None, str(err))
    else:
        stdout, stderr = process.communicate()

    return (stdout.strip(), stderr.strip())

def extract_phone_number(resume_text):
    '''Accepts text as string and returns the first occurence of a phone number
    '''
    try:
        return list(iter(phonenumbers.PhoneNumberMatcher(text, None)))[0].raw_string.strip()
    except:
        try:
            return re.search(re.compile(r'(\+91)?(-)?\s*?(91)?\s*?(\d{3})-?\s*?(\d{3})-?\s*?(\d{4})'), resume_text).group().strip()
        except:
            return ""
        

if __name__ == '__main__':
    directory = 'Downloads/dataset/'

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        text = extract_text_from_pdf(f)
        phone_number = extract_phone_number(text)

        print(f," : ",phone_number)