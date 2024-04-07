import requests

API_TOKEN = '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'

API_URL = "https://api-inference.huggingface.co/models/MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()

output = query({
    "inputs": '''net cash flow provide operating activity 7044 million 2016 increased 1547 million 2015 due primarily 1 improved operating performance 2 low supplier payment 2016 compare 2015 partially offset 1 impact excess tax benefit stock plan primarily due increased stock price 2 increase account receivable due increase sale primarily united state net cash flow provide operating activity 5497 million 2015 decreased 4726 million 2014 due primarily 1 7500 million upfront payment receive medtronic litigation settlement agreement 2 high bonus payout 2015 associated 2014 performance decrease partially offset 1 income tax payment 2245 million make 2014 related medtronic settlement 2 improved operating performance 2015 3 500 million charitable contribution make 2014 edward lifesciences foundation net cash use invest activity 2117 million 2016 consist primarily capital expenditures 1761 million 413 million acquisition intangible asset net cash use invest activity 3161 million 2015 consist primarily 3201 million net payment associate acquisition cardiaq capital expenditures 1027 million partially offset net proceeds investment 1196 million net cash use invest activity 6330 million 2014 consist primarily net purchase investment 5274 million capital expenditures 829 million net cash use financing activity 2685 million 2016 consist primarily purchase treasury stock 6623 million partially offset 1 net proceeds issuance debt 2221 million 2 proceeds stock plan 1033 million 3 excess tax benefit stock plan 643 million net cash use financing activity 1586 million 2015 consist primarily purchase treasury stock 2801 million partially offset 1 proceeds stock plan 872 million 2 excess tax benefit stock plan 413 million net cash use financing activity 1530 million 2014 consist primarily purchase treasury stock 3009 million partially offset 1 proceeds stock plan 1133 million 2 excess tax benefit stock plan 494 million include realization previously unrealized excess tax benefit summary contractual obligation commercial commitment december 31 2016 follow million''',
    "parameters": {"candidate_labels": ["Urgent", "Not Urgent"]},
})

print(output)