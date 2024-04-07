# Use a pipeline as a high-level helper
from transformers import pipeline

pipe = pipeline("summarization", model="facebook/bart-large-cnn")

input_str = '''['human capital management strategic imperative entergy engaged in a strategic imperative intended to optimize the organization through a process known as human capital management .'
 'in july 2013 management completed a comprehensive review of entergy 2019s organization design and processes .'
 'this effort resulted in a new internal organization structure , which resulted in the elimination of approximately 800 employee positions .'
 'entergy incurred approximately $ 110 million in costs in 2013 associated with this phase of human capital management , primarily implementation costs , severance expenses , pension curtailment losses , special termination benefits expense , and corporate property , plant , and equipment impairments .'
 'in december 2013 , entergy deferred for future recovery approximately $ 45 million of these costs , as approved by the apsc and the lpsc .'
 'see note 2 to the financial statements for details of the deferrals and note 13 to the financial statements for details of the restructuring charges .'
 'liquidity and capital resources this section discusses entergy 2019s capital structure , capital spending plans and other uses of capital , sources of capital , and the cash flow activity presented in the cash flow statement .'
 'capital structure entergy 2019s capitalization is balanced between equity and debt , as shown in the following table. .']'''
output = pipe(input_str)

print(output)