# Use a pipeline as a high-level helper
from transformers import pipeline

import requests

API_TOKEN = ''

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

pipe = pipeline("text-classification", model="mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")
pipe1 = pipeline("summarization", model="facebook/bart-large-cnn")

input_str = '''['the goldman sachs group , inc .'
 'and subsidiaries management 2019s discussion and analysis the table below presents our average monthly assets under supervision by asset class .'
 'average for the year ended december $ in billions 2017 2016 2015 .']
 ['operating environment .'
 'during 2017 , investment management operated in an environment characterized by generally higher asset prices , resulting in appreciation in both equity and fixed income assets .'
 'in addition , our long- term assets under supervision increased from net inflows primarily in fixed income and alternative investment assets .'
 'these increases were partially offset by net outflows in liquidity products .'
 'as a result , the mix of average assets under supervision during 2017 shifted slightly from liquidity products to long-term assets under supervision as compared to the mix at the end of 2016 .'
 'in the future , if asset prices decline , or investors favor assets that typically generate lower fees or investors withdraw their assets , net revenues in investment management would likely be negatively impacted .'
 'following a challenging first quarter of 2016 , market conditions improved during the remainder of 2016 with higher asset prices resulting in full year appreciation in both equity and fixed income assets .'
 'also , our assets under supervision increased during 2016 from net inflows , primarily in fixed income assets , and liquidity products .'
 'the mix of our average assets under supervision shifted slightly compared with 2015 from long-term assets under supervision to liquidity products .'
 'management fees were impacted by many factors , including inflows to advisory services and outflows from actively-managed mutual funds .'
 '2017 versus 2016 .'
 'net revenues in investment management were $ 6.22 billion for 2017 , 7% ( 7 % ) higher than 2016 , due to higher management and other fees , reflecting higher average assets under supervision , and higher transaction revenues .'
 'during the year , total assets under supervision increased $ 115 billion to $ 1.49 trillion .'
 'long- term assets under supervision increased $ 128 billion , including net market appreciation of $ 86 billion , primarily in equity and fixed income assets , and net inflows of $ 42 billion ( which includes $ 20 billion of inflows in connection with the verus acquisition and $ 5 billion of equity asset outflows in connection with the australian divestiture ) , primarily in fixed income and alternative investment assets .'
 'liquidity products decreased $ 13 billion ( which includes $ 3 billion of inflows in connection with the verus acquisition ) .'
 'operating expenses were $ 4.80 billion for 2017 , 3% ( 3 % ) higher than 2016 , primarily due to increased compensation and benefits expenses , reflecting higher net revenues .'
 'pre-tax earnings were $ 1.42 billion in 2017 , 25% ( 25 % ) higher than 2016 versus 2015 .'
 'net revenues in investment management were $ 5.79 billion for 2016 , 7% ( 7 % ) lower than 2015 .'
 'this decrease primarily reflected significantly lower incentive fees compared with a strong 2015 .'
 'in addition , management and other fees were slightly lower , reflecting shifts in the mix of client assets and strategies , partially offset by the impact of higher average assets under supervision .'
 'during 2016 , total assets under supervision increased $ 127 billion to $ 1.38 trillion .'
 'long-term assets under supervision increased $ 75 billion , including net inflows of $ 42 billion , primarily in fixed income assets , and net market appreciation of $ 33 billion , primarily in equity and fixed income assets .'
 'in addition , liquidity products increased $ 52 billion .'
 'operating expenses were $ 4.65 billion for 2016 , 4% ( 4 % ) lower than 2015 , due to decreased compensation and benefits expenses , reflecting lower net revenues .'
 'pre-tax earnings were $ 1.13 billion in 2016 , 17% ( 17 % ) lower than 2015 .'
 'geographic data see note 25 to the consolidated financial statements for a summary of our total net revenues , pre-tax earnings and net earnings by geographic region .'
 'goldman sachs 2017 form 10-k 63 .']
 '''

a = pipe1(input_str)
summary_text = a[0]['summary_text']
out = pipe(summary_text)

output = query({
    "inputs": summary_text,
    "parameters": {"candidate_labels": ["Enquiry", "Escalation", "Dissatisfaction", "Concern", "Random"]},
})

print(out[0]['label'])

max_score_index = output['scores'].index(max(output['scores']))

# Print the label corresponding to the maximum score
print("Label with highest score:", output['labels'][max_score_index])
#print(output)'''

