import json, re, string

# with open('physics_topics.json', 'r') as infile:
#     data = json.load(infile)
#
# article_list = []
# for article in data:
#     page = wikipedia.page(article["topic"])
#     article_list.append({"topic": article["topic"], "content":page.content})
#
#
# with open('physics_training.json', 'w') as outfile:
#     json.dump(article_list, outfile)

with open('physics_training.json', 'r') as infile:
     data = json.load(infile)

article_list = []
for article in data:
    content = article["content"]
    content = (content.encode('ascii','ignore'))
    content = content.replace('\n', ' ')
    content = re.sub(' +',' ',content)
    # content = content.replace('\n','  ')
    # content = content.replace('  ','')

    p = re.compile(r'(\{.*\})?', re.MULTILINE)
    subst = ""
    content = re.sub(p, subst, content)

    p = re.compile(r'(\==.*\==)?', re.MULTILINE)

    content = re.sub(p, subst, content)

    exclude = string.punctuation.replace('.', '')
    content = ''.join(ch for ch in content if ch not in exclude)

    article_list.append({"topic": article["topic"], "content":content})

with open('physics_content.json', 'w') as outfile:
    json.dump(article_list, outfile)
