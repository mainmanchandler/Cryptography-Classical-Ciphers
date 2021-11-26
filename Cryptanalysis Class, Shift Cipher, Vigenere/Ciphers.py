"""
-------------------------------------
File: Ciphers.py
File description
Cryptanalysis class, shift cipher, Vigenere implementations
-------------------------------------
Author:  Chandler Mayberry
Version  2021-10-19
-------------------------------------
"""
import utilities

class Cryptanalysis:
    """
    ----------------------------------------------------
    Description: Class That contains cryptanalysis functions
                 Mainly for Vigenere and Shift Cipher 
                     but can be used for other ciphers
    ----------------------------------------------------
    """
    @staticmethod    
    def index_of_coincidence(text, base_type = None):
        """
        ----------------------------------------------------
        Static Method
        Parameters:   text(str)
                      base_type(str): default = None
        Return:       I (float): Index of Coincidence
        Description:  Computes and returns the index of coincidence 
                      Uses English alphabets by default, otherwise, given base_type
        Asserts:      text is a string
        ----------------------------------------------------
        """
        #Formula:  I = 1/(n(n-1)) for E[n(n-1)]
        assert type(text) is str, 'invalid input'
        
        #frequency is a list of floats of all char (aka the length of the text)
        frequency_list = utilities.get_freq(text, base_type)
        I = 0 
        n = 0
        
        #total number of characters in the ciphertext
        for each in frequency_list:
            n = n + each
        
        for k in frequency_list:
            I += k * (k - 1)
        
        #check for division by 0
        if n == 0:
            return 0
        
        I = I / (n*(n-1))
        
        return I       


    @staticmethod
    def IOC(text):
        """
        ----------------------------------------------------
        Same as Cryptanalysis.index_of_coincidence(text)
        ----------------------------------------------------
        """
        return Cryptanalysis.index_of_coincidence(text)
    
    
    @staticmethod
    def friedman(ciphertext):
        """
        ----------------------------------------------------
        Static method
        Parameters:   ciphertext(str)
        Return:       list of two key lengths [int,int]
        Description:  Uses Friedman's test to compute key length
                      returns best two candidates for key length
                        Best candidates are the floor and ceiling of the value
                          Starts with most probable key, for example: 
                          if friedman = 3.2 --> [3, 4]
                          if friedman = 4.8 --> [5,4]
                          if friedman = 6.5 --> [6, 5]
        Asserts:      ciphertext is a non-empty string
        ----------------------------------------------------
        """        
        #formula:   k = 0.0265n / ( (0.065 - I) + n(I - 0.0385))
        
        n = len(ciphertext) #text length
        I = Cryptanalysis.index_of_coincidence(ciphertext, None) #index of coincidence
        k = 0.0265*n / ( (0.065 - I) + n*(I - 0.0385)) #random keyword of length k 
        
        #find most and least probable
        most_probable = round(k)
        if most_probable < k:
            less_probable = most_probable + 1
        else:
            less_probable = most_probable - 1 
            
        #floor and ceiling, with [0] being the most probable size of keyword and [1] being second most probable length
        key_lengths = [most_probable, less_probable]
        
        return key_lengths


    @staticmethod
    def chi_squared(text,language='English'):
        """
        ----------------------------------------------------
        Parameters:   text (str)
                      language (str): default = 'English'
        Return:       result (float)
        Description:  Calculates the Chi-squared statistics 
                      for given text against given language
                      Only alpha characters are considered
        Asserts:      text is a string
        Errors:       if language is unsupported:
                        print error msg: 'Error(chi_squared): unsupported language'
                        return -1
        ----------------------------------------------------
        """
        assert type(text) is str, 'invalid input'
        
        #frequency of characters in a given language
        #if the frequency is empty then the language is unsupported
        language_frequency = utilities.get_language_freq(language)
        result = 0.0
        
        if language_frequency is []:
            print('Error(chi_squared): unsupported language')
            return -1
        
        
        #get the count of the char
        #check for division by 0
        frequency_list = utilities.get_freq(text, None)
        n = 0
        for each in frequency_list:
            n = n + each
        
        if n == 0:
            return -1
        
        
        #formula:   x^2 = E[ ((Ci - Ei)^2) / Ei]
        #Ci = count of i character in the text
        #Ei expected count of character (default stats table data, nothing calculated)
        #loop through each char in the alphabet 0-26
        for currLetter in range(26):
            Ei = language_frequency[currLetter] * n
            numerator = (frequency_list[currLetter] - Ei)**2
            result += numerator/Ei
            
        return result


    @staticmethod
    def cipher_shifting(ciphertext, args =[20,26]):
        """
        ----------------------------------------------------
        Parameters:   ciphertext (str)
                      args (lsit):
                          max_key_length (int): default = 20
                          factor (int): default = 26
        Return:       Best two key lengths [int,int]
        
        Description:  Uses Cipher shifting to compute key length
                      returns best two candidates for key length
                      cipher shift factor determines how many shifts should be made
                      Cleans the text from all non-alpha characters before shifting
                      Upper and lower case characters are considered different chars
                      
                      The returned two keys, are the ones that produced highest matches
                          if equal, start with smaller value
       
        Asserts:      ciphertext is a non-empty string
        ----------------------------------------------------
        """
        assert type(ciphertext) is str, 'invalid input'
        
        #remove all char that are not alpha
        ciphertext = utilities.clean_text(ciphertext, " \n")
        ciphertext = utilities.clean_text(ciphertext, "\t")
        ciphertext = utilities.clean_text(ciphertext, utilities.get_base('nonalpha'))
        assert ciphertext != '', 'invalid input'

        #grab arguments
        max_key_length, factor = args #factor determines how many shifts should be made
        shifted_cipher = ciphertext
        
        #comparision variables for the most matches, and their respective index
        mostMatches = 0
        mostMatches_Index = 0
        MostMatches2 = 0
        MostMatches2_Index = 0    
        
        #perform shifts to right
        for shiftNum in range(1, factor):     
                    
            #shift the cipher to the right on each iteration
            shifted_cipher = ' ' + shifted_cipher[:-1]
 
            """if shiftNum < 4:
                print(shifted_cipher)"""
            
            #compare the text to get the number of matches
            n_matches = utilities.compare_texts(ciphertext, shifted_cipher)
            
           
            #modulo with max_key_length if the shiftNum exceeds the max_key_length
            #number of shifts for keyword length <= max_key_length
            if shiftNum > max_key_length:
                adjShiftNum = shiftNum % max_key_length
            else:
                adjShiftNum = shiftNum
            
            if n_matches > mostMatches: #check to see if the number of matches was greater than previous shifts
                MostMatches2 = mostMatches
                MostMatches2_Index = mostMatches_Index
                mostMatches = n_matches
                mostMatches_Index = adjShiftNum
                
            elif n_matches > MostMatches2: #check to see if it was greater for only second most matches
                MostMatches2 = n_matches
                MostMatches2_Index = adjShiftNum
         

        
        key_lengths = [mostMatches_Index, MostMatches2_Index]
        
        return key_lengths


class Shift:
    """
    ----------------------------------------------------
    Cipher name: Shift Cipher
    Key:         (int,int,int): shifts,start_index,end_index
    Type:        Shift Substitution Cipher
    Description: Generalized version of Caesar cipher
                 Uses a subset of BASE for substitution table
                 Shift base by key and then substitutes
                 Case sensitive
                 Preserves the case whenever possible
                 Uses circular left shift
    ----------------------------------------------------
    """
    BASE = utilities.get_base('all') + ' '
    DEFAULT_KEY = (3,26,51)   #lower case Caesar cipher
    
    def __init__(self, key=DEFAULT_KEY):
        """
        ----------------------------------------------------
        Parameters:   _key (int,int,int): 
                        #shifts, start_index, end_indx 
                        (inclusive both ends of indices)
        Description:  Shift constructor
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
        Return:       key (str)
        Description:  Returns a copy of the Shift key
        ---------------------------------------------------
        """
        return self._key
       
    def set_key(self,key):
        """
        ----------------------------------------------------
        Parameters:   key (str): non-empty string
        Return:       success: True/False
        Description:  Sets Shift cipher key to given key
                      #shifts is set to smallest value
                      if invalid key --> set to default key
        ---------------------------------------------------
        """ 
        success = False
        
        if self.valid_key(key):
            
            #if the key is less than 0 we need to take the length of the new base and subtract to get # of shifts
            #key[2]+1 - key[1] is the length of the base (end+1 - start) == len(new base)
            if key[0] < 0:
                shifts = (key[2]+1 - key[1]) - abs(key[0])
                new_key = (shifts, key[1], key[2])
            else:           
                new_key = key

            self._key = new_key
            success = True
            
        else:
            self._key = self.DEFAULT_KEY
            
        return success

    def get_base(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       base (str)
        Description:  Returns a copy of the base characters
                      base is the subset of characters from BASE
                      starting at start_index and ending with end_index
                      (inclusive both ends)
        ---------------------------------------------------
        """
        #get the base
        BASE = self.BASE
        
        #get the starting and ending index
        start = self.get_key()[1]
        end = self.get_key()[2]+1
        
        base = BASE[start:end]
        
        return base
        
    def __str__(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       output (str)
        Description:  Constructs and returns a string representation of 
                      Shift object. Used for testing
                      output format:
                      Shift Cipher:
                      key = <key>
                      base = <base>
                      sub  = <sub>
        ---------------------------------------------------
        """
        #note: sub is what is being substituted after shift
        output = "Shift Cipher:\nkey = " + str(self.get_key()) + "\nbase = " + self.get_base()
        output += "\nsub  = " + utilities.shift_string(self.get_base(), self.get_key()[0], 'l')
        return output
    
    @staticmethod
    def valid_key(key):
        """
        ----------------------------------------------------
        Static Method
        Parameters:   key (?):
        Returns:      True/False
        Description:  Checks if given key is a valid Shift key
                      A valid key is a tuple consisting of three integers
                          shifts, start_index, end_index
                      The shifts can be any integer
                      The start and end index should be positive values
                      such that start is smaller than end and both are within BASE
        ---------------------------------------------------
        """
        valid = False
        
        if type(key) == tuple and len(key) ==3 and type(key[0]) is int and type(key[1]) is int and type(key[2]) is int:
            start = key[1]
            end = key[2]
            within_range = len(Shift.BASE)
            if start >= 0 and end > 0 and start < end and start < within_range and end <= within_range:
                valid = True
        
        
        return valid

    def encrypt(self, plaintext):
        """
        ----------------------------------------------------
        Parameters:   plaintext (str)
        Return:       ciphertext (str)
        Description:  Encryption using Shift Cipher
        Asserts:      plaintext is a string
        ---------------------------------------------------
        """
        assert type(plaintext) is str, 'invalid input'
        ciphertext = ''
        
        #we simply need to shift the shift the base text and then substitute the letter from the base
        sub = utilities.shift_string(self.get_base(), self.get_key()[0], 'l')
        base = self.get_base()
        
        for char in plaintext: 
            if char in base:
                position_of_char = utilities.get_positions(base, char)
                temp_char = sub[position_of_char[0][1]]
                ciphertext += temp_char
            else:
                ciphertext += char
                
        return ciphertext


    def decrypt(self, ciphertext):
        """
        ----------------------------------------------------
        Parameters:   ciphertext (str)
        Return:       plaintext (str)
        Description:  Decryption using Shift Cipher
        Asserts:      ciphertext is a string
        ---------------------------------------------------
        """
        assert type(ciphertext) is str, 'invalid input'
        plaintext = ''
        
        #we simply need to shift the shift the base text and then substitute the letter from the base
        sub = utilities.shift_string(self.get_base(), self.get_key()[0], 'l')
        base = self.get_base()
        
        for char in ciphertext: 
            if char in sub:
                position_of_char = utilities.get_positions(sub, char)
                temp_char = base[position_of_char[0][1]]
                plaintext += temp_char
            else:
                plaintext += char
                
        return plaintext
        

    @staticmethod
    def cryptanalyze(ciphertext,args=['',-1,0]):
        """
        ----------------------------------------------------
        Static method
        Parameters:   ciphertext (string)
                      args (list):
                            base: (str): default = ''
                            shifts: (int): default = -1
                            base_length (int): default = -1 
        Return:       key,plaintext
        Description:  Cryptanalysis of Shift Cipher
                      Returns plaintext and key (shift,start_indx,end_indx)
                      Uses the Chi-square method
                      Assumes user passes a valid args list
        ---------------------------------------------------
        """
                
        #get args
        base, shifts, base_length = args
        
        key = (0,0,0)
        plaintext = ''
        compare_chi = 1002955768

        
        # 1 - known base, known number of shifts
        if base != '' and shifts != -1 and base_length != -1:
            start = utilities.get_positions(Shift.BASE, base[0])[0][1]
            end = utilities.get_positions(Shift.BASE, base[-1])[0][1] 
            """print(Shift.BASE[start_pos:end_pos])"""
            
            #create key and object then decrypt
            key = (shifts, start, end) 
            shiftobj = Shift(key)
            plaintext = shiftobj.decrypt(ciphertext)
        
        
        # 2 - known base, unknown number of shifts 
        elif base != '' and shifts == -1:
            
            start = utilities.get_positions(Shift.BASE, base[0])[0][1]
            end = utilities.get_positions(Shift.BASE, base[-1])[0][1] 
            
            #stop shifting on the length of the key
            shift_key_found = 0
            runs = len(base)
            
            #we need to test for all possible shifts, ie. the length of the cipher
            for shifts in range(runs):
                
                key = (shifts, start, end) 
                shiftobj = Shift(key)
                plaintext = shiftobj.decrypt(ciphertext)
                chi_squared_result = Cryptanalysis.chi_squared(plaintext, language='English')
                
                #we need to see if the chi-squared is close enough to plain english (hard coded at 800, arbitrary # not the right thing to do..)
                if chi_squared_result <= compare_chi:
                    compare_chi = chi_squared_result
                    shift_key_found = shifts
                    
            """if shifts <= 10:
                print(chi_squared_result)"""
            
            #use the key that was the closest and output the plaintext
            key = (shift_key_found, start, end) 
            shiftobj = Shift(key)
            plaintext = shiftobj.decrypt(ciphertext)
        
        
        # 3 - unknown base, known shifts, known base length
        elif base == '' and shifts != -1 and base_length != -1:
            
            #we need to shift through all values in the base_length, can be any range within the default BASE
            for i in range(len(Shift.BASE)):
                
                start = i
                
                #do not go over the length of BASE (95)
                if (i + base_length < len(Shift.BASE)):
                        end = i + base_length + 1
                else:
                    break
                
                #we need to cycle through base_length n times in each cycle as start/end can be any range inside base_length
                run = 1
                for _ in range(base_length):
                    
                    end = i + run + 1
                    
                    """print(end-start)"""
                                                        
                    #create key and object then decrypt
                    temp_key = (shifts, start, end) 
                    shiftobj = Shift(temp_key)
                    plaintext = shiftobj.decrypt(ciphertext)
                    
                    chi_squared_result = Cryptanalysis.chi_squared(plaintext, language='English')
                    
                    """print('-------------------------------')
                    print(chi_squared_result)
                    print(compare_chi)
                    print(start)
                    print(end)"""
                    
                    
                    if chi_squared_result <= compare_chi:
                        #print('hi')
                        compare_chi = chi_squared_result
                        key = (shifts, start, end)
                
                    run += 1
                    
            #use the key that was the closest and output the plaintext
            shiftobj = Shift(key)
            plaintext = shiftobj.decrypt(ciphertext)
        
        # 4 - unknown base, unknown shifts, known base length
        elif base == '' and shifts == -1 and base_length != -1:
            

            #we need to shift through all values in the base_length, can be any range within the default BASE
            for i in range(len(Shift.BASE)):
                
                start = i
                
                #do not go over the length of BASE (95)
                if (i + base_length < len(Shift.BASE)):
                        end = i + base_length + 1
                else:
                    break
                
                #we need to cycle through base_length n times in each cycle as start/end can be any range inside base_length
                run = 1
                for _ in range(base_length):
                    
                    end = i + run + 1
                    
                    #we need to cycle through every possible shift with every possible start/end key
                    for shifts in range(base_length):

                        #create key and object then decrypt
                        temp_key = (shifts, start, end) 
                        shiftobj = Shift(temp_key)
                        plaintext = shiftobj.decrypt(ciphertext)
                        
                        chi_squared_result = Cryptanalysis.chi_squared(plaintext, language='English')
                        
                        """print('-------------------------------')
                        print(chi_squared_result)
                        print(compare_chi)
                        print(start)
                        print(end)
                        print(shifts)
                        print(base_length)"""
                        
                        if chi_squared_result <= compare_chi:
                            compare_chi = chi_squared_result
                            key = (shifts, start, end)
                    
                        
                    run += 1
                    
            #use the key that was the closest and output the plaintext
            shiftobj = Shift(key)
            plaintext = shiftobj.decrypt(ciphertext)
            
        
        return key, plaintext

class Vigenere:
    """
    ----------------------------------------------------
    Cipher name: Vigenere Cipher
    Key:         (str): a character or a keyword
    Type:        Polyalphabetic Substitution Cipher
    Description: if key is a single characters, uses autokey method
                    Otherwise, it uses a running key
                 In autokey: key = autokey + plaintext (except last char)
                 In running key: repeat the key
                 Substitutes only alpha characters (both upper and lower)
                 Preserves the case of characters
    ----------------------------------------------------
    """
    
    DEFAULT_KEY = 'k'
    
    def __init__(self,key=DEFAULT_KEY):
        """
        ----------------------------------------------------
        Parameters:   _key (str): default value: 'k'
        Description:  Vigenere constructor
                      sets _key
                      if invalid key, set to default key
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
        Return:       key (str)
        Description:  Returns a copy of the Vigenere key
        ---------------------------------------------------
        """
        return self._key
       
    def set_key(self,key):
        """
        ----------------------------------------------------
        Parameters:   key (str): non-empty string
        Return:       success: True/False
        Description:  Sets Vigenere cipher key to given key
                      All non-alpha characters are removed from the key
                      key is converted to lower case
                      if invalid key --> set to default key
        ---------------------------------------------------
        """ 
        success = False
        
        if self.valid_key(key):
            #remove all non-alpha characters and convert to lowercase
            key = key.lower()
            key = utilities.clean_text(key, utilities.get_base('nonalpha'))
            key = utilities.clean_text(key, ' \n\t')

            self._key = key
            
            success = True
        else:
            self._key = self.DEFAULT_KEY
            
        return success
    
    def __str__(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       output (str)
        Description:  Constructs and returns a string representation of 
                      Vigenere object. Used for testing
                      output format:
                      Vigenere Cipher:
                      key = <key>
        ---------------------------------------------------
        """
        output = 'Vigenere Cipher:\nkey = ' + self.get_key()
        return output
    
    @staticmethod
    def valid_key(key):
        """
        ----------------------------------------------------
        Static Method
        Parameters:   key (?):
        Returns:      True/False
        Description:  Checks if given key is a valid Vigenere key
                      A valid key is a string composing of at least one alpha char
        ---------------------------------------------------
        """
        valid = False
        
        if type(key) is str:
            
            # A valid key is a string composing of at least one alpha char
            has_alpha = False
            for char in key:
                if char.isalpha():
                    has_alpha = True
                    break
            
            if has_alpha:
                valid = True  
                 
        return valid


    @staticmethod
    def get_square():
        """
        ----------------------------------------------------
        static method
        Parameters:   -
        Return:       vigenere_square (list of string)
        Description:  Constructs and returns vigenere square
                      The square contains a list of strings
                      element 1 = "abcde...xyz"
                      element 2 = "bcde...xyza" (1 shift to left)
        ---------------------------------------------------
        """
        #get base, the alphabet shifted to left 1, 26times
        vigenere_square = []
        base = utilities.get_base('lower')

        for row in range(26):
            vigenere_square.append(utilities.shift_string(base, row, 'l'))
        
        return vigenere_square


    def encrypt(self,plaintext):
        """
        ----------------------------------------------------
        Parameters:   plaintext (str)
        Return:       ciphertext (str)
        Description:  Encryption using Vigenere Cipher
                      May use an auto character or a running key
        Asserts:      plaintext is a string
        ---------------------------------------------------
        """
        assert type(plaintext) == str, 'invalid plaintext'
        
        if len(self._key) == 1:
            return self._encrypt_auto(plaintext)
        else:
            return self._encrypt_run(plaintext)


    def _encrypt_auto(self,plaintext):
        """
        ----------------------------------------------------
        Parameters:   plaintext (str)
        Return:       ciphertext (str)
        Description:  Private helper function
                      Encryption using Vigenere Cipher Using an autokey
        ---------------------------------------------------
        """
        #when key length is 1:
        #The encryption and decryption apply only to alpha characters. The case of the letters 
        #should be preserved.
        #performing calculation with ascii, if you convert the square table to ascii numbers then its 
        #simple logic, no iteration needed
        ciphertext = ''
        alpha_length = 26
        toUpper = 32
        key = self.get_key()
        
        for char in plaintext:
            
            #if the char is alpha we need to encrypt it
            if char.isalpha():
                
                #check to see if the char is upper or lowercase and then convert it to ascii
                #perform: ascii + ascii mod 26. This is the ~logic~ used behind the vigenere square table
                
                if ord(char) >= 97:
                    plainchar = ord(char) - 97
                    keychar = ord(key) - 97
                    cipherchar = (plainchar + keychar) % alpha_length
                    cipherchar = cipherchar + 97
    
                    ciphertext += chr(cipherchar)
                
                else: #retain case of word
                    char = char.lower()
                    plainchar = ord(char) - 97
                    keychar = ord(key) - 97
                    cipherchar = (plainchar + keychar) % alpha_length
                    
                    #convert back to uppercase
                    cipherchar = cipherchar + 97
                    cipherchar -= toUpper
                    
                    ciphertext += chr(cipherchar)
                            
            else:
                #if the char is not alpha then we can just add it to the ciphertext
                ciphertext += char
        


        return ciphertext

    def _encrypt_run(self,plaintext):
        """
        ----------------------------------------------------
        Parameters:   plaintext (str)
        Return:       ciphertext (str)
        Description:  Private helper function
                      Encryption using Vigenere Cipher Using a running key
        ---------------------------------------------------
        """
        #when key length is >1:
        #The encryption and decryption apply only to alpha characters. The case of the letters 
        #should be preserved.
        #performing calculation with ascii, if you convert the square table to ascii numbers then its 
        #simple logic, no iteration needed
        ciphertext = ''
        alpha_length = 26
        toUpper = 32
        key = self.get_key()
        
        key_index = 0
        for char in plaintext:
            
            if char.isalpha():
                
                #ensure that our index will reset at end of repeating key
                if key_index >= len(key):
                    key_index = 0
                
                #check to see if the char is upper or lowercase and then convert it to ascii
                #perform: ascii + ascii mod 26. This is the ~logic~ used behind the vigenere square table
                if ord(char) >= 97:
                    plainchar = ord(char) - 97
                    keychar = ord(key[key_index]) - 97
                    cipherchar = (plainchar + keychar) % alpha_length
                    cipherchar = cipherchar + 97
    
                    ciphertext += chr(cipherchar)
                
                else: #retain case of word
                    char = char.lower()
                    plainchar = ord(char) - 97
                    keychar = ord(key[key_index]) - 97
                    cipherchar = (plainchar + keychar) % alpha_length
                    
                    #convert back to uppercase
                    cipherchar = cipherchar + 97
                    cipherchar -= toUpper
                    
                    ciphertext += chr(cipherchar)
                
                key_index += 1
            
            else:
                #if the char is not alpha then we can just add it to the ciphertext
                ciphertext += char

        return ciphertext
        

    def decrypt(self,ciphertext):
        """
        ----------------------------------------------------
        Parameters:   ciphertext (str)
        Return:       plaintext (str)
        Description:  Decryption using Vigenere Cipher
                      May use an auto character or a running key
        Asserts:      ciphertext is a string
        ---------------------------------------------------
        """
        assert type(ciphertext) == str, 'invalid input'
        
        if len(self._key) == 1:
            return self._decryption_auto(ciphertext)
        else:
            return self._decryption_run(ciphertext)

    def _decryption_auto(self,ciphertext):
        """
        ----------------------------------------------------
        Parameters:   ciphertext (str)
        Return:       plaintext (str)
        Description:  Private Helper method
                      Decryption using Vigenere Cipher Using autokey
        ---------------------------------------------------
        """
        #when key length is >1:
        #The encryption and decryption apply only to alpha characters. The case of the letters 
        #should be preserved.
        #performing calculation with ascii, if you convert the square table to ascii numbers then its 
        #simple logic, no iteration needed
        plaintext = ''
        
        alpha_length = 26
        toUpper = 32
        key = self.get_key()
        
        for char in ciphertext:
            
            if char.isalpha():
                
                #check to see if the char is upper or lowercase and then convert it to ascii
                #perform: (ascii - ascii) and +26 if < 0. 
                #This is the ~logic~ used behind the vigenere square table
                if ord(char) >= 97:
                    cipherchar = ord(char) - 97
                    keychar = ord(key) - 97
                    
                    plainchar = cipherchar - keychar
                    if plainchar < 0:
                        plainchar = plainchar + alpha_length
                    plainchar = plainchar + 97
                    
                    plaintext += chr(plainchar)
                
                else: #retain case of word
                    char = char.lower()
                    
                    cipherchar = ord(char) - 97
                    keychar = ord(key) - 97                    
                
                    plainchar = cipherchar - keychar
                    if plainchar < 0:
                        plainchar = plainchar + alpha_length
                    plainchar = plainchar + 97
                    
                    #convert back to uppercase
                    plainchar -= toUpper
                    plaintext += chr(plainchar)
                    
                                
            else:
                #if the char is not alpha then we can just add it to the plaintext
                plaintext += char
            
        return plaintext

    def _decryption_run(self,ciphertext):
        """
        ----------------------------------------------------
        Parameters:   ciphertext (str)
        Return:       plaintext (str)
        Description:  Private Helper method
                      Decryption using Vigenere Cipher Using running key
        ---------------------------------------------------
        """
        #when key length is >1:
        #The encryption and decryption apply only to alpha characters. The case of the letters 
        #should be preserved.
        #performing calculation with ascii, if you convert the square table to ascii numbers then its 
        #simple logic, no iteration needed
        plaintext = ''
        
        alpha_length = 26
        toUpper = 32
        key = self.get_key()
        
        key_index = 0
        for char in ciphertext:
            
            if char.isalpha():
                
                #ensure that our index will reset at end of repeating key
                if key_index >= len(key):
                    key_index = 0
                
                #check to see if the char is upper or lowercase and then convert it to ascii
                #perform: (ascii - ascii) and +26 if < 0. 
                #This is the ~logic~ used behind the vigenere square table
                if ord(char) >= 97:
                    cipherchar = ord(char) - 97
                    keychar = ord(key[key_index]) - 97
                    
                    plainchar = cipherchar - keychar
                    if plainchar < 0:
                        plainchar = plainchar + alpha_length
                    plainchar = plainchar + 97
                    
                    plaintext += chr(plainchar)
                
                else: #retain case of word
                    char = char.lower()
                    
                    cipherchar = ord(char) - 97
                    keychar = ord(key[key_index]) - 97                    
                
                    plainchar = cipherchar - keychar
                    if plainchar < 0:
                        plainchar = plainchar + alpha_length
                    plainchar = plainchar + 97
                    
                    #convert back to uppercase
                    plainchar -= toUpper
                    plaintext += chr(plainchar)
                    
                    
                key_index += 1
            
            else:
                #if the char is not alpha then we can just add it to the plaintext
                plaintext += char
            
        return plaintext
    
    @staticmethod
    def cryptanalyze_key_length(ciphertext):
        """
        ----------------------------------------------------
        Static Method
        Parameters:   ciphertext (str)
        Return:       key_lenghts (list)
        Description:  Finds key length for Vigenere Cipher
                      Combines results of Friedman and Cipher Shifting
                      Produces a list of key lengths from the above two functions
                      Start with Friedman and removes duplicates
        ---------------------------------------------------
        """
        key_lengths = []
        
        #start with friedman and remove duplicates
        friedman = Cryptanalysis.friedman(ciphertext)
        cipher_shifting = Cryptanalysis.cipher_shifting(ciphertext)
        
        #friedman[priority #1, priority #2]
        #cipher_shift[priority #1, priority #2]
        
        """print("-----------------------------------")
        print(friedman)
        print(cipher_shifting)"""
        
        #if there is a matching probable key_length between both algorithms it takes priority
        #at the front of the list
        for length in friedman:
            if length in cipher_shifting:
                key_lengths.append(length)
        
        #insert the rest of the key_length elements from friedman and cipher_shifting
        for length in friedman:
            if length not in key_lengths:
                key_lengths.append(length)
        
        for length in cipher_shifting:
            if length not in key_lengths:
                key_lengths.append(length)
        
        return key_lengths

    @staticmethod
    def cryptanalyze(ciphertext):
        """
        ----------------------------------------------------
        Static method
        Parameters:   ciphertext (string)
        Return:       key,plaintext
        Description:  Cryptanalysis of Shift Cipher
                      Returns plaintext and key (shift,start_indx,end_indx)
                      Uses the key lengths produced by Vigenere.cryptanalyze_key_length
                      Finds out the key, then apply chi_squared
                      The key with the lowest chi_squared value is returned
        Asserts:      ciphertext is a non-empty string
        ---------------------------------------------------
        """
        assert type(ciphertext) is str, 'invalid input'
        assert len(ciphertext) != 0, 'invalid input'
        
        #clean ciphertext
        cleaned_ciphertext = utilities.clean_text(ciphertext, utilities.get_base('nonalpha') + " \t\n")
        
        
        
        #get the potential keyword lengths
        key_lengths = Vigenere.cryptanalyze_key_length(ciphertext)
        key = ''
        plaintext = ''
        
        minimumValue = None
        
        #go through each possible key_length
        for key_length in key_lengths:
            
            #break text into blocks and then baskets of text to find key
            blocks = utilities.text_to_blocks(cleaned_ciphertext, key_length, True)
            baskets = utilities.blocks_to_baskets(blocks)
            
            
            #find a potential key value and potential letter from Shift cipher cryptanalyze
            #shift.cryptanalze: we want to get the shift value. The shift value when turned into ascii represents a 
            #letter in the shift table
            potential_key_word = ''
            for basket in baskets:
                potential_key_letter = Shift.cryptanalyze(basket, [utilities.get_base("lower"), -1, key_length])[0][0]
                #print(potential_key)
                potential_key_word += chr(potential_key_letter + 97)
                #print(potential_key_letter)
            
            
            #make possible plaintext and check to see if its close to english language
            vigenereObject = Vigenere(potential_key_word)
            possible_plaintext = vigenereObject.decrypt(ciphertext)
        
            chi_val = Cryptanalysis.chi_squared(possible_plaintext, )
            
            if minimumValue == None or chi_val < minimumValue:
                minimumValue = chi_val
                key = potential_key_word
                plaintext = possible_plaintext
        
        
        return key, plaintext
        
        
        
        
        
        
        
        
            
            
            
    
    
    
    