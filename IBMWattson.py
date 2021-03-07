import json
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

#Api Access
#Using latest version
authenticator = IAMAuthenticator('')
tone_analyzer = ToneAnalyzerV3(
    version='2017-09-21',
    authenticator=authenticator
)
#url corresponds to location closest
tone_analyzer.set_service_url('https://api.us-east.tone-analyzer.watson.cloud.ibm.com/instances/02ad5ad4-e149-4347-a67e-b94550f58e84')


text = ""
with open("Speech.txt", encoding="utf8") as f:
    for line in f:
        text += line


#json file from api
tone_analysis = tone_analyzer.tone(
    {'text': text},
    content_type='application/json'
).get_result()

#prints entire json file in a neat format
#print(json.dumps(tone_analysis, indent=2))

document_tone = tone_analysis["document_tone"]["tones"]
sentences_tone = tone_analysis["sentences_tone"]

#prints the tone score for the entire document
#scores range from 0.5-1.0
#scores under 0.0 will result in empty array
#scores above .75 are high accuracy
print("Document Tones\n")
for elements in document_tone:
    print("Tone Name: " + str(elements["tone_name"]))
    print("Score: " + str(elements["score"]) +" Percent: "+ str("{0:.0%}".format(elements["score"])))

    if(elements["score"] > 0.75):
        print("Accurate? : Yes")
    else:
        print("Accurate? : No")
    print("")
  
#prints the tone score for each setence in the document
#scores range from 0.5-1.0
#scores under 0.0 will result in empty array
#scores above .75 are high accuracy
print("Sentence Tones\n")
for index, elements in enumerate(sentences_tone, start=1):
    print(f"Sentence Number: {index}")
    print("Sentence: "+ elements["text"])
    if not elements["tones"]:
        print("Accurate? : Not Enough Data")
    else:
        for tones in elements["tones"]:
            print("Tone Name: " + tones["tone_name"])
            print("Score: " + str(tones["score"]) + " Percent: "+ str("{0:.0%}".format(tones["score"])))
            if(tones["score"] > 0.75):
                print("Accurate? : Yes")
            else:
                print("Accurate? : No")
    print("")


