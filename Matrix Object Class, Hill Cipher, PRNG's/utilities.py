"""
-------------------------------------
File: utilities.py
File description
utilities file used by almost all cipher implementations
-------------------------------------
Author:  Chandler Mayberry
Version  2021-09-18
-------------------------------------
"""
DICT_FILE = 'engmix.txt'
PAD = 'q'

'______________________________________________________________________________'

def get_base(base_type):
    """
    ---------------------------------------------------- 
    Parameters:   base_type (str) 
    Return:       result (str)
    Description:  Return a base string containing a subset of ASCII charactes
                  Defined base types:
                  lower, upper, alpha, lowernum, uppernum, alphanum, special, nonalpha, B6, BA, all
                      lower: lower case characters
                      upper: upper case characters
                      alpha: upper and lower case characters
                      lowernum: lower case and numerical characters
                      uppernum: upper case and numerical characters
                      alphanum: upper, lower and numerical characters
                      special: punctuations and special characters (no white space)
                      nonalpha: special and numerical characters
                      B6: num, lower, upper, space and newline
                      BA: upper + lower + num + special + ' \n'
                      all: upper, lower, numerical and special characters
    Errors:       if invalid base type, print error msg, return empty string
    ---------------------------------------------------
    """
    lower = "".join([chr(ord('a')+i) for i in range(26)])
    upper = lower.upper()
    num = "".join([str(i) for i in range(10)])
    special = ''
    for i in range(ord('!'),127):
        if not chr(i).isalnum():
            special+= chr(i)
            
    result = ''
    if base_type == 'lower':
        result = lower
    elif base_type == 'upper':
        result = upper
    elif base_type == 'alpha':
        result = upper + lower
    elif base_type == 'lowernum':
        result = lower + num
    elif base_type == 'uppernum':
        result = upper + num
    elif base_type == 'alphanum':
        result = upper + lower + num
    elif base_type == 'special':
        result = special
    elif base_type == 'nonalpha':
        result = special + num
    elif base_type == 'B6': #64 symbols
        result = num + lower + upper + ' ' + '\n'
    elif base_type == 'BA': #96 symbols
        result = upper + lower + num + special + ' \n'
    elif base_type == 'all':
        result = upper + lower + num + special
    else:
        print('Error(get_base): undefined base type')
        result = ''
    return result

'______________________________________________________________________________'

def get_language_freq(language='English'):
    """
    ----------------------------------------------------
    Parameters:   language (str): default = English 
    Return:       freq (list of floats) 
    Description:  Return frequencies of characters in a given language
                  Current implementation supports English language
                  If unsupported language --> print error msg and return []
    ---------------------------------------------------
    """
    if language == 'English':
        return [0.08167,0.01492,0.02782, 0.04253, 0.12702,0.02228, 0.02015,
                0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749,
                0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758,
                0.00978, 0.0236, 0.0015, 0.01974, 0.00074]
    else:
        print('Error(get_language_freq): unsupported language')
        return []
    
'______________________________________________________________________________'

def file_to_text(filename):
    """
    ----------------------------------------------------
    Parameters:   filename (str)
    Return:       contents (str)
    Description:  Utility function to read contents of a file
                  Can be used to read plaintext or ciphertext
    Asserts:      filename is a valid name
    ---------------------------------------------------
    """

    assert is_valid_filename(filename) == True, 'invalid input'
    
    #open the file to read using the open function.
    filetoread = open(filename, "r")
    
    #the contents will be the data within that file
    contents = filetoread.read()
    
    return contents;

'______________________________________________________________________________'

def text_to_file(text, filename):
    """
    ----------------------------------------------------
    Parameters:   text (str)
                  filename (str)            
    Return:       no returns
    Description:  Utility function to write any given text to a file
                  If file already exist, previous contents will be erased
    Asserts:      text is a string and filename is a valid filename
    ---------------------------------------------------
    """
    
    assert type(text) == str, 'invalid input'
    assert is_valid_filename(filename) == True, 'invalid input'
    
    #open the file that you want to write to
    filetowrite = open(filename, "w")
    
    #write the text that was sent to the method
    filetowrite.write(text);
    
    return

'______________________________________________________________________________'

def is_valid_filename(filename):
    """
    ----------------------------------------------------
    Parameters:   filename (str)
    Return:       True/False
    Description:  Checks if given input is a valid filename 
                  a filename should have at least 3 characters
                  and contains a single dot that is not the first or last character
    ---------------------------------------------------
    """
    filename_count = 0;
    i = 0;
    extension = False;
    is_valid = True

    #if filename.length is less than 4, xxx.c, then false 
    #if '.' is greater than 2, false.
    if len(filename) > 4 and filename.count('.') == 1:
            
        while (i < len(filename) and is_valid is True):
            
            char = filename[i];
            
            if extension == False:
                
                #increment the count for the length of the filename
                
                #checking for alphanumeric
                if char.isalnum() or char == "_":
                    filename_count+=1;
                                
                elif char == "." and filename_count <= 3:
                    is_valid = False;
                    extension = True;
            
            i+=1
            
        #check that it ends with a proper end
        ext = (".py", ".c", ".txt")
        if filename.endswith(ext) == False:
            is_valid = False
        
        #check that it doesnt start with .
        if filename.startswith('.') == True:
            is_valid = False
            
    else:
        is_valid = False
      
    return is_valid;

'______________________________________________________________________________'
   
def load_dictionary(dict_file=None):
    """
    ----------------------------------------------------
    Parameters:   dict_file (str): filename
                        default value = None
    Return:       dict_list (list): 2D list
    Description:  Reads a given dictionary file
                  dictionary is assumed to be formatted as each word in a separate line
                  Returns a list of lists, list 0 contains all words starting with 'a'
                  list 1 all words starting with 'b' and so forth.
                  if no parameter given, use default file (DICT_FILE)
    Errors:       if invalid filename, print error msg, return []
    ---------------------------------------------------
    """
    #Hint: for the function load_dictionary when opening the dictionary files use encoding="ISO-8859-15"
    
    dict_list = [[] for _ in range(26)];    
    
    #if the file name is none then default to DICT_FILE
    if dict_file is None:
        dict_file = DICT_FILE
    
    #verify that the filename that was sent is valid
    if is_valid_filename(dict_file) is False:
        print('Error(<load_dictionary): <filename not valid>')
        dict_list = []
        
    else:
        #running counter in the first index of 2d list
        #throw each word running from 'left to right' with starting letter 
        # EX. print("10th word starting with P = ",dict_list[15][9])
        
        file = open(dict_file, "r", encoding="ISO-8859-15")
        
        for word in file:
            
            word.lower()
            index = ord(word[0]) - 97
            inner_list = dict_list[index]
            inner_list.append(word.strip())
    
    file.close()
    return dict_list

'______________________________________________________________________________'

def text_to_words(text):
    """
    ----------------------------------------------------
    Parameters:   text (str)
    Return:       word_list (list)
    Description:  Reads a given text
                  Returns a list of strings, each pertaining to a word in the text
                  Words are separated by a white space (space, tab or newline)
                  Gets rid of all special characters at the start and at the end
    Asserts:      text is a string
    ---------------------------------------------------
    """
    
    assert type(text) is str, 'invalid input'
    
    #create list of characters    
    word_list = text.split()
    
    #delete the ALL special characters at the start and end of the word
    for i in range(len(word_list)):
        
        word = word_list[i]
        
        #end of word
        while len(word) > 0 and word[-1].isalnum() == False:
            word = word[:-1]
            #print(word)
            word_list[i] = word
        
        #start of word    
        while len(word) > 0 and word[0].isalnum() == False:
            word = word[1:]
            word_list[i] = word

    
    return word_list
    

'______________________________________________________________________________'

def analyze_text(text, dict_list):
    """
    ----------------------------------------------------
    Parameters:   text (str)
                  dict_list (list)
    Return:       matches (int)
                  mismatches (int)
    Description:  Reads a given text, checks if each word appears in given dictionary
                  Returns number of matches and mismatches.
                  Words are compared in lowercase
                  Assumes a proper dict_list
    Asserts:      text is a string and dict_list is a list
    ---------------------------------------------------
    """

    #assertions
    assert type(text) is str, 'invalid input'
    assert type(dict_list) is list, 'invalid input'

    matches = 0
    mismatches = 0
    
    #call text to words
    text = text.lower()
    word_list = text_to_words(text)
    
    #print(text)
    #print(word_list)
    
    #go through each word, grab index of first character
    for word in word_list:
        
        #print(word)
        
        #check if the word is the dictionary
        if len(word) > 0 and word[0].isalpha():
            index = ord(word[0]) - 97
            inner_list = dict_list[index]
            
            if word in inner_list:
                matches += 1
            else:
                #print('mismatch:', word)
                mismatches += 1
        
        #if the word is a number or is '' then it is a mismatch
        if len(word) == 0 or word[0].isalpha() is not True:
            #print('mismatch:', word)
            mismatches += 1
                
        
    #list traversal to find word
    
    
    return matches, mismatches
    
     
    

'______________________________________________________________________________'

def is_plaintext(text, dict_list, threshold=0.9):
    """
    ----------------------------------------------------
    Parameters:   text (str)
                  dict_list (list): dictionary list
                  threshold (float): number between 0 to 1
                      default value = 0.9
    Return:       True/False
    Description:  Check if a given file is a plaintext
                  If #matches/#words >= threshold --> True
                      otherwise --> False
                  If invalid threshold, set to default value of 0.9
                  An empty text should return False
                  Assumes a valid dict_list is passed
    ---------------------------------------------------
    """
    is_plaintext = True
    
    #if the input threshold is not between 0-1 then default
    if threshold > 1 and threshold < 0:
        threshold = 0.9
    
    
    if text == '':
        is_plaintext = False
        
    else:
        
        #get the number of matches
        matches = analyze_text(text, dict_list)
        
        #divide by the number of words in the list
        text = text.lower()
        word_list = text_to_words(text)
        number_of_words = len(word_list)
        
        #if less than the threshold than it is not plaintext
        if matches[0]/number_of_words < threshold:
            is_plaintext = False
    
    return is_plaintext

'______________________________________________________________________________'

def new_matrix(r,c,fill):
    """
    ----------------------------------------------------
    Parameters:   r: #rows (int)
                  c: #columns (int)
                  fill (str,int,double)
    Return:       matrix (2D List)
    Description:  Create an empty matrix of size r x c
                  All elements initialized to fill
                  minimum #rows and #columns = 2
                  If invalid value given, set to 2
    ---------------------------------------------------
    """
    #fill is a default value
    matrix = []
   
    #If invalid value given, set to 2
    if r < 2 or type(r) is not int:
        r = 2
    if c < 2 or type(c) is not int:
        c = 2
    
    #create matrix
    for _ in range(r):
        row = []
        
        for _ in range(c):
            row.append(fill)
        
        matrix.append(row)   
            
    
    
    return matrix

'______________________________________________________________________________'

def print_matrix(matrix):
    """
    ----------------------------------------------------
    Parameters:   matrix (2D List)
    Return:       -
    Description:  prints a matrix each row in a separate line
                  items separated by a tab
                  Assumes given parameter is a valid matrix
    ---------------------------------------------------
    """
    
    #print the matrix with proper formatting
    
    for i in range(len(matrix)):
        
        for j in matrix[i]:
            print('{}'.format(j), end='\t')
    
        print() #newline
    
    return None

'______________________________________________________________________________'

def index_2d(input_list,item):
    """
    ----------------------------------------------------
    Parameters:   input_list (list): 2D list
                  item (?)
    Return:       i (int): row number
                  j (int): column number
    Description:  Performs linear search on input list to find "item"
                  returns i,j, where i is the row number and j is the column number
                  if not found returns -1,-1
    Asserts:      input_list is a list
    ---------------------------------------------------
    """
    
    assert type(input_list) is list, 'invalid input'
    
    x = -1
    y = -1
    row = 0
    col = 0
    
    for i in input_list:
        row += 1
        for j in i:
            col += 1
            if j == item:
                x = row-1
                y = col-1
                break #no need to continue
        col = 0
    
    return x, y
'______________________________________________________________________________'

def shift_string(s,n,d='l'):
    """
    ----------------------------------------------------
    Parameters:   text (string): input string
                  shifts (int): number of shifts
                  direction (str): 'l' or 'r'
    Return:       update_text (str)
    Description:  Shift a given string by given number of shifts (circular shift)
                  If shifts is a negative value, direction is changed
                  If no direction is given or if it is not 'l' or 'r' set to 'l'
    Asserts:      text is a string and shifts is an integer
    ---------------------------------------------------
    """
    assert type(s) == str, 'invalid input'
    assert type(n) == int, 'invalid input'
    
    #set default
    if d != 'l' and d !='r' or d is None:
        d = 'l'
    
    #reduce number of shifts with known length of text for n > len(text)
    n = n%len(s)
    
    #switch directions of rotation if negative
    if d == 'l' and n < 0:
        d = 'r' 
        n = abs(n)
        
    elif d == 'r' and n < 0:
        d = 'l'
        n = abs(n)

    #perform shifting
    if d == 'l':
        
        #get the new right side string of left rotation
        new_right = s[0 : n] 
        
        #delete the old left side for left rotation
        new_left = s[n :] 
        
        s = new_left + new_right
        
    else:
        #delete the old right side for right rotation
        new_right = s[0 : len(s)-n] 
        
        #get the new left side string of right rotation
        new_left = s[len(s)-n : ]
        
        s = new_left + new_right
        
    return s

'______________________________________________________________________________'

def matrix_to_string(matrix):
    """
    ----------------------------------------------------
    Parameters:   matrix (2D List)
    Return:       text (string)
    Description:  convert a 2D list of characters to a string
                  from top-left to right-bottom
                  Assumes given matrix is a valid 2D character list
    ---------------------------------------------------
    """
    text = ''
    
    #traverse the matrix and append the char
    for i in matrix:
        for j in i:
            text += str(j)
            
    return text

'______________________________________________________________________________'

def get_positions(text,base):
    """
    ----------------------------------------------------
    Parameters:   text (str): input string
                  base (str):  stream of unique characters
    Return:       positions (2D list)
    Description:  Analyzes a given text for any occurrence of base characters
                  Returns a 2D list with characters and their respective positions
                  format: [[char1,pos1], [char2,pos2],...]
                  Example: get_positions('I have 3 cents.','c.h') -->
                      [['h',2],['c',9],['.',14]]
                  items are ordered based on their occurrence in the text
    Asserts:      text and base are strings
    ---------------------------------------------------
    """
    
    assert type(text) is str, 'invalid input'
    assert type(base) is str, 'invalid input'

    #make a list of the unique char
    unique_char = []
    
    for char in base:
        unique_char.append(char)
    
    '''i = 0
    print(base)
    for char in unique_char:
        print(i, char)
        i +=1'''
    
    #go through the characters in the text, get all occurrences
    positions = []
    index = 0
    for char in text:
        
        #if the char is inside of the unique_char list:
        if char in unique_char:
            insert = [char, index]
            #print(insert)
            positions.append(insert)
            
        index += 1
        
    
    return positions

'______________________________________________________________________________'

def clean_text(text,base):
    """
    ----------------------------------------------------
    Parameters:   text (str)
                  base (str)
    Return:       updated_text (str)
    Description:  Constructs and returns a new text which has
                  all characters in original text after removing base characters
    Asserts:      text and base are strings
    ---------------------------------------------------
    """
    assert type(text) is str, 'invalid input'
    assert type(base) is str, 'invalid input'
    
    #make a list of the unique char
    unique_char = []
    
    for char in base:
        unique_char.append(char)
    
    #go through the characters in the text
    for char in text:
        
        #if the char is inside of the unique_char list then delete it
        if char in unique_char:
            text = text.replace(char, '')
        
    
    return text
    

'______________________________________________________________________________'

def insert_positions(text, positions):
    """
    ----------------------------------------------------
    Parameters:   text (str)
                  positions (list): [[char1,pos1],[char2,pos2],...]]
    Return:       updated_text (str)
    Description:  Inserts all characters in the positions 2D list (generated by get_positions)
                  into their respective locations
                  Assumes a valid positions 2d list is given
    Asserts:      text is a string and positions is a list
    ---------------------------------------------------
    """
    assert type(text) is str, 'invalid input'
    assert type(positions) is list, 'invalid input'
    
    #for each item in positions, seperate the string and add the character positions
    for row in positions:
        text = text[:row[1]] + row[0] + text[row[1]:]
    
    return text

'______________________________________________________________________________'

def text_to_blocks(text, b_size, padding = False, pad =PAD):
    """
    ----------------------------------------------------
    Parameters:   text (str): input string
                  block_size (int)
                  padding (bool): False(default) = no padding, True = padding
                  pad (str): padding character, default = PAD
    Return:       blocks (list)
    Description:  Create a list containing strings each of given block size
                  if padding flag is set, pad empty blocks using given padding character
                  if no padding character given, use global PAD
    Asserts:      text is a string and block_size is a positive integer
    ---------------------------------------------------
    """
    assert type(text) is str, 'invalid input'
    assert type(b_size) is int and b_size>0, 'invalid input'
    
    count = 1
    temp = ''
    blocks = []
    
    for char in text:
        temp = temp + char
        
        if count == b_size:
            count = 1
            blocks.append(temp)
            temp = ''
            continue
        
        count += 1;
    
    if temp != '' and padding == False:
        blocks.append(temp)
    
    if temp != '' and padding == True:
        padding_length = b_size - len(temp)
        for _ in range(padding_length):
            temp = temp + pad
        blocks.append(temp)
        
    return blocks

'______________________________________________________________________________'

def blocks_to_baskets(blocks):
    """
    ----------------------------------------------------
    Parameters:   blocks (list): list of equal size strings
    Return:       baskets: (list): list of equal size strings
    Description:  Create k baskets, where k = block_size
                  basket[i] contains the ith character from each block
    Errors:       if blocks are not strings or are of different sizes -->
                    print 'Error(blocks_to_baskets): invalid blocks', return []
    ----------------------------------------------------
    """
    
    #get the length of a block, k
    k = len(str(blocks[0]))   
    
    #verify that blocks is a list
    if type(blocks) is str:
        print('Error(blocks_to_baskets): invalid blocks')
        return []
    
    #verify that the size of the blocks are equal, that all blocks are strings, 
    for block in blocks:
        if (type(block) is not str) or (len(block) != k):
            print('Error(blocks_to_baskets): invalid blocks')
            return []
    
    #create the basket and the basket word length variable
    baskets = []    
    basket_word_length = len(blocks)
    
    
    #print(k)
    #print(len(blocks))
    #print(basket_word_length)
    
    index = 0
    basket_text = ''
    while(index < k):
        
        for text in blocks:
            basket_text = basket_text + text[index] #create the basket_text with each char from blocks
            
            if len(basket_text) == basket_word_length: #if the basket_text is the right length, insert into baskets
                baskets.insert(index, basket_text)
                basket_text = ''
                
            #print(text[index])
        
        #print(temp)

        index += 1
        
    return baskets



'______________________________________________________________________________'

def compare_texts(text1,text2):
    """
    ----------------------------------------------------
    Parameters:   text1 (str)
                  text2 (str)
    Return:       matches (int)
    Description:  Compares two strings and returns number of matches
                  Comparison is done over character by character
    Assert:       text1 and text2 are strings
    ----------------------------------------------------
    """
    assert type(text1) is str, 'invalid input'
    assert type(text2) is str, 'invalid input'

    
    matches = 0
    
    if len(text1) < len(text2):
        index_length = len(text1)
    else:
        index_length = len(text2)
    
    for i in range(index_length):
        if text1[i] == text2[i]:
            matches += 1
    
    return matches

'______________________________________________________________________________'

def get_freq(text,base = ''):
    """
    ----------------------------------------------------
    Parameters:   text (str)
                  base (str): default = ''
    Return:       count_list (list of floats) 
    Description:  Finds character frequencies (count) in a given text
                  Default is English language (counts both upper and lower case)
                  Otherwise returns frequencies of characters defined in base
    Assert:       text is a string
    ----------------------------------------------------
    """
    assert type(text) is str, 'invalid input'
    
    count_list = [0] * len(base)
    
    index = 0;
    for cmp in base:
        
        for char in text:
            if char == cmp:
                count_list[index] = count_list[index] + 1
                
        index += 1
    return count_list

'______________________________________________________________________________'

def is_binary(b):
    """
    ----------------------------------------------------
    Parameters:   b (str): binary number
    Return:       True/False
    Description:  Checks if given input is a string that represent a valid
                  binary number
                  An empty string, or a string that contains other than 0 or 1
                  should return False
    ---------------------------------------------------
    """
    is_binary = False
    
    if type(b) is str and b != '' and b is not None:
        
        #convert the list to a unique set of char inside of the string
        set_of_char = set(b)
        
        #see if the set is '0', '1', or '0 and 1'
        if set_of_char == {'1', '0'} or set_of_char == {'1'} or set_of_char == {'0'}:
            is_binary = True
    
    return is_binary

'______________________________________________________________________________'

def bin_to_dec(b):
    """
    ----------------------------------------------------
    Parameters:   b (str): binary number
    Return:       decimal (int)
    Description:  Converts a binary number into corresponding integer
    Errors:       if not a valid binary number: 
                      print 'Error(bin_to_dec): invalid input' and return empty string
    ---------------------------------------------------
    """
    decimal = 0
    
    if is_binary(b) == False:
        print('Error(bin_to_dec): invalid input')
        return ''
    
    #run through the string backwards and multiply by the power and add if 1
    power = 0;
    for num in reversed(b):
        if num == '1':
            decimal += 2**(power)
            
        power+=1
        
        #print("$",num,"$")
        
    #we can also just use int(b)
    #decimal = int(b)
    
    
    return decimal

'______________________________________________________________________________'

def dec_to_bin(decimal,size=None):
    """
    ----------------------------------------------------
    Parameters:   decimal (int): input decimal number
                  size (int): number of bits in output binary number
                      default size = None
    Return:       binary (str): output binary number
    Description:  Converts any integer to binary
                  Result is to be represented in size bits
                  pre-pad with 0's to fit the output in the given size
                  If no size is given, no padding is done 
    Asserts:      decimal is an integer
    Errors:       if an invalid size:
                      print 'Error(dec_to_bin): invalid size' and return ''
                  if size is too small to fit output binary number:
                      print 'Error(dec_to_bin): integer overflow' and return ''
    ---------------------------------------------------
    """
    assert type(decimal) is int, 'invalid input'
    
    #size is invalid
    if (size is not None) and (type(size) is str or size <= 0):
        print ('Error(dec_to_bin): invalid size')
        return ''
    
    
    #init binary str
    """binary = ''
    if decimal == 0:
        binary =  '0'
    else:
        while decimal != 0:
            
            #we need to mod 2 as binary is of notation 2
            #if mod is 1 then it is a valid binary number
            #add from right to left
            
            if decimal%2 == 1 and binary == '0':
                binary = '1';
            
            elif decimal%2 == 1:
                binary = "1"+ binary 
            
            else:
                binary = "0" + binary
            
            decimal = decimal//2"""
    
    #turns out there is a built in
    binary = bin(decimal)
    binary = binary[2:]
    
    
    #pad the binary string if size is given
    if size is not None:
        add_size = int(size) - len(binary)
        
        if add_size >= 0:
            for _ in range(add_size):
                binary = '0' + binary
        
        else: #if the add size is below 0, then it is an invalid size error
            print('Error(dec_to_bin): integer overflow')
            return ''
        
        
    return binary

'______________________________________________________________________________'

def xor(a,b):
    """
    ----------------------------------------------------
    Parameters:   a (str): binary number
                  b (str): binary number
    Return:       decimal (int)
    Description:  Apply xor operation on a and b
    Errors:       if a or b is not a valid binary number 
                      print 'Error(xor): invalid input' and return ''
                  if a and b have different lengths:
                       print 'Error(xor): size mismatch' and return ''
    ---------------------------------------------------
    """
    
    #b6 is a 6 bit long binary number
    #0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ \n
    #10 + 26 + 26 + 1 + 1
    #error checks
    
    if is_binary(a) is False:
        print('Error(xor): invalid input')
        return ''
    
    if is_binary(b) is False:
        print('Error(xor): invalid input')
        return ''
    
    if len(a) != len(b):
        print('Error(xor): size mismatch')
        return ''
    
    
    #perform xor operation on the two binary numbers
    decimal = ''
    
    
    #XOR logic condition: if the two numbers are the same then 0, else, 1
    for i in range(len(a)):
        if a[i] == b[i]:
            decimal += "0"
        else:
            decimal += "1"
    
    return decimal

'______________________________________________________________________________'

def encode(c, code_type):
    """
    ----------------------------------------------------
    Parameters:   c (str): a character
                  code_type (str): ASCII or B6
    Return:       b (str): corresponding binary number
    Description:  Encodes a given character using the given encoding scheme
                  Current implementation supports only ASCII and B6 encoding
    Errors:       If c is not a single character:
                    print 'Error(encode): invalid input' and return ''
                  If unsupported encoding type:
                    print 'Error(encode): Unsupported Coding Type' and return ''
    ---------------------------------------------------
    """
    
    #error checking
    if type(c) is not str or len(c) != 1:
        print('Error(encode): invalid input')
        return ''

    
    #encode    
    b = ''
    
    if code_type == "ASCII":
        b = dec_to_bin(ord(c), 8)
    
    elif code_type == "B6":
        b6_str = get_base(code_type)
        #print(b6_str)
        position = get_positions(b6_str, c)
        
        #if the position isnt found then the character input is not B6
        """if position[0][1] is None:
            print('Error(encode): invalid input')
            return ''"""
                  
        index = position[0][1]
        
        
        #print(index)
        b = dec_to_bin(index, 6)
    
    else:
        print('Error(encode): Unsupported coding type')
        return ''
    
    return b

'______________________________________________________________________________'

def decode(b, code_type):
    """
    ----------------------------------------------------
    Parameters:   b (str): a binary number
                  code_type (str): ASCII or B6
    Return:       c (str): corresponding character
    Description:  Encodes a given character using the given encoding scheme
                  Current implementation supports only ASCII and B6 encoding
    Errors:       If b is not a binary number:
                    print 'Error(decode): invalid input' and return ''
                  If unsupported encoding type:
                    print 'Error(decode): unsupported Coding Type' and return ''
    ---------------------------------------------------
    """
    
    #error checking
    if is_binary(b) == False:
        print('Error(decode): invalid input')
        return ''
    
    if len(b) > 6 and code_type == "B6":
        print('Error(decode_B6): invalid input')
        return ''
    
    if len(b) > 8 and code_type == "ASCII":
        print('Error(decode): invalid input')
        return ''
    
    #decode
    c = ''    
    if code_type == "ASCII":
        c = chr(bin_to_dec(b))
        
    elif code_type == "B6":
        b6_str = get_base(code_type)
        index = bin_to_dec(b)
        c = b6_str[index]
        
    else:
        print('Error(decode): unsupported coding type')
        return ''
    
    
    return c
