import sys

def highlight_doc(doc, query):
    """
    Args:
         doc - String that is a document to be highlighted
         query - String that contains the search query
    Returns:
         The the most relevant snippet with the query terms highlighted.
    """

    """
    As it appears to me, simply highlight individual words (in the set of the query words) in the input string is the most straightforward way but lack of good user-experience. 
    I intend to reduce this problem to "find all possible windows (to be highlighted) for an input sentence, where all of the required words appear in each window".
    Based on this definition, my algorithm goes through the doc (which denotes the input string) once (e.g.,  O(N)) and can output all such highlighted windows.
    
    
    Actually, my algorithm could be named as Earthworm-Moving algorithm (if you have ever see how a earthworm moves -- stretch and contract).     
    The idea is:
    -- use two arrays to store the number of required words (during preprocessing) and the words founded (during traversing doc);
    -- use two indexes i/j are used to denote the right/left bound of the current window;
    -- while traversing doc, each of the docword contributes to the "found" array (e.g., stretch stage by i+=1), and right after that, j is increased to throw out all unnecessary
       word from the current window (e.g., contract stage by j+=1)

    For simplicity, I only implemented the core algorithm. For further improvement, 
        -- semicolon/comma/colon/period/etc should be first replaced in doc
        -- fuzzy match should be supported, e.g., "dezp" should match "deep"
        -- after executing highlight_doc:
            -- neighbouring windows should merged, e.g.,  [[HIGHLIGHT]]ABC[[ENDHIGHLIGHT]][[HIGHLIGHT]]ABC[[ENDHIGHLIGHT]] => [[HIGHLIGHT]]ABCABC[[ENDHIGHLIGHT]]
            -- each window should "absorb" neighbouring words if they are in the set of the required words [[HIGHLIGHT]]ABC[[ENDHIGHLIGHT]]C => [[HIGHLIGHT]]ABCC[[ENDHIGHLIGHT]]
    """

    doc_words = doc.split()
    query_words = query.split();
    required={}
    for query_word in query_words:
        if(required.get(query_word)==None):
            required[query_word] = 1
        else:        
            required[query_word] +=1 
   
    found = {}
    
    #find a window contains all the required words
    i=-1
    j=0
    i_cache = [-1]
    j_cache = [-1]
    for doc_word in doc_words:
        i+=1
        if(required.get(doc_word)==None):   #irrelevant letters
            continue
        
        if(found.get(doc_word)==None):
            found[doc_word] =1
        else:
            found[doc_word] +=1
        
        #move the left bound rightward if possible
        while ((required.get(doc_words[j])==None) or (found[doc_words[j]] > required[doc_words[j]])) and (j<i):
            if (found.get(doc_words[j])!=None):
                found[doc_words[j]] -=1
            j+=1

        #check if all query words are in the current window 
        redflag = 0
        for query_word in query_words:
            if (found.get(query_word)==None) or (required[query_word] > found[query_word]):     #not satisfied
                redflag = 1                 #raise a redflag
                break 

        #found a window containing all words in query, try to see if it is minimum
        if (redflag == 0) and (j>i_cache[len(i_cache)-1]):   #I don;t like two windows to be overlapped
            i_cache.append(i)
            j_cache.append(j)

    #print and output
    cnt = 1;
    for index, doc_word in enumerate(doc_words):
        if (index==j_cache[cnt]):
            sys.stdout.write( "[[HIGHLIGHT]]" + doc_word + " ")
        elif(index==i_cache[cnt]):
            sys.stdout.write( doc_word + "[[ENDHIGHLIGHT]] " )
            if (cnt < len(j_cache)-1):
                cnt +=1
        else:
            sys.stdout.write( doc_word + " ")


if __name__ == "__main__":
    doc = "Little star's deep dish pizza sure is fantastic. Raullen likes deep (not that deep) dish pizza (really?)"
    query = "deep dish pizza"
    highlight_doc(doc, query)
