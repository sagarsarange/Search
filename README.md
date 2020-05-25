# Search
Install all required libraries mentioned in `requirements.txt` file before performing following steps.
Command to install package: `pip install -r requirements.txt`.
 
1. `InvertedIndex.py` is used to build inverted index for the given file name.   
    Usage: `python InvertedIndex.py -d <corpus-file-path>`
    Example: `python InvertedIndex.py -d ./document/wiki_10`
    
    Three files namely `<filename>-structured-documents.json`, `<filename>-vector-squared-sum.json`, `<filename>-term-inverted-index.json` are generated. 
    
2. `Search.py` is the file used to search given search query in given inverted index file name and vector square sum file name.
    Usage: `python Search.py -i <inverted-index-file-name> -v <vector-squared-sum-file-name> -s "<search text>"`
