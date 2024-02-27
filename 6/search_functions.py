#################################################################
# FILE : additional_search_functions.py
# WRITER : Dori_Peleg , dori.plg , 207685306
# EXERCISE : intro2cs ex6 2024
# DESCRIPTION: The brain behind Moogle
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED:
# NOTES: ...
#################################################################


import bs4, requests, pickle
HEADERS = {'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def read_pickle(filename):
    """returns the stored data in a pickle file"""
    with open(filename, 'rb') as f:
        return pickle.load(f)

def write_pickle(data,path):
    """writes data onto a pickle file"""
    with open(path, 'wb') as f:
        pickle.dump(data,f)

def get_all_paragraphs(url):
    """gets all paragraphs from a certain page"""
    soup = bs4.BeautifulSoup(requests.get(url,headers=HEADERS).text,features="html.parser")
    return soup.find_all("p")

def crawl(base_url, index, out_file):
    """ returns a variable denoting how many times a page was linked to other
    pages. type: trafic_dic: dict[str,dict[str,int]]"""
    trafic_dic = {}
    file = open(index, "r",encoding= "utf-8")
    page_list = (file.read()).split()
    file.close()
    for page in page_list:
        temp_dict = dict.fromkeys(page_list,0)
        paragraphs = get_all_paragraphs(base_url+page)
        for p in  paragraphs:
            for links in p.find_all("a"):
                if links.get("href") in page_list:
                    temp_dict[links.get("href")] += 1
        trafic_dic[page] = {k: v for k, v in temp_dict.items() if v != 0}
    print(trafic_dic)
    write_pickle(trafic_dic,out_file)

def page_rank(iterations, dict_file, out_file):
    """preforms the famous Google Page Rank algorithm"""
    link_dic = read_pickle(dict_file)
    rank = dict.fromkeys(link_dic,1)
    for _ in range(int(iterations)):
        new_r = dict.fromkeys(rank,0)
        for page in rank.items():
            total = sum(list(link_dic[page[0]].values()))
            for inner_page in rank:
                try:
                    new_r[inner_page] += page[1]*(link_dic[page[0]][inner_page]/total)
                except:
                    new_r[inner_page] += 0
        rank = new_r
    write_pickle(rank,out_file)

def words_from_text(text: str, word_splitters: list= ['\n','\t','.',',','!','?',':','"',"'", " "]):
    """meant to derive a list of words, only words - in a text"""
    def split_list(string_list,char):
        new_list = []
        for string in string_list:
            new_list += string.split(char)
        return new_list
    word_list = [text]
    for i in word_splitters:
        word_list = split_list(word_list,i)
    return [i for i in word_list if i != '']

def item_repetiition_dic(item_list):
    """recieves a list of items and returns a dictionary with the amount 
    of repetitions for each item"""
    word_dic = {}
    for word in item_list:
        if word in word_dic:
            word_dic[word] += 1
        else:
            word_dic[word] = 1
    return word_dic

def words_dict(base_url, index, out_file):
    """used to derive a dictionary with each word an the amount it shows up in each page"""
    file = open(index, "r",encoding= "utf-8")
    page_list = (file.read()).split("\n")
    file.close()
    page_dic = {}
    word_dic = {}
    for page in page_list:
        paragraphs = get_all_paragraphs(base_url+page)
        word_list =[]
        for p in paragraphs:
            word_list += words_from_text(p.text,[" ","\n","\t"])
        page_dic[page] = item_repetiition_dic(word_list)
        for key in page_dic[page].items():
            if key[0] not in word_dic:
                word_dic[key[0]] = {}
            word_dic[key[0]][page] = key[1]
    write_pickle(word_dic, out_file)

def check_all_words_in(words_and_appearances: dict, words: list):
    """checks if all words in a list are in a dictionary"""
    all_words = True
    for word in words:
        if word not in words_and_appearances:
            all_words = False
    return all_words

def search(query, ranking_dict_file,words_dict_file,max_results):
    """preforms a search on the pages returns the pages ranked by the page_rank algorithm"""
    rank_dic, word_dic = read_pickle(ranking_dict_file),read_pickle(words_dict_file)
    if len(rank_dic)>0:
        page_and_rank_by_appearance = {}
        for page in rank_dic:
            try:
                appearances = [word_dic[phrase][page] for phrase in query]
            except:
                appearances = [1]
            page_and_rank_by_appearance[page] = rank_dic[page]*min(appearances)
        ranked_list = sorted(page_and_rank_by_appearance.items(), key=lambda x:x[1])
        for i in range(min(max_results,len(ranked_list))):
            print(ranked_list[-(1+i)][0],ranked_list[-(1+i)][1])
