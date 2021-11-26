"""
-------------------------------------
File: Ciphers.py
File description
Columnar Transposition, Polybius, Simple substitution implementations
-------------------------------------
Author:  Chandler Mayberry
Version  2021-10-08
-------------------------------------
"""
import utilities

class Columnar_Transposition:
    """
    ----------------------------------------------------
    Cipher name: Columnar Transposition Cipher
    Key:         (str) a keyword
    Type:        Transposition Cipher
    Description: Constructs a table from plaintext, 
                 #columns = len(keyword)
                 Rearrange columns based on keyword order
                 Read the text vertically
                 Applies to all characters except whitespaces
    ----------------------------------------------------
    """
    
    DEFAULT_PAD = 'q'
    DEFAULT_PASSWORD = 'abcd'
    
    def __init__(self,key=DEFAULT_PASSWORD,pad=DEFAULT_PAD):
        """
        ----------------------------------------------------
        Parameters:   _key (str): default = abcd
                      _pad (str): a character, default = q
        Description:  Columnar Transposition constructor
                      sets _key and _pad
        ---------------------------------------------------
        """
        #set defaults
        self._key = self.DEFAULT_PASSWORD
        self._pad = self.DEFAULT_PAD
        
        if key != self.DEFAULT_PASSWORD:
            self.set_key(key)
        if pad != self.DEFAULT_PAD:
            self.set_pad(pad)
        
        return
            
    def get_key(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       key (str)
        Description:  Returns a copy of columnar transposition key
        ---------------------------------------------------
        """
        return self._key
    
    def set_key(self,key):
        """
        ----------------------------------------------------
        Parameters:   key (str): keyword
        Return:       success: True/False
        Description:  Sets key to given key
                      if invalid key --> set to default key
        ---------------------------------------------------
        """
        success = False
        if self.valid_key(key):
            self._key = key
            success = True
        else:
            self._key = self.DEFAULT_PASSWORD
            
        return success

    def __str__(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       output (str)
        Description:  Constructs and returns a string representation of 
                      Columnar Transposition object
                      output format:
                      Columnar Transposition Cipher:
                      key = <key>, pad = <pad>
        ---------------------------------------------------
        """
        output = "Columnar Transposition Cipher:\nkey = " + self.get_key() + ", pad = " + self.get_pad()
        return output
        
    def get_pad(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       pad (str): current padding character
        Description:  Returns a copy of current padding character
        ---------------------------------------------------
        """ 
        return self._pad
    
    def set_pad(self,pad):
        """
        ----------------------------------------------------
        Parameters:   pad (str): a padding character
        Return:       success: True/False
        Description:  Sets pad to given character
                      a pad should be a single character
                      if invalid pad, set to default value
        ---------------------------------------------------
        """ 
        success = False
        if  type(pad) == str and len(pad) == 1:
            self._pad = pad
            success = True
        else:
            self._pad = self.DEFAULT_PAD
            
        return success

    @staticmethod
    def valid_key(key):
        """
        ----------------------------------------------------
        Static Method
        Parameters:   key (?): an arbitrary input
        Returns:      True/False
        Description:  Check if given input is a valid Columnar Transposition key
                      A valid key is a string consisting of at least two unique chars
        ---------------------------------------------------
        """
        valid = False
        
        #make sure that there are at least two unqiue char, so if aa then false
        if type(key) == str and len(key) >= 2 and key.count(key[0]) != len(key):
            valid = True
        
        return valid
 
    @staticmethod
    def key_order(key):
        """
        ----------------------------------------------------
        Static Method
        Parameters:   key (str)           
        Return:       key_order (list)
        Description:  Returns key order
                      Example: [mark] --> akmr --> [1,3,0,2]
                      If invalid key --> return []
                      Applies to all ASCII characters from space to ~
                      Discards duplicate characters
        ----------------------------------------------------
        """  
        
        key_order = []
        
        if Columnar_Transposition.valid_key(key):
            
            #we need a string to hold the non-duplicate char
            unicodes_list = []
            no_duplicates = ''
            
            for char in key:
                
                #get the ascii value of the char, space takes priority
                if char != ' ':
                    unicode = ord(char)
                else:
                    unicode = 0
                
                if unicode not in unicodes_list:
                    #give characters a higher priority over special characters
                    #add 122 as z is the last ascii at 122, 122-126 are special char
                    if unicode != 0 and unicode < 65:
                        unicode += 122
                        
                    unicodes_list.append(unicode)
                    no_duplicates += char
                    
                    #print(no_duplicates)
                    
            #now that we have a list of letter priority:
            #convert back to letter now that its in order, and insert it into the key_order list
            unicodes_list.sort()
            
            for val_char in unicodes_list:
                #convert unicode value back to character
                if val_char == 0:
                    unicode = ' '
                elif val_char > 122:
                    unicode = chr(val_char-122)
                else:
                    unicode = chr(val_char)
                
                #find its position in the no_duplicates string, and append it into the key_order
                index = utilities.get_positions(no_duplicates, unicode)[0][1]
                key_order.append(index)
           
        else:
            #output is supposed to have a non-empty list when char is len(1) ( ex. [0] ) 
            if type(key) == str and len(key) == 1:
                key_order.append(0)
        
        return key_order

    def encrypt(self,plaintext):
        """
        ----------------------------------------------------
        Parameters:   plaintext (str)
        Return:       ciphertext (list)
        Description:  Encryption using Columnar Transposition Cipher
                      Does not include whitespaces in encryption
                      Uses padding
        Asserts:      plaintext is a string
        ----------------------------------------------------
        """
        assert type(plaintext) is str, 'invalid input'
        ciphertext = ''
        
        #get the order of keys and create a list to store the ciphertext
        key_order = Columnar_Transposition.key_order(self.get_key())
        ciphertext_list = ['' for _ in range(len(key_order))]
        
        #we need to keep track of the spaces and where they are placed within the text
        #so we can reintroduce them into the cipher text
        spaces = []
        space_position = 0
        
        i = 0
        for char in plaintext:
            
            if char == ' ':
                spaces.append([' ',space_position])
            
            else:
                #insert the char into a list, the length of the key_order
                ciphertext_list[i] += char
                
                #if at the length of key_order, then reset column
                if (i + 1) % (len(key_order)) == 0 and i != 0:
                    i = 0;
        
                else: 
                    i += 1;
                    
            #print(ciphertext_list)
            space_position += 1 #running counter of space index
        
        #insert pads where column isn't the same size of the number of keys
        pad = self.get_pad()
        while i % len(key_order) != 0:
            ciphertext_list[i] += pad
            #print(ciphertext_list)
            i += 1
        
        print(key_order)
        #create ciphertext in correct order of key with scrambled ciphertext_list
        for i in key_order:
            ciphertext += ciphertext_list[i]
        ciphertext = utilities.insert_positions(ciphertext, spaces)
       
        return ciphertext


    def decrypt(self,ciphertext):
        """
        ----------------------------------------------------
        Parameters:   ciphertext (str)
        Return:       plaintext (list)
        Description:  Decryption using Columnar Transposition Cipher
        Asserts:      ciphertext is a string
        ----------------------------------------------------
        """
        assert type(ciphertext) is str, 'invalid input'
        plaintext = ''
        
        key_order = Columnar_Transposition.key_order(self.get_key())
                
        #get length of the ciphertext without spaces
        text_char_length = 0
        for item in ciphertext.split():
            text_char_length += len(item)
        
        #calculate number of rows by dividing textcount by columns(size)
        n_rows = int(text_char_length / len(key_order))
        if text_char_length % len(key_order) != 0: 
            n_rows += 1;
        
        #create a new padded matrix of size n 
        pad = self.get_pad()
        plaintext_list = utilities.new_matrix(len(key_order), n_rows, pad)
        
        #we need to keep track of the spaces and where they are placed within the text
        #so we can reintroduce them into the plaintext text
        spaces = []
        space_position = 0
        
        #insert the ciphertext into the columns to reverse to plaintext
        row = 0
        col = 0
        for char in ciphertext:
            
            if char == ' ':
                spaces.append([' ', space_position])
                
            else:
                plaintext_list[row][col] = char
                
                if col == n_rows - 1:
                    col = 0
                    row += 1
                    
                else: 
                    col += 1
                    
            space_position += 1
            
        
        #read the matrix in the key_order to get the plaintext output 
        for col in range(n_rows):
            for i in range(len(key_order)):
                row = key_order.index(i)
                plaintext += plaintext_list[row][col]
        
        #reintroduce the spaces and strip the padding
        plaintext = utilities.insert_positions(plaintext, spaces)
        plaintext = plaintext.rstrip(pad)
        
        return plaintext




class Polybius:
    """
    ----------------------------------------------------
    Cipher name: Polybius Square Cipher (205-123 BC)
    Key:         tuple(start_char,size)
    Type:        Substitution Cipher
    Description: Substitutes every character with two digit number [row#][column#]
                 Implementation allows different square sizes with customized start ASCII char
                 Default square is 5x5 starting at 'a' and ending in 'y' (z not encrypted)
                 Encrypts/decrypts only characters defined in the square
    ----------------------------------------------------
    """
    
    DEFAULT_KEY = ('a',5)

    def __init__(self,key=DEFAULT_KEY):
        """
        ----------------------------------------------------
        Parameters:   _key (str): default = ('a',5)
        Description:  Polybius Cipher constructor
                      sets _key
        ---------------------------------------------------
        """
    
        self._key = self.DEFAULT_KEY
        if key != self.DEFAULT_KEY:
            self.set_key(key)
            
        return

    def get_key(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Returns:      key (tuple)
        Description:  Returns a copy of current key
        ---------------------------------------------------
        """
        return self._key
    
    @staticmethod
    def valid_key(key):
        """
        ----------------------------------------------------
        Static Method
        Parameters:   key (?): an arbitrary input
        Returns:      True/False
        Description:  Check if given input is a valid Polybius key
                      A valid key is a tuple with two elements
                      First element (start_char) is a single ASCII character
                      Second element (size) is an integer
                      The start_char should be an ASCII value between space and ~
                      The size should be an integer in the range [2,9]
                      The combination of start_char and size should not result in
                      a string that is beyond the ASCII range of [' ', '~']
        ---------------------------------------------------
        """
        
        valid = False
        #key meets above conditions
        if (type(key) is tuple and len(key) == 2) and ((type(key[0]) == str and len(key[0]) == 1) and (type(key[1]) == int)) and ((ord(key[0]) >= 32 
        and ord(key[0]) <= 126) and (key[1] >= 2 and key[1] <= 9)) and (ord(key[0]) + key[1]**2 -1 <= ord('~')):
            valid = True
            
        return valid
    
    def get_square(self, mode='list'):
        """
        ----------------------------------------------------
        Parameters:   mode(str)= 'list' or 'string'
        Returns:      square (2D list)
        Description:  Constructs Polybius square from key
                      Square can be returned as a 2D list or
                      as a string formatted as a matrix
        Errors:       if mode is not 'list' or 'string'
                          print error_msg: 'Error(Polybius.get_square): undefined mode'
                          return empty string
        ---------------------------------------------------
        """
        xy = self.get_key()[1]
        fill_string = self._get_base()
        
        #create a new square table from width_height
        square = utilities.new_matrix(xy, xy, '')
        
        i = 0
        for row in range(xy):
            for col in range(xy):
                square[row][col] = fill_string[i]
                i += 1
                
                
        #figure out what to return depending on the mode:
        #if string, then convert the matrix to string format otherwise return
        if mode == 'string':
            square_string = ''
            
            for row in range(len(square)):
                for char in square[row]:
                    square_string += char + '  '
                square_string += '\n'
            
            square_string = square_string.rstrip('\n')
            return square_string
            
        elif mode != 'list' and mode != 'string':
            print('Error(Polybius.get_square): undefined mode')
            return ''
        
        return square
    
    def _get_base(self):
        """
        ----------------------------------------------------
        A private helper function that returns the characters defined
        in the Polybius square as a single string
        String begins with start_char and ends with key*key subsequent chars
        ---------------------------------------------------
        """
        
        polybius_fill_string = ''
        
        starting_char, height = self.get_key()
        square = height**2 #size of square
        start = ord(starting_char) #starting unicode
        
        #get all characters between starting character to end of square
        for i in range(start, start + square):
            polybius_fill_string += chr(i)
               
        return polybius_fill_string

    
    def set_key(self,key):
        """
        ----------------------------------------------------
        Parameters:   key (tuple)
        Returns:      success (True/False)
        Description:  Sets Polybius object key to given key
                      Does not update key if invalid key
                      Returns success status: True/False
        ---------------------------------------------------
        """
        success = False
        if Polybius.valid_key(key):
            self._key = key
            success = True
        
        return success
    
    def __str__(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       output (str): string representation
        Description:  Returns a string representation of polybius
                      Format:
                      Polybius Cipher:
                      key = <key>
                      <polybius_square in matrix format>
        ---------------------------------------------------
        """
        output = 'Polybius Cipher:\nkey = ' + str(self.get_key()) + '\n' + self.get_square('string')
        return output
        
    
    def encode(self, plainchar):
        """
        -------------------------------------------------------
        Parameters:   plainchar(str): single character
        Return:       cipher(str): two digit number
        Description:  Substitutes a character with corresponding two numbers
                          using the defined Polybius square
                      If character is not defined in square return ''
        Errors:       if input is not a single character --> 
                         msg: 'Error(Polybius.encode): invalid input'
                         return empty string
        -------------------------------------------------------
        """
        cipher = ''
        poly_square = self.get_square()
        
        if type(plainchar) is str and len(plainchar) == 1:
            #if the plainchar is within the start and end char then perform encoding
            if plainchar in self._get_base():
                #get the index of the plainchar from the square
                row, col = utilities.index_2d(poly_square, plainchar)
                #as long as row != -1 that means it was found, +1 as polybius starts at row=1, col=1
                if row != -1:
                    cipher = str(row+1) + str(col+1)
        else:
            print('Error(Polybius.encode): invalid input')
            cipher = ''
            
        return cipher


    def decode(self, cipher):
        """
        -------------------------------------------------------
        Parameters:   cipher(str): two digit number
        Return:       plainchar(str): a single character
        Description:  Substitutes a two digit number with a corresponding char
                          using the defined Polybius square
                      If invalid two digit number return empty string
        Errors:       if input is not string composing of two digits  --> 
                         msg: 'Error(Polybius.decode): invalid input'
                         return empty string
        -------------------------------------------------------
        """
        plainchar = ''
        
        if type(cipher) is str and cipher.isdigit() and len(cipher) == 2:
            poly_square = self.get_square()
            
            row = int(cipher[0])-1
            col = int(cipher[1])-1
            
            #if the row and column are within the size of the square
            if row <= self.get_key()[1]-1 and col <= self.get_key()[1]-1:
                #if they are both greater than or equal to 0 (non-negative)
                if row >= 0 and col >= 0:
                    plainchar = poly_square[row][col]
        
        else:
            print('Error(Polybius.decode): invalid input')
        
        return plainchar
    
    def encrypt(self,plaintext):
        """
        ----------------------------------------------------
        Parameters:   plaintext (str)
        Return:       ciphertext (list)
        Description:  Encryption using Polybius cipher
                      Encrypts only characters defined in the square
        Asserts:      plaintext is a string
        ----------------------------------------------------
        """
        assert type(plaintext) is str, 'invalid input'
        ciphertext = ''
        
        #encode all of the characters in the plaintext given
        for char in plaintext:
            cipher_char = self.encode(char)
            
            if cipher_char != '':
                ciphertext += cipher_char
            
            #if the ciphertext is '' then it cant be encoded, just add the char    
            else:
                ciphertext += char
                
        return ciphertext

    def decrypt(self,ciphertext):
        """
        ----------------------------------------------------
        Parameters:   ciphertext (str)
        Return:       plaintext (list)
        Description:  decryption using Polybius cipher
                        decrypts only 2 digit numbers
        Asserts:      ciphertext is a string
        ----------------------------------------------------
        """
        assert type(ciphertext) is str, 'invalid input'
        plaintext = ''
        
        cipher_digit = ''
        for char in ciphertext:
            
            #check if the char is a digit or a string,
            #if its a string it wasnt encoded and can be directly added
            if char.isdigit() is False:
                
                if len(cipher_digit) == 1:
                    plaintext += cipher_digit
                
                cipher_digit = ''
                plaintext += char
                
            
            #if its a digit then add to the cipher digit
            else:
                cipher_digit += char
            
            #if cipher digit is 2 then we can decode and add it to the plaintext
            if len(cipher_digit) == 2:
                decoded = Polybius.decode(self, cipher_digit)
                if decoded != '':
                    plaintext += decoded
                
                cipher_digit = ''
                
        return plaintext + cipher_digit

    @staticmethod
    def cryptanalyze(ciphertext,args=['',0,0,None,0.93]):
        """
        ----------------------------------------------------
        Static method
        Parameters:   ciphertext (string)
                      args (list):
                            start_char: (str): default = ''
                            min_size: (int): default = 0
                            max_size: (int): default = 0
                            dictionary_file (str): default = None
                            threshold (float): default = 0.93
        Return:       key,plaintext
        Description:  Cryptanalysis of Polybius Cipher
                      Returns plaintext and key (start_char,size)
                      Assumes user passes a valid args list
                      Uses bruteforce for the sizes is in range [min_size,max_size]
                      The square is always located between [' ', '~'] ASCII characters
        ---------------------------------------------------
        """
        plaintext = ''
        key = ''
        start_char, min_size, max_size, dictionary_file, threshold = args        
        dict_list = utilities.load_dictionary(dictionary_file)
        
        #to end of ascii if null
        if max_size == 0:
            max_size = ord('~')
        
        keyfound = False
        run = True
        
        #we need to keep the start_char unchanged for running_char brute force condition
        if start_char != '':
            running_char = start_char
        else:
            running_char = ' '
            
        #we need to iterate through every possible size, for each char from min->max
        while run == True and keyfound == False:
            
            for n in range(min_size, max_size + 1):
                
                new_obj = (running_char, n)
                polyobj = Polybius(new_obj)
                plaintext = polyobj.decrypt(ciphertext)
                
                keyfound = utilities.is_plaintext(plaintext, dict_list, threshold) 
                if keyfound:
                    key = (running_char, n)
                    break
            
            #move to the next character to test in for loop, as long as end isnt hit and start isnt given
            if start_char == '' and running_char != '~':
                next_char = ord(running_char)
                running_char = chr(next_char+1)
                #print(running_char)
            else: 
                run = False

        #failure check
        if keyfound is False:
            print('Polybius.cryptanalyze: cryptanalysis failed')
            key = ''
            plaintext = ''
            
        return key, plaintext




class Simple_Substitution:
    """
    ----------------------------------------------------
    Cipher name: Simple Substitution Cipher
    Key:         tuple(keyword(str),base(str))
    Type:        Substitution Cipher
    Description: The base is a stream of unique characters
                 Only characters defined in the base are substituted
                 The base is case insensitive
                 The keyword is a random arrangement of the base, or some of its characters
                 The substitution string is the keyword, then all base characters
                     not in keyword, while maintaining their order in the base
                 The case of characters should be preserved whenever possible
    ----------------------------------------------------
    """
    DEFAULT_KEY = ('frozen','abcdefghijklmnopqrstuvwxyz')

    def __init__(self,key=DEFAULT_KEY):
        """
        ----------------------------------------------------
        Parameters:   _key (str)
        Description:  Simple Substitution Cipher constructor
                      sets _key
        ---------------------------------------------------
        """
        self._key = self.DEFAULT_KEY
        if key != self.DEFAULT_KEY:
            self.set_key(key)
        return

    def get_key(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Returns:      key (tuple)
        Description:  Returns a copy of current key
        ---------------------------------------------------
        """
        return self._key
    
    @staticmethod
    def valid_key(key):
        """
        ----------------------------------------------------
        Static Method
        Parameters:   key (?): an arbitrary input
        Returns:      True/False
        Description:  Check if given input is a valid Simple Substitution key
                      The key is a tuple composing of two strings
                      The base should contain at least two unique characters
                      The keyword should have at least two unique characters defined in the base
        ---------------------------------------------------
        """
        success = False
        
        #if the key is a tuple of length 2, the keyword/base are strings greater than 2 then:
        if (type(key) is tuple and len(key) == 2) and (type(key[0]) is str and 
        type(key[1]) is str) and (len(key[1]) >= 2 and key[1].count(key[1][0]) != len(key[1])):
            
            keyword = key[0]
            base = key[1]
            
            #need to put in lower case for char comparision
            keyword = keyword.lower()
            base = base.lower()
            
            temp = []
            similarities = 0
            
            #find the similarities of characters in keyword to characters in base
            #ie. keyword has at least two unique characters defined in base
            for char in keyword:
                if char not in temp and char in base:
                    similarities += 1
                    temp.append(char)
                if similarities > 1:
                    success = True
            
        return success
    
    def get_table(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Returns:      [base,sub]
        Description:  Constructs a substitution table
                      First element is the base string
                      Second element is the substitution string 
        ---------------------------------------------------
        """
        (keyword, base) = self.get_key()
        
        sub_string = keyword
        
        #add all char in base that are not already in the sub_string
        for char in base:
            if char not in sub_string:
                sub_string += char
        
        return [base, sub_string]
    
    def set_key(self,key):
        """
        ----------------------------------------------------
        Parameters:   key (tuple(str,str))
        Returns:      success (True/False)
        Description:  Sets Simple Substitution key to given key
                      Does not update key if invalid key
                      Stores key without duplicates in lower case
                          duplicates in base are removed
                          duplicates in keyword are removed
                          keyword chars not in base are removed
                      Returns success status: True/False
        ---------------------------------------------------
        """
        success = False
        
        if self.valid_key(key):
            #need to remove duplicates from the base and keyword
            keyword = key[0].lower()
            base = key[1].lower()
            
            no_dupes_keyword = ''
            no_dupes_base = ''
            
            for char in keyword:
                if char in base and char not in no_dupes_keyword:
                    no_dupes_keyword += char
            
            for char in base:
                if char not in no_dupes_base:
                    no_dupes_base += char    
            
            #make a new key that doesnt have the duplicate characters
            new_key = (no_dupes_keyword, no_dupes_base)
            
            self._key = new_key
            success = True
            
            
        return success
        
    def __str__(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       output (str): string representation
        Description:  Returns a string representation of Simple Substitution
                      Format:
                      Simple Substitution Cipher:
                      keyword = <keyword>
                      <base string>
                      <sub string>
        ---------------------------------------------------
        """
        return 'Simple Substitution Cipher:\nkey = ' + self.get_key()[0] + '\n' + self.get_table()[0] + '\n' + self.get_table()[1]
    
    def encrypt(self, plaintext):
        """
        ----------------------------------------------------
        Parameters:   plaintext (str)
        Return:       ciphertext (list)
        Description:  Encryption using Simple Substitution Cipher
                      Encrypts only characters defined in base
                      Preserves the case of characters
        Asserts:      plaintext is a string
        ----------------------------------------------------
        """
        assert type(plaintext) is str, 'invalid input'
        
        ciphertext = ''
        base, sub_string = self.get_table()
        
        #we need a bool to keep track of case for preservation
        uppercase = False
        
        for char in plaintext:
            
            if char.lower() not in base:
                ciphertext += char
            
            else:  
                #if the character is uppercase then we need to insert it as a capital  
                if char.isupper(): uppercase = True
                
                #get the position of the char in the sub_string                
                position = utilities.get_positions(base, char.lower())[0][1]
                
                #get the char from the base that matches that position index
                if not uppercase:
                    ciphertext += sub_string[position]
                else:
                    ciphertext += sub_string[position].upper()
                    uppercase = False
            
                
        return ciphertext

    def decrypt(self,ciphertext):
        """
        ----------------------------------------------------
        Parameters:   ciphertext (str)
        Return:       plaintext (list)
        Description:  decryption using Simple Substitution Cipher
                      Decrypts only characters defined in base
                      Preserves the case of characters
        Asserts:      ciphertext is a string
        ----------------------------------------------------
        """
        assert type(ciphertext) is str, 'invalid input'
        
        #same process as encrypt, just backwards
        plaintext = ''
        base, sub_string = self.get_table()
        
        #we need a bool to keep track of case for preservation
        uppercase = False
        
        for char in ciphertext:
            
            if char.lower() not in sub_string:
                plaintext += char
            
            else:  
                #if the character is uppercase then we need to insert it as a capital  
                if char.isupper(): uppercase = True
                
                #get the position of the char in the sub_string
                position = utilities.get_positions(sub_string, char.lower())[0][1]
                
                #get the char from the base that matches that position index
                if not uppercase:
                    plaintext += base[position]
                else:
                    plaintext += base[position].upper()
                    uppercase = False
            
                
        return plaintext





        
        
        
        
        
        