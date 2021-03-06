import json
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

import randomtest

# Api Access
# Using latest version
authenticator = IAMAuthenticator(
    'cfWZ9e9Dqi0mjjj6AfVqHo6reWDVCVZF9is5_pwEPMLv')
tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    authenticator=authenticator
)
# url corresponds to location closest
tone_analyzer.set_service_url(
    'https://api.us-east.tone-analyzer.watson.cloud.ibm.com/instances/02ad5ad4-e149-4347-a67e-b94550f58e84')


#return jsonfile of text
def text_to_analyze(text):
    # json file from api
    tone_analysis = tone_analyzer.tone(
        {'text': text},
        content_type='application/json'
    ).get_result()

    return tone_analysis

# prints the tone score for the entire document
# scores range from 0.5-1.0
# scores under 0.0 will result in empty array
# scores above .75 are high accuracy
def tone_of_document(text):
    document_tone = "Document Tone\n"
    for elements in text_to_analyze(text)["document_tone"]["tones"]:
        document_tone +=("Tone Name: " + str(elements["tone_name"]) + "\n")
        document_tone +=("Score: " + str(elements["score"]) +
              " Percent: " + str("{0:.0%}".format(elements["score"])) + "\n")

        if(elements["score"] > 0.75):
            document_tone +=("Accurate? : Yes\n")
        else:
            document_tone +=("Accurate? : No\n")
    return document_tone
# prints the tone score for each setence in the document
# scores range from 0.5-1.0
# scores under 0.0 will result in empty array
# scores above .75 are high accuracy


def tone_of_sentences(text):
    sentence_tone = "Sentence Tones\n"
    for index, elements in enumerate(text_to_analyze(text)["sentences_tone"], start=1):
        sentence_tone +=(f"Sentence Number: {index}\n")
        sentence_tone +=("Sentence: " + elements["text"] + "\n")
        if not elements["tones"]:
            sentence_tone +=("Accurate? : Not Enough Data\n")
        else:
            for tones in elements["tones"]:
                sentence_tone +=("Tone Name: " + tones["tone_name"] + "\n")
                sentence_tone +=("Score: " + str(tones["score"]) +
                      " Percent: " + str("{0:.0%}".format(tones["score"])) + "\n")
                if(tones["score"] > 0.75):
                    sentence_tone +=("Accurate? : Yes\n")
                else:
                    sentence_tone +=("Accurate? : No\n")
        sentence_tone += "\n"
    return sentence_tone

if __name__ == '__main__':
   
    text_to_analyze(tone_of_sentences(randomtest.millerscrape()[0]['transcript']))
    print(tone_of_document(randomtest.millerscrape()[0]['transcript']))
    print(tone_of_sentences(randomtest.millerscrape()[0]['transcript']))
