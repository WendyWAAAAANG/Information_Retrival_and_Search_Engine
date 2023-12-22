from elasticsearch import Elasticsearch 
from elasticsearch_dsl import Search, Q

history = []
hotword = {}

def drugsearch(name="",typee=""):      
    es = Elasticsearch(hosts="http://elastic:changeme@localhost:9200/")
    if name:
    	history.insert(0,name)
    	q = Q("bool", should=Q("match", Name=name), minimum_should_match=1)  
    	s = Search(using=es, index="drugs").query(q)[0:20] 
    	response = s.execute()
    	print('Total %d hits found.' % response.hits.total.value)
    	    	
    	search = get_results(response)
    	recommend_array = []
    	if len(name) > 3:
            recommend = es.search(index = 'drugs', body = {'query':{'more_like_this':{'fields':['Name', 'Effect', 'Usage'], 'like': name[:3], 'analyzer': 'ik_smart', 'min_doc_freq': 2, 'min_term_freq': 1}}})
    	else:
            recommend = es.search(index = 'drugs', body = {'query':{'more_like_this':{'fields':['Name', 'Effect', 'Usage'], 'like': name[:3], 'analyzer': 'ik_smart', 'min_doc_freq': 2, 'min_term_freq': 1}}})
    	
    	for i in recommend['hits']['hits']:
    	    r = []
    	    r.append(i['_source']['Name'])
    	    r.append(i['_source']['Effect'])
    	    r.append(i['_source']['Usage'])
    	    r.append(i['_source']['Picture'])
    	    recommend_array.append(r)
    	    
    	print('recommend info:', recommend_array)
    	print(name[0])

    	for i in search:
    	    for j in recommend_array:
    	    	if i[0] == j[0]:
    	    	    recommend_array.remove(j)
    	    	else:
    	    	    continue
	
    	
    	suggestion = es.search(index = 'drugs', body={"suggest":{"term-suggestion":{"text":name,"term":{"field":"Name"}}}})
    	suggestion_array = []
    	
    	for i in suggestion['suggest']['term-suggestion'][0]['options']:
    		suggest = i['text']
    		suggestion_array.append(suggest)
    		
    	print("suggestion info:", suggestion)
    	
    	for i in set(history):
    		temp = history.count(i)
    		hotword[i] = temp
    	
    	hot = sorted(hotword.items(), key = lambda x:x[1], reverse = True)
    	
    	hotwords = []
    	for i in hot:
    		hotwords.append(list(i))
    		
    	return search, recommend_array, suggestion_array, history, hotwords, len(history), len(hotwords)
    	
    	
    	
    elif typee:
    	history.insert(0,typee)
    	q = Q("bool", should=Q("match", Type=typee), minimum_should_match=1)  
    	s = Search(using=es, index="drugs").query(q)[0:20] 
    	response = s.execute()
    	print('Total %d hits found.' % response.hits.total.value)
    	search = get_results(response)
    	
    	recommend = es.search(index = 'drugs', body = {'query':{'more_like_this':{'fields':['Type'], 'like': typee, 'analyzer': 'ik_smart', 'min_doc_freq': 2, 'min_term_freq': 1}}})
    	recommend_array = []
    	
    	for i in recommend['hits']['hits']:
    	    r = []
    	    r.append(i['_source']['Name'])
    	    r.append(i['_source']['Effect'])
    	    r.append(i['_source']['Usage'])
    	    r.append(i['_source']['Picture'])
    	    recommend_array.append(r)
    	
    	suggestion = es.search(index = 'drugs', body={"suggest":{"term-suggestion":{"text":typee,"term":{"field":"Type"}}}})
    	suggestion_array = []
    	
    	for i in suggestion['suggest']['term-suggestion'][0]['options']:
    		suggest = i['text']
    		suggestion_array.append(suggest)
    	
    	for i in set(history):
    		temp = history.count(i)
    		hotword[i] = temp
    	
    	hot = sorted(hotword.items(), key = lambda x:x[1], reverse = True)
    	
    	hotwords = []
    	for i in hot:
    		hotwords.append(list(i))
    	
    	return search, recommend_array, suggestion_array, history, hotwords, len(history), len(hotwords)
    else:
    	search = []
    	suggestion_array = []
    	recommend_array = []
    	hotwords = []
    	return search, recommend_array, suggestion_array, history, hotwords, len(history), len(hotwords)

def get_results(response): 
    results = []  
    for hit in response: 
        result_tuple = (hit.Name, str(hit.Price), hit.Effect,hit.Usage,hit.Picture,hit.Type,
        str(hit.Sale),str(hit.Number))    
        results.append(result_tuple)  
    return results
    
if __name__ == '__main__':  
    print("Drug name details:\n", drugsearch(name = "the"))
    print("Search results for name", sys.argv[1], ", type:", sys.argv[2], "\n", drugsearch(sys.argv[1], sys.argv[2]))
    #print("Drug type details:\n", drugsearch(type = "the"))
