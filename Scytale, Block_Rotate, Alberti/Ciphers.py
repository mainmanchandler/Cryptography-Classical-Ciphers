"""
-------------------------------------
File: Ciphers.py
File description
Scytale, Block Rotate, and Alberti Implementations
-------------------------------------
Author:  Chandler Mayberry
Version  2021-09-18
-------------------------------------
"""
from random import random
import utilities

class Scytale:
    """
    ----------------------------------------------------
    Cipher name: Spartan Scytale Cipher (500 B.C.)
    Key:         (int): number of rows (diameter of rod)
    Type:        Transposition Cipher
    Description: Assume infinite length rod, i.e., unlimited #columns
                 Construct a table that can fit the plaintext
                 Then read text vertically
                 #rows is equal to the key, final row might be empty
                 User may or may not use padding
    ----------------------------------------------------
    """
    
    DEFAULT_PAD = 'Q'
    DEFAULT_KEY = 4
    
    
    def __init__(self, key = DEFAULT_KEY, pad = DEFAULT_PAD):
        """
        ----------------------------------------------------
        Parameters:   _key (int): default value: 4
                      _pad (str): padding character, default = 'Q'
        Description:  Scytale constructor
                      sets _key, and _pad
                      if _pad is set to empty string --> no padding
        ---------------------------------------------------
        """
        #set the key and pad
        self._key = self.DEFAULT_KEY
        if key != self.DEFAULT_KEY:
            self.set_key(key)
        
        self._pad = self.DEFAULT_PAD
        if pad != self.DEFAULT_PAD:
            self.set_pad(pad)
        
        
    def get_key(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       key (int)
        Description:  Returns a copy of the scytale key
        ---------------------------------------------------
        """
        return self._key
       
       
    def set_key(self,key):
        """
        ----------------------------------------------------
        Parameters:   key (int): #columns
        Return:       success: True/False
        Description:  Sets Scytale key to given key
                      if invalid key --> set to default key
        ---------------------------------------------------
        """ 
        if Scytale.valid_key(key):
            self._key = key
            return True
        
        self._key = self.DEFAULT_KEY 
        return False
    
    
    def __str__(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       output (str)
        Description:  Constructs and returns a string representation of 
                      Scytale object. Used for testing
                      output format:
                      Scytale Cipher:
                      key = <key>, pad = <pad> OR
                      key = <key>, no padding
        ---------------------------------------------------
        """
        string_rep = 'Scytale Cipher:\n'
        if self._pad == '':
            string_rep += "key = " + str(self._key) + ", no padding"
        else:
            string_rep += "key = " + str(self._key) + ", pad = " + self._pad
        
        
        return string_rep
        
        
    @staticmethod
    def valid_key(key):
        """
        ----------------------------------------------------
        Static Method
        Parameters:   key (?):
        Returns:      True/False
        Description:  Checks if given key is a valid Scytale key
                      A valid key is an integer >= 1
        ---------------------------------------------------
        """
        if type(key) == int and key >= 1:
            return True
        else:
            return False
    
    
    def set_pad(self,pad):
        """
        ----------------------------------------------------
        Parameters:   pad (str): a padding character
        Return:       success: True/False
        Description:  Sets scytale pad to given character
                      a pad should be a single character or an empty string
                      if invalid pad, set to default value
                      empty string means no padding
        ---------------------------------------------------
        """
        #set empty string
        if pad == '':
            self._pad = pad
            return True
        
        #set single char
        elif type(pad) is str and len(pad)==1:
            self._pad = pad
            return True
        
        else:
            self._pad = self.DEFAULT_PAD
            return False
        
        

    def get_pad(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       pad (str): current padding character
        Description:  Returns a copy of current padding character
        ---------------------------------------------------
        """
        return self._pad
    

    def encrypt(self, plaintext):
        """
        ----------------------------------------------------
        Parameters:   plaintext (str)
        Return:       ciphertext (str)
        Description:  Encryption using Scytale Cipher
        Asserts:      plaintext is a string
        ---------------------------------------------------
        """
        assert type(plaintext) == str, 'invalid input'
        ciphertext = ''
        
        #key = number of rows
        nrows = self.get_key()
        
        
        #length of the plaintext determines how many columns
        length = len(plaintext)
        
        ncols = int(length/nrows)
        
        if length%nrows != 0:
            ncols+=1;
        
        
        # ncols and nrows determined, now make and fill the matrix
        cipher_matrix = utilities.new_matrix(nrows, ncols, self.get_pad())
        
        
        #fill matrix
        row = 0
        col = 0
        for char in plaintext:
            
            cipher_matrix[row][col] = char
            
            if col != ncols-1:
                col += 1
            else:
                col = 0
                row += 1
                
        #utilities.print_matrix(cipher_matrix)
        
        
        #encrypt, read vertically, col by col
        for col in range(ncols):
            for row in range(nrows):
                ciphertext += cipher_matrix[row][col]
        
        return ciphertext


    def decrypt(self, ciphertext):
        """
        ----------------------------------------------------
        Parameters:   ciphertext (str)
        Return:       plaintext (str)
        Description:  Decryption using Scytale Cipher
                      Removes padding if it exist
        Asserts:      ciphertext is a string
        ---------------------------------------------------
        """
        assert type(ciphertext) == str, 'invalid input'
        plaintext = ''
        
        #key = number of rows
        nrows = self.get_key()
        
        #length of the ciphertext determines how many columns
        length = len(ciphertext)
        ncols = int(length/nrows)
        
        if length%nrows != 0:
            ncols+=1;
        
        # ncols and nrows determined, now make and fill the matrix
        cipher_matrix = utilities.new_matrix(nrows, ncols, self.get_pad())

        #add padding to ciphertext, no padding pad_num
        pad_num = ncols*nrows - len(ciphertext)
        pad_time = ncols - pad_num #when to pad in the matrix

        #fill matrix
        row = 0
        col = 0
        
        i = 0
        while i < len(ciphertext):
            
            if col >= pad_time and row == nrows-1: #insert a pad
                cipher_matrix[row][col] = self.get_pad()

            else:
                cipher_matrix[row][col] = ciphertext[i]
                i+=1
            
            if row == nrows-1:
                row = 0
                col += 1
            else:
                row += 1
                
        
        #decrypt, read horizontally, row by row
        #utilities.print_matrix(cipher_matrix)
        """for i in range(len(cipher_matrix)):
            for char in cipher_matrix[i]:
               
                plaintext += char"""
        
        for r in range(nrows):
            for c in range(ncols):
                plaintext += cipher_matrix[r][c]          
           
        return plaintext.rstrip(self.get_pad())


    @staticmethod
    def cryptanalyze(ciphertext, args = [100, None, 0.9]):
        """
        ----------------------------------------------------
        Static method
        Parameters:   ciphertext (string)
                      args (list):
                        max_key (int): default 100
                        dictionary_file (str): default = None
                        threshold (float): default = 0.9
        Return:       key,plaintext
        Description:  Cryptanalysis of Scytale Cipher
                      Apply brute force from key 1 up to max_key (inclusive)
                      Assumes user passes a valid args list
        ---------------------------------------------------
        """
        
        #grab args
        max_key, dictionary_file, threshold = args
        dict_list = utilities.load_dictionary(dictionary_file)
        
        #init
        plaintext = ''
        keyfound = False
        i = 0
        
        #make new objects and test them with every key from 1 to max_key
        #if it passes is_plaintext with input threshold then it is successful
        while i < max_key and keyfound==False: 
            i += 1
            brute_force_attempt = Scytale(i, None) #creating a new object to analyze
            plaintext = brute_force_attempt.decrypt(ciphertext)
            keyfound = utilities.is_plaintext(plaintext, dict_list, threshold)
            #print(i)
                
        key = i
        
        #check for failure
        if i >= max_key:
            print('Scytale.cryptanalysis: cryptanalysis failed')
            key = ''
            plaintext = ''
            
        return key, plaintext





class Block_Rotate:
    """
    ----------------------------------------------------
    Cipher name: Block Rotate Cipher
    Key:         (B,R): block size, number of rotations
    Type:        Transposition Cipher
    Description: Breaks plaintext into blocks of size B
                 Rotates each block by R
                 Uses padding for the final block
    ----------------------------------------------------
    """
    
    DEFAULT_PAD = 'q'
    DEFAULT_KEY = (1,0)
    
    def __init__(self, key=DEFAULT_KEY, pad=DEFAULT_PAD):
        """
        ----------------------------------------------------
        Parameters:   _key (int,int): default value: (1,0)
                      _pad (str): a character, default = q
        Description:  Block Rotate constructor
                      sets _key and _pad
        ---------------------------------------------------
        """
        #set the key and the pad to the object
        self._key = self.DEFAULT_KEY
        if key != self.DEFAULT_KEY:
            self.set_key(key)
        
        self._pad = self.DEFAULT_PAD
        if pad != self.DEFAULT_PAD:
            self.set_pad(pad)
            
              
    def get_key(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       key (int,int)
        Description:  Returns a copy of the Block Rotate key
        ---------------------------------------------------
        """
        return self._key
       
       
    def set_key(self, key):
        """
        ----------------------------------------------------
        Parameters:   key (b,r): tuple(int,int)
        Return:       success: True/False
        Description:  Sets block rotate cipher key to given key
                      if invalid key --> set to default key
        ---------------------------------------------------
        """ 
        
        if Block_Rotate.valid_key(key):
            #reduce the number of rotations with modulo
            b = key[0]
            r = key[1]
            
            r = r%b
            refactored = (b,r)
        
            self._key = refactored
            return True
        
        self._key = self.DEFAULT_KEY 
        return False
        
    
    def __str__(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       output (str)
        Description:  Constructs and returns a string representation of 
                      Blcok Rotate object. Used for testing
                      output format:
                      Block Rotate Cipher:
                      key = <key>, pad = <pad>
        ---------------------------------------------------
        """
        string_rep = 'Block Rotate Cipher:\n'
        if self._pad == '':
            string_rep += "key = " + str(self._key) + ", no padding"
        else:
            string_rep += "key = " + str(self._key) + ", pad = " + self._pad
        
        return string_rep
        
            
    @staticmethod
    def valid_key(key):
        """
        ----------------------------------------------------
        Static Method
        Parameters:   key (?):
        Returns:      True/False
        Description:  Checks if given key is a valid block rotate key
        ---------------------------------------------------
        """
        #check if both tuples are of int type
        
        if type(key) is tuple and (type(key[0]) is int and key[0] > 0) and type(key[1]) is int and len(key) == 2:
            return True
        else:
            return False
        
    
    def set_pad(self,pad):
        """
        ----------------------------------------------------
        Parameters:   pad (str): a padding character
        Return:       success: True/False
        Description:  Sets block rotate pad to given character
                      a pad should be a single character
                      if invalid pad, set to default value
        ---------------------------------------------------
        """ 
        
        if pad == '':
            self._pad = pad
            return True
        
        elif type(pad) is str and len(pad)==1:
            self._pad = pad
            return True
        
        else:
            self._pad = self.DEFAULT_PAD
            return False

    
    def get_pad(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       pad (str): current padding character
        Description:  Returns a copy of current padding character
        ---------------------------------------------------
        """ 
        return self._pad
        
        
    def encrypt(self, plaintext):
        """
        ----------------------------------------------------
        Parameters:   plaintext (str)
        Return:       ciphertext (str)
        Description:  Encryption using Block Rotation Cipher
        Asserts:      plaintext is a string
        ---------------------------------------------------
        """
        assert type(plaintext) is str, 'invalid input'
        
        nblocks = self._key[0]
        nrotations = self._key[1]
        
        #convert the string to blocks
        blocks = utilities.text_to_blocks(plaintext, nblocks, True, self.get_pad())
        
        """for i in blocks:
            print(i, end = " ")
            
        print()"""
            
        #we need to remove the newline character
        newline_positions = utilities.get_positions(plaintext, "\n")    
        plaintext = utilities.clean_text(plaintext, "\n")
        
        #could use shift string here:
        #perform rotations
        #positive, then left rotation, otherwise right
        for i in range(len(blocks)):
            
            if nrotations > 0: 
                block = blocks[i] #inner list to rotate
            
                #get the new right side string of left rotation
                new_right = block[0 : nrotations] 
                
                #delete the old left side for left rotation
                new_left = block[nrotations :] 
                
                block = new_left + new_right
                blocks[i] = block
            
            else:
                block = blocks[i] #inner list to rotate
                
                #delete the old right side for right rotation
                new_right = block[0 : len(block) - nrotations] 
                
                #get the new left side string of right rotation
                new_left = block[len(block) - nrotations : ]
                
                block = new_left + new_right
                blocks[i] = block
                    
        """for i in blocks:
            print(i, end = " ")
            
        print()"""
        
        #convert the matrix back to a string
        ciphertext = utilities.matrix_to_string(blocks)
        
        #add the newline characters back in
        ciphertext = utilities.insert_positions(ciphertext, newline_positions)
        
        
        return ciphertext


    def decrypt(self,ciphertext):
        """
        ----------------------------------------------------
        Parameters:   ciphertext (str)
        Return:       plaintext (str)
        Description:  Decryption using Block Rotation Cipher
                      Removes padding if it exist
        Asserts:      ciphertext is a string
        ---------------------------------------------------
        """    
        assert type(ciphertext) is str, 'invalid input'
        
        #remove the newline characters
        newline_positions = utilities.get_positions(ciphertext, "\n")    
        ciphertext = utilities.clean_text(ciphertext, "\n")
        
        current_key = self.get_key()
        
        b = current_key[0]
        r = current_key[1]
        r = -r
        inverse_rotation_key = (b,r)
        
        self.set_key(inverse_rotation_key)
        plaintext = Block_Rotate.encrypt(self, ciphertext)
        self.set_key(current_key)
        
        #add the newline characters back in
        plaintext = utilities.insert_positions(plaintext, newline_positions)        
        
        return plaintext.rstrip(self.get_pad())


    @staticmethod
    def cryptanalyze(ciphertext,args=[0,0,0,None,0.8]):
        """
        ----------------------------------------------------
        Static method
        Parameters:   ciphertext (string)
                      args (list):
                            b0: minimum block size (int): default = 0
                            bn: maximum block size (int): default = 0
                            r: rotations (int): default = 0
                            dictionary_file (str): default = None
                            threshold (float): default = 0.8
        Return:       key,plaintext
        Description:  Cryptanalysis of Block Rotate Cipher
                      Returns plaintext and key (r,b)
                      Attempts block sizes from b0 to bn (inclusive)
                      If bn is invalid or unspecified use 20
                      Minimum valid value for b0 is 2
                      Assumes user passes a valid args list
        ---------------------------------------------------
        """
        #grab args
        b0, bn, r, dictionary_file, threshold = args
        dict_list = utilities.load_dictionary(dictionary_file)

        #set defaults
        if b0 == 0:
            b0 = 2 #minimum size for b0
        
        if bn == 0 or bn < 2:
            bn = 20 #default size
            
        plaintext = ''
        
        #find plaintext
        keyfound = False
        temp = 0
        #print(b0)
        for i in range(b0, bn+1):
            
            temp = i
            #print(temp)
            if r == 0:
                for rotations in range(i):
                    brute_force_attempt = Block_Rotate((i,rotations), None)
                    plaintext = brute_force_attempt.decrypt(ciphertext)
                    keyfound = utilities.is_plaintext(plaintext, dict_list, threshold)
                    if keyfound:
                        r = rotations
                        break
                        
            else:
                brute_force_attempt = Block_Rotate((i,r),None)
                plaintext = brute_force_attempt.decrypt(ciphertext)
                keyfound = utilities.is_plaintext(plaintext, dict_list, threshold)
            
            if keyfound:
                break
        
        key = (temp, r)
        
        #print(keyfound)
        #check for failure
        if temp > bn or keyfound is False:
            print('Block_Rotate.cryptanalyze: cryptanalysis failed')
            key = ''
            plaintext = ''
        
        return key, plaintext




class Alberti:
    """
    ----------------------------------------------------
    Cipher name: Alberti Cipher (1472)
    Key:         (pointer,in_wheel)
    Type:        Substitution Cipher
    Description:Default mode:
                    Outer wheel has a..z0..9
                    Given inner wheel has some random arrangement of a..z0..9
                    Perform simple substitution
                Simple mode:
                    Outer wheel has a..z0..9
                    Inner wheel uses default value
                    Perform simple substitution
                Periodic mode:
                    Outer wheel has a..z0..9
                    Given inner wheel has some random arrangement of a..z0..9
                    Perform simple substitution while changing inner wheel once
                        clockwise every PERIOD number of characters
                In all modes:
                    Outer wheel at a is aligned with (pointer) at inner wheel
                    outer and inner wheel has same characters
                    In encryption/decryption Ignore characters not 
                        defined in the base (wheels)
                     encryption/decryption is case insensitive -->
                        output is always lower case
    ----------------------------------------------------
    """
    #constants
    OUT_WHEEL = 'abcdefghijklmnopqrstuvwxyz0123456789'
    DEFAULT_KEY = ('k','k0v9p1j8m2r7d3l5g4a6zteunwbosfchyqix')
    PERIOD = 8
    MODES = ['default','simple','periodic']
    
    def __init__(self,key=DEFAULT_KEY, mode='default'):
        """
        ----------------------------------------------------
        Parameters:   _key (str,str): pointer,base
                      _mode (str): default = 'default'
        Description:  Alberti Cipher constructor
                      sets _key and _mode
        ---------------------------------------------------
        """
        #we have to set the mode first, to default a key in-wheel if not given
        self._mode = self.MODES[0]
        if mode != self.MODES[0] and mode in self.MODES:
            self.set_mode(mode)
            
        
        self._key = self.DEFAULT_KEY
        if key is not None and key != self.DEFAULT_KEY:
            self.set_key(key)
        
        
    
    def get_key(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       key (str,str)
        Description:  Returns a copy of the Alberti key
        ---------------------------------------------------
        """
        return self._key
       
       
    def set_key(self,key):
        """
        ----------------------------------------------------
        Parameters:   key (str,str): tuple(str,str)
        Return:       success: True/False
        Description:  Sets Alberti cipher key to given key
                      if invalid key --> set to default key
                      does not update in_wheel in simple mode
        ---------------------------------------------------
        """ 
        if Alberti.valid_key(key):  
            
            #if the mode is in simple, then the in-wheel must stay default
            if self.get_mode() == 'simple':
                simple_case_key = (key[0], self.DEFAULT_KEY[1])
                self._key = simple_case_key
            else:
                self._key = key
            
            return True
        
        self._key = self.DEFAULT_KEY 
        return False
        
        
    def __str__(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       output (str)
        Description:  Constructs and returns a string representation of 
                      Alberti object. Used for testing
                      output format:
                      Alberti Cipher:
                      key = <key>, mode = <mode>
                      <out_wheel>
                      <in_wheel>
        ---------------------------------------------------
        """
        string_rep = 'Alberti Cipher:\n'
        string_rep += "key = " + str(self._key) + ", mode = " + str(self._mode) + "\n"
        
        out_wheel, in_wheel = self.get_wheels()
        string_rep += out_wheel + "\n" + in_wheel 
        
        return string_rep
    
    @staticmethod
    def valid_key(key):
        """
        ----------------------------------------------------
        Static Method
        Parameters:   key (?):
        Returns:      True/False
        Description:  Checks if given key is a valid alberti key
        ---------------------------------------------------
        """
        #check if both tuples are of str type
        checker = Alberti(None, None) # need to instantiate an object as this is a static method, avoid hardcoding
        
        #print(checker.OUT_WHEEL)
        #make sure key is a tuple, both tuples are str, key[0] is one char, key[1] is same length as outer, 
        #key[1] is alphanumeric, key[0] in key[1]
        if ((type(key) is tuple) and (type(key[0]) is str and len(key[0]) == 1) and (type(key[1]) is str) and 
        ((len(key[1]) == len(checker.OUT_WHEEL))) and (key[1].isalnum()) and key[0] in key[1]):
            return True
        else:
            return False
        
               
    def set_mode(self, mode):
        """
        ----------------------------------------------------
        Parameters:   mode (str): Alberti cipher mode
        Return:       success: True/False
        Description:  Sets Alberti cipher to given mode
                      valid only if defined in MODES
                      Otherwise set to 'default'
                      when setting to simple mode, set in_wheel to default value
        ---------------------------------------------------
        """ 
        self._mode = self.MODES[0]
        
        if mode != self.MODES[0] and mode in self.MODES:
            
            self._mode = mode
            
            #if simple, set in_wheel to default value
            if mode == 'simple':
                key = self.get_key()
                pointer = key[0]
                in_wheel = self.DEFAULT_KEY[1]
                new_key = (pointer, in_wheel)
                self.set_key(new_key)
                
            return True
        
        elif mode == self.MODES[0]:
            #self.set_key(self.DEFAULT_KEY)
            return True
        
        return False
    
    def get_mode(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       mode (str): current cipher mode
        Description:  Returns a copy of current mode
        ---------------------------------------------------
        """ 
        return self._mode
    
    
    def get_wheels(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       out_wheel (str)
                      in_wheel (str)
        Description:  returns out and in wheels aligned at pointer
        ---------------------------------------------------
        """
        
        out_wheel = self.OUT_WHEEL
        
        key = self.get_key()
        in_wheel = key[1]
            
        #pointer_position = ['pointer', i]
        pointer_position = utilities.get_positions(key[1], key[0])
        aligned_in_wheel = utilities.shift_string(in_wheel, pointer_position[0][1], 'l')
        
        
        return out_wheel, aligned_in_wheel

    @staticmethod
    def random_wheel():
        """
        ----------------------------------------------------
        Static Method
        Parameters:   -
        Returns:      random_wheel (str)
        Description:  Generates a random arrangement of outer wheel
        ---------------------------------------------------
        """
        #using the random import, randomize the outer wheel string
        random_out_wheel = Alberti().OUT_WHEEL
        random_out_wheel = ''.join(random.sample(random_out_wheel, len(random_out_wheel)))
    
        return random_out_wheel

    def encrypt(self,plaintext):
        """
        ----------------------------------------------------
        Parameters:   plaintext (str)
        Return:       ciphertext (str)
        Description:  Encryption using Alberti Cipher
        Asserts:      plaintext is a string
        ---------------------------------------------------
        """
        assert type(plaintext) is str, "invalid input"
        
        ciphertext = ''
        out_wheel, in_wheel = self.get_wheels()
        
        for i in range(len(plaintext)):
            
            #for regular char in out_wheel
            if plaintext[i].lower() in out_wheel:
                character_position = utilities.get_positions(out_wheel, plaintext[i].lower())
                index = character_position[0][1]
                ciphertext += in_wheel[index]  
                          
            #for special characters that aren't in the outer wheel
            else:
                ciphertext += plaintext[i]

            #shifting the outer wheel if the mode is periodic
            period = self.PERIOD
            if self.get_mode() == 'periodic' and i > 0 and (i+1) % period == 0:
                in_wheel = utilities.shift_string(in_wheel, 1, 'r')
                
                
        return ciphertext
        

    
    def decrypt(self,ciphertext):
        """
        ----------------------------------------------------
        Parameters:   ciphertext (str)
        Return:       plaintext (str)
        Description:  Decryption using Alberti Cipher
        Asserts:      ciphertext is a string
        ---------------------------------------------------
        """
        assert type(ciphertext) is str, "invalid input"

        plaintext = ''        
        out_wheel, in_wheel = self.get_wheels()
        
        for i in range(len(ciphertext)):
            
            #for regular char in out_wheel
            if ciphertext[i].lower() in in_wheel:
                character_position = utilities.get_positions(in_wheel, ciphertext[i].lower()) 
                index = character_position[0][1]
                plaintext += out_wheel[index]
                            
            #for special characters that aren't in the outer wheel
            else:
                plaintext += ciphertext[i]
                
            #shifting the inner wheel if the mode is periodic
            period = self.PERIOD
            if self.get_mode() == 'periodic' and i > 0 and (i+1) % period == 0:
                in_wheel = utilities.shift_string(in_wheel, 1, 'r')
                
        return plaintext
    
    
    @staticmethod
    def cryptanalyze(ciphertext, args=['','','',None,0.8]):
        """
        ----------------------------------------------------
        Static method
        Parameters:   ciphertext (string)
                      args (list):
                            pointer: (str): default = ''
                            in_wheel: (str): default = ''
                            mode: (str): default = ''
                            dictionary_file (str): default = None
                            threshold (float): default = 0.8
        Return:       key,plaintext
        Description:  Cryptanalysis of Alberti Cipher
                      Returns plaintext and key (pionter,in_wheel)
                      Assumes user passes a valid args list
        ---------------------------------------------------
        """  
        #extract arguments
        pointer,in_wheel, mode, dictionary_file, threshold = args        
        dict_list = utilities.load_dictionary(dictionary_file)
        
        #init
        keyfound = False
        key = (pointer, in_wheel)
        brute_force_attempt = Alberti()
        
        #can not set key if the in_wheel is not given as it would be invalid, therefore default
        if in_wheel == '':
            in_wheel = brute_force_attempt.DEFAULT_KEY[1]
        
        #if mode is not given we need to test all modes with all char
        if mode == '':
            
            i = 0
            while keyfound is False and i != len(brute_force_attempt.MODES):
                
                #set the mode to the ith mode
                mode = brute_force_attempt.MODES[i]
                brute_force_attempt.set_mode(mode)
                
                #test each character in the ciphertext
                
                curr_char = 0
                while keyfound is False and curr_char < len(ciphertext):
                    pointer = ciphertext[curr_char];
                    key = (pointer,in_wheel);
                    brute_force_attempt.set_key(key);
                    
                    plaintext = brute_force_attempt.decrypt(ciphertext)
                    keyfound = utilities.is_plaintext(plaintext, dict_list, threshold)
                    curr_char += 1
                
                i += 1            
            
        else:
            
            #set the mode to the ith mode
            brute_force_attempt.set_mode(mode)
            
            #test each character in the ciphertext
            curr_char = 0
            while keyfound is False and curr_char < len(ciphertext):
                pointer = ciphertext[curr_char];
                key = (pointer,in_wheel);
                brute_force_attempt.set_key(key);
                
                plaintext = brute_force_attempt.decrypt(ciphertext)
                keyfound = utilities.is_plaintext(plaintext, dict_list, threshold)
                curr_char += 1

        
        #check for failure   
        if keyfound == False:
            print('Alberti.cryptanalyze: cryptanalysis failed')
            return '',''
        
        return (key,plaintext)
        
    
    
    
    
    