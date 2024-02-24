#################################################################
# FILE : moogle.py
# WRITER : Dori_Peleg , dori.plg , 207685306
# EXERCISE : intro2cs ex6 2024
# DESCRIPTION: Copying Google to sucsess
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED:
# NOTES: ...
#################################################################

import argparse
import search_functions

def call_crawl(arguments):
    """ returns a variable denoting how many times a page was linked to other
    pages. type: trafic_dic: dict[str,dict[str,int]]"""
    base_url, index, out_file = arguments
    search_functions.crawl(base_url,index,out_file)

def call_page_rank(arguments):
    """preforms the famous Google Page Rank algorithm"""
    iterations, dict_file, out_file = arguments
    search_functions.page_rank(iterations,dict_file,out_file)

def call_words_dict(arguments):
    """used to derive a dictionary with each word an the amount it shows up in each page"""
    base_url, index, out_file = arguments
    search_functions.words_dict(base_url,index,out_file)

def call_search(arguments):
    """preforms a search on the pages returns the pages ranked by the page_rank algorithm"""
    max_results = int(arguments.pop(-1))
    words_dict_file = arguments.pop(-1)
    ranking_dict_file = arguments.pop(-1)
    query = arguments
    search_functions.search(query,ranking_dict_file,words_dict_file,max_results)



if __name__ == "__main__":
    function_map = {
        'crawl': call_crawl,
        'page_rank': call_page_rank,
        'words_dict': call_words_dict,
        'search': call_search
    }
    parser = argparse.ArgumentParser()
    parser.add_argument( 'command', nargs=1 )
    parser.add_argument( 'args', nargs="*" )
    args= parser.parse_args()
    function = function_map[args.command[0]]
    function(args.args)