import utilities
from mod import MOD
from psuedoNumGen import PRNG
from copy import deepcopy

class SBOX:
    """
    ----------------------------------------------------
    Description: SDES SBOX
    ----------------------------------------------------
    """
    def __init__(self, filename = ''):
        """
        ----------------------------------------------------
        Parameters:   _box (list): default value = [[],[]]
                      _size (int): #bits for input, default = 0
        Description:  Creates an SBOX from a given file
                      The contents of the file are read into a 2D list
                      The size represent #bits for the sbox input
                      Note that the output #bits is (size - 1)
        ---------------------------------------------------
        """
        if filename == '':  
            self._box = [[],[]]
            self._size = 0
        
        else:
            self.set_box(filename)
            
            
    def is_empty(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       True/False
        Description:  Check if current sbox is empty
        ---------------------------------------------------
        """ 
        isempty = False
        if self.get_box() == [[],[]]:
            isempty = True
        return isempty
    
    def get_box(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       box (list)
        Description:  Returns a copy of _box
        ---------------------------------------------------
        """ 
        return deepcopy(self._box)
    
    def get_size(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       size (int)
        Description:  Returns a copy of current sbox size
        ---------------------------------------------------
        """ 
        return deepcopy(self._size)
    
    @staticmethod
    def valid_box(box):
        """
        ----------------------------------------------------
        Parameters:   box (?)
        Return:       True/False
        Description:  Check if given output is a valid box
                      A valid box is a 2D list, composing of 2 rows
                      Both rows have same #columns
                      All items in the 2D list are binary numbers of
                          equal number of bits
        ---------------------------------------------------
        """ 
        valid_box = True
        
        #check for 2 rows
        if type(box) is list and len(box) == 2:
            
            sub_box1 = box[0]
            sub_box2 = box[1]
            
            #make sure that the len of the two inner lists are the same
            if len(sub_box1) != len(sub_box2):
                valid_box = False


            #we need to make sure all of the binary numbers are the same length 
            #we need to make sure all of the numbers are binary           
            common_length = len(str(sub_box1[0]))
            
            for binary in sub_box1:
                is_binary = utilities.is_binary(binary)
                
                if is_binary == False or len(str(binary)) != common_length:
                    valid_box = False
                    break
                    
            for binary in sub_box2:
                is_binary = utilities.is_binary(binary)
                
                if is_binary == False or len(str(binary)) != common_length:
                    valid_box = False
                    break
                    
        else:
            valid_box = False
           
           
        return valid_box
    
    def set_box(self, filename):
        """
        ----------------------------------------------------
        Parameters:   filename (str)
        Return:       success: True/False
        Description:  Read contents of a file into _box
                      file is formatted as:
                        <item[0][0]>-<item[0][1]>-...-<item[0][n-1]>
                        <item[1][0]>-<item[1][1]>-...-<item[1][n-1]>
                      where n is the size
                      if successful, values of _box and _size are updated
                      otherwise, no changes are applied to _box and _size
        ---------------------------------------------------
        """ 
        success = False
                
        if utilities.is_valid_filename(filename):
            
            #we pop contents as splitting it results in 3 items 
            contents = utilities.file_to_text(filename).split('\n')
            contents.pop()
            
            #print("contents + " + str(contents))
            
            box = []
            for boxes in contents:
                box.append(boxes.split('-'))            
            
            if SBOX.valid_box(box):
                
                #for box
                self._box = box
                
                #for size
                self._size = len(box[0][0]) + 1 #+1 for msb
                                
                success = True
                
        return success
    
    
    def substitute(self, value):
        """
        ----------------------------------------------------
        Parameters:   value (str): sbox input (binary num of size bits)
        Return:       result (str): sbox output (binary num of size-1 bits)
        Description:  substitute <value> to corresponding output in sbox
                      if invalid input return ''
        ---------------------------------------------------
        """ 
        sbox_out = ''
        
        #ensure value is string, is the same size to sub with the table, and is a binary number
        if type(value) is str and len(value) == self.get_size() and utilities.is_binary(value):
            
            #first bit in value is the row 
            row = int(value[0])
            
            #subsequent bits are the corresponding column #
            col = value[1:]
            col_num = utilities.bin_to_dec(col)
            
            #ensure there is a column number of size n
            sub_box = self.get_box()
            if col_num <= len(sub_box[0]):
                sbox_out = sub_box[row][col_num]
        
        return sbox_out
    
    
    def __str__(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       output (str)
        Description:  Constructs and returns a string representation of SBOX object
                      format:
                      SBOX(<size>):
                      <_box[0]>
                      <_box[1]>
        ---------------------------------------------------
        """ 
        return 'SBOX(' + str(self.get_size()) + '):\n' + str(self.get_box()[0]) + '\n' + str(self.get_box()[1])



class SDES:
    DEFAULT_ENCODING = 'B6'
    DEFAULT_BLOCK_SIZE = 12
    DEFAULT_KEY_LENGTH = 9
    DEFAULT_ROUNDS = 2
    DEFAULT_P = 103
    DEFAULT_Q = 199
    DEFAULT_SBOX1 = SBOX('sbox1.txt')
    DEFAULT_SBOX2 = SBOX('sbox2.txt')
    DEFAULT_PAD = 'Q'

    def __init__(self):
        """
        ----------------------------------------------------
        Parameters:   _rounds (int)
                      _key_length (int)
                      _block_size (int)
                      _encoding (str): set to B6
                      _p (int)
                      _q (int)
                      _sbox1 (SBOX)
                      _sbox2 (SBOX)
                      _pad (str)
        Description:  Constructs an SDES object
                      All parameters are set to default values
        ---------------------------------------------------
        """
        
        self._rounds = self.DEFAULT_ROUNDS
        
        self._key_length = self.DEFAULT_KEY_LENGTH
        
        self._block_size = self.DEFAULT_BLOCK_SIZE
        
        self._encoding = self.DEFAULT_ENCODING
        
        self._p = self.DEFAULT_P
        
        self._q = self.DEFAULT_Q
        
        self._sbox1 = self.DEFAULT_SBOX1
        
        self._sbox2 = self.DEFAULT_SBOX2
        
        self._pad = self.DEFAULT_PAD
        
        
    def get_value(self, parameter):
        """
        ----------------------------------------------------
        Parameters:   parameter (str)
        Return:       value (?)
        Description:  Returns a copy of parameter value
                      Valid parameter names:
                      rounds, key_length, block_size
                      encoding, p, q, sbox1, sbox2, pad
                      if invalid parameter name --> print error msg & return ''
        ---------------------------------------------------
        """
        #parameter is to get any of the values:
        
        #encoding
        if parameter == 'encoding':
            return deepcopy(self._encoding)
        #rounds
        elif parameter == 'rounds':
            return deepcopy(self._rounds)
        #block_size
        elif parameter == 'block_size':
            return deepcopy(self._block_size)
        #key_length
        elif parameter == 'key_length':
            return deepcopy(self._key_length)
        #p
        elif parameter == 'p':
            return deepcopy(self._p)
        #q
        elif parameter == 'q':
            return deepcopy(self._q)
        #sbox1
        elif parameter == 'sbox1':
            return deepcopy(self._sbox1)
        #sbox2
        elif parameter == 'sbox2':
            return deepcopy(self._sbox2)
        #pad
        elif parameter == 'pad':
            return deepcopy(self._pad)
        else:
            print('Error: incorrect parameter entered for get_value')
            return ''
         
    
    def set_parameter(self,parameter,value):
        """
        ----------------------------------------------------
        Parameters:   parameter (str)
                      value (?)
        Return:       success: True/False
        Description:  Set the given parameter to given value (if valid)
                      if invalid value, do not update current value
                      if invalid parameter name, print error msg and return ''
                      
                      rounds should be an integer larger than 1
                      p and q should be integers congruent to 3 mod 4
                      pad should be a single character string in B6 encoding
                      sbox1 and sbox2 should be non-empty SBOX objects
                      block_size should be an integer of multiples of 2, >= 4
                          sets also key_length to block_size//2 + 3
                      cannot set key_length
                      
                      If invalid value, return False
                      if invalid parameter name, print error msg and return False
        ---------------------------------------------------
        """
                
        success = True
        
        #encoding
        if parameter == 'encoding':
            #The encoding parameter can only be set to 'B6'.
            self._encoding = self.DEFAULT_ENCODING
            
        #rounds
        elif parameter == 'rounds':
            #The rounds should be an integer larger than 1
            if type(value) != int or value <= 1:
                success = False
            else:
                self._rounds = value
            
        
        #block_size
        elif parameter == 'block_size':
            #The block_size should be a power of 2, greater than or equal to 4
            #When setting the block_size, the key_length is automatically set to (block_size/2) + 3. 
            #(The 3 comes from 2 for expand function, and 1 for key generation function).
            if type(value) != int or value < 4 or value%2!=0:
                success = False
            else:
                self._block_size = value
                self._key_length = (self._block_size / 2) + 3
            
            
        #key_length
        elif parameter == 'key_length':            
            if type(value) != int and value > 1:
                success = False
            else:
                self._key_length = value
                
        #p
        elif parameter == 'p':
            #The p should be congruent to 3 mod 4
            if type(value) == int:
                
                modobj_default = MOD(3, 4)
                modobj_value = MOD(value, 4)
                
                is_congruent = modobj_default.is_congruent(modobj_value)
                
                if is_congruent:
                    self._p = value
    
            else:
                success = False
                    
        #q
        elif parameter == 'q':
            #The q should be congruent to 3 mod 4
            if type(value) == int:
                
                modobj_default = MOD(3, 4)
                modobj_value = MOD(value, 4)
                
                is_congruent = modobj_default.is_congruent(modobj_value)
                
                if is_congruent:
                    self._q = value
    
            else:
                success = False

        
        #sbox1
        elif parameter == 'sbox1':
            #The sbox1 should be a non-empty SBOX object
            if type(value) == SBOX and value.is_empty() == False:
                self._sbox1 = value
                
            else:
                success = False
        
        #sbox2
        elif parameter == 'sbox2':
            #The sbox2 should be a non-empty SBOX object
            if type(value) == SBOX and value.is_empty() == False:
                self._sbox2 = value
                
            else:
                success = False
        
        #pad
        elif parameter == 'pad':
            #pad should be a single character string in B6 encoding
            B6 = utilities.get_base('B6')
            
            if value in B6:
                self._pad = value
            else:
                success = False
                
        else:
            print('Error: incorrect parameter entered for set_parameter')
            success = False
        
        return success


    def get_key(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       key (str): binary number
        Description:  Returns a copy of SDES key
                      The key is generated by Blum Blum Shub algorithm
                      Uses p and q to generates key_length bits
        ---------------------------------------------------
        """
        key = PRNG.BBS(self.get_value('p'), self.get_value('q'), self.get_value('key_length'))
        return deepcopy(key)
    
    
    def get_subkey(self,i):
        """
        ----------------------------------------------------
        Parameters:   i (int): subkey index
        Return:       subkey (str): binary number
        Description:  Returns the ith subkey from SDES key
                      Gets key_length bits from key starting at index i
                      Using circular indexing if necessary
        Errors:       if invalid i --> return ''
        ---------------------------------------------------
        """
        
        subkey = ''
        
        if type(i) == int and i > -1:
            
            #The method get_subkey(i) generates the ith subkey, which is the key_length bits 
            #starting at key index i, using circular method if necessary. 
            #in notes its the first 8-bits for subkey
            temp = utilities.shift_string(self.get_key(), i, 'l')
            length_of_key = self.get_value('key_length')
            subkey = temp[0:length_of_key-1]
        
        return subkey
        
        
        
    def expand(self,R):
        """
        ----------------------------------------------------
        Parameters:   R (str): binary number of size (block_size/2)
        Return:       R_exp (str): output of expand function
        Description:  Expand the input binary number by adding two digits
                      Expansion works as the following:
                      If the index of the two middle elements is i and i+1
                          indices 0 up to i-1: same order
                          middle becomes: R(i+1)R(i)R(i+1)R(i)
                          indices R(i+2) to the end: same order
                      No need to validate that R is of size block_size/2
        Errors:       if R is an invalid binary number -->  return ''
        ---------------------------------------------------
        """
        R_exp = ''
        
        if type(R) is str and utilities.is_binary(R):
            
            middle = len(R)//2 - 1
            #print('\n')            
            #print("middle: " + str(middle))
            R_exp = R_exp + R[0:middle]
            #print("start of R_exp: " + R_exp)
            R_exp = R_exp + (R[middle+1] + R[middle] + R[middle+1] + R[middle])
            #print("middle of R_exp: " + R_exp)
            R_exp = R_exp + R[(middle+2):len(R)]
            #print("end of R_exp: " + R_exp)
            
        return R_exp
 
    
    def F(self,Ri,ki):
        """
        ----------------------------------------------------
        Parameters:   Ri (str): block of binary numbers
                      ki (str): binary number representing subkey
        Return:       Ri2 (str): block of binary numbers
        
        Description:  Performs the following five tasks:
                      1- Pass the Ri block to the expander function
                      2- Xor the output of [1] with ki
                      3- Divide the output of [2] into two equal sub-blocks
                      4- Pass the most significant bits of [3] to Sbox1
                         and least significant bits to sbox2
                      5- Concatenate the output of [4] as [sbox1][sbox2]
                      
        Errors:       if ki or Ri is an invalid binary number --> return ''
        ---------------------------------------------------
        """
        Ri2 = ''
                
        if type(Ri) == str and type(ki) == str and utilities.is_binary(Ri) and utilities.is_binary(ki) and len(Ri) + 2 == len(ki):  #the last clause is to correct xor error
            
            #print("Ri: " + Ri)
            #print("ki: " + ki)
            
            
            #1-  Pass the Ri block to the expander function
            Ri_exp = self.expand(Ri)
            #print("Ri expanded: " + Ri_exp)
            
            #this clause is to correct xor error
            if len(Ri_exp) == len(ki):
                #2 - Xor the output of [1] with ki
                xor_output = utilities.xor(Ri_exp, ki)
                #print("xor output: " + xor_output)
                
                #3 - Divide the output of [2] into two equal sub-blocks
                sub_block1 = xor_output[:len(xor_output)//2]
                sub_block2 = xor_output[len(xor_output)//2:]
                #print("sub_block1: " + sub_block1)
                #print("sub_block2: " + sub_block2)
                
                #4 - Pass the most significant bits of [3] to Sbox1 and least significant bits to sbox2
                sbox1 = self.get_value('sbox1')
                sbox2 = self.get_value('sbox2')
                
                passed_block1 = sbox1.substitute(sub_block1)
                passed_block2 = sbox2.substitute(sub_block2)
                
                #print("passed block 1: " + passed_block1)
                #print("passed block 2: " + passed_block2)
                
                #5 - Concatenate the output of [4] as [sbox1][sbox2]
                concatenated_bits = passed_block1 + passed_block2
                #print("Concatenated Bits: " + concatenated_bits)
                
                Ri2 = concatenated_bits
        
        return Ri2


    def feistel(self,bi,ki):
        """
        ----------------------------------------------------
        Parameters:   bi (str): block of binary numbers
                      ki (str): binary number representing subkey
        Return:       bi2 (str): block of binary numbers
        
        Description:  Applies Feistel Cipher on a block of binary numbers
                      L(current) = R(previous)
                      R(current) = L(previous) xor F(R(previous), subkey)
        Errors:       if ki or bi is an invalid binary number --> return ''
        ---------------------------------------------------
        """
        
        #one round of fiestal
        bi2 = ''
        if type(bi) is str and type(ki) is str and utilities.is_binary(bi) and utilities.is_binary(ki): 
            
            #split the Li and Ri
            middle = len(bi)//2
            
            Li = bi[:middle]
            Ri = bi[middle:]
            
            #take the right side, put it on the left
            #take the right side, throw it through F function, then xor it with the left side. Becomes new right side
            new_Li = Ri
            new_Ri = self.F(Ri, ki)
            
            #print(Li)
            #print(new_Ri)
            #this last clause is to correct xor error
            if len(Li) == len(new_Ri):
                new_Ri = utilities.xor(Li, new_Ri)
                
                #add together the new two sides
                bi2 = new_Li + new_Ri
        
        
        return bi2
    
    
    def encrypt(self,plaintext,mode):
        """
        ----------------------------------------------------
        Parameters:   plaintext (str)
                      mode (str)
        Return:       ciphertext (str)
        Description:  A dispatcher SDES encryption function
                      passes the plaintext to the proper function based on given mode
                      Works for ECB, CBC and OFB modes
        Errors:       if undefined mode --> return ''
        ---------------------------------------------------
        """
        ciphertext = ''
        
        #MODES:
        
        #ECB
        if mode == 'ECB':
            ciphertext = self._encrypt_ECB(plaintext)
        #CBC
        elif mode == 'CBC':
            ciphertext = self._encrypt_CBC(plaintext)
        #OFB
        elif mode == 'OFB':
            ciphertext = self._encrypt_OFB(plaintext)
        
        return ciphertext
    
    
    def decrypt(self,ciphertext,mode):
        """
        ----------------------------------------------------
        Parameters:   ciphertext (str)
                      mode (str)
        Return:       plaintext (str)
        Description:  A dispatcher SDES decryption function
                      passes the ciphertext to the proper function based on given mode
                      Works for ECB, CBC and OFB modes
        Errors:       if undefined mode --> return ''
        ---------------------------------------------------
        """
        plaintext = ''
        
        #MODES:
        
        #ECB
        if mode == 'ECB':
            plaintext = self._decrypt_ECB(ciphertext)
        #CBC
        elif mode == 'CBC':
            plaintext = self._decrypt_CBC(ciphertext)
        #OFB
        elif mode == 'OFB':
            plaintext = self._decrypt_OFB(ciphertext)
        
        return plaintext
    
    
    
    def _encrypt_ECB(self, plaintext):
        """
        ----------------------------------------------------
        Parameters:   plaintext (str)
        Return:       ciphertext (str)
        Description:  SDES encryption using ECB mode
        ---------------------------------------------------
        """         
        #The two methods use the ECB mode to encrypt/decrypt a given text. The feistel network is 
        #called as many as rounds. For the last round, the two sides (R and L) are swapped.
                
        #remove all the characters that are not in base before encryption 
        base = utilities.get_base(self.get_value('encoding'))
        #print(base)
        
        not_in_base_str = ''
        for char in plaintext:
            if char not in base:
                not_in_base_str += char
        
        not_in_base = utilities.get_positions(plaintext, not_in_base_str)
        plaintext = utilities.clean_text(plaintext, not_in_base_str)   
        
        
        """Since the B6 encoding is used, for the standard block_size of 12, every two characters 
            in the input text will correspond to one block. If the last block contains one character, then 
            it needs to be padded."""
        #pair each char group in cipherblocks to blocksize
        plainblocks = utilities.text_to_blocks(plaintext, 2, True, self.get_value('pad'))
        
        #print(plainblocks)
        
        #encode each char in the cipherblock to B6 encoding
        encoded_plain = ''
        for block in plainblocks:
            for char in block:
                encoded_plain += utilities.encode(char, self.get_value('encoding'))
        
        #print(encoded_plain)
        
        
        #split into block_sized blocks and run them the n rounds fiestal
        encoded_blocks = utilities.text_to_blocks(encoded_plain, self.get_value('block_size'), True, self.get_value('pad'))
        #print(encoded_blocks)
        
        encrypted_block_code = ''
        cipherstream = ''
        rounds = self.get_value('rounds') 
        for block_code in encoded_blocks:
            
            #print("\ncurrent codeblock: " + str(block_code))
            for i in range(rounds+1):

                if i == 0:
                    #print("current subkey: " + str(i) + " -> " + str(self.get_subkey(i)))
                    encrypted_block_code = self.feistel(block_code, self.get_subkey(i))
                
                elif i < rounds:
                    #print("current subkey: " + str(i) + " -> " + str(self.get_subkey(i)))
                    encrypted_block_code = self.feistel(encrypted_block_code, self.get_subkey(i))
                
                else:
                #for the last "round" we need to swap the left half and the right half for ECB
                    #print('I swap')
                    middle = len(encrypted_block_code)//2
                    right = encrypted_block_code[middle:]
                    left = encrypted_block_code[:middle]
                    
                    encrypted_block_code = right + left
                    
                    #add final to the cipherstream
                    cipherstream += encrypted_block_code
                    
                #print("encrypted_block_code: " + str(i) + " -> " + str(encrypted_block_code))
                
        #print("encrypted code (cipherstream): " + cipherstream)
        

        #decode encrypted_code back into characters
        decoded_ciphertext = ''
        for chars in range(0, len(cipherstream), 6):
            to_decode = cipherstream[chars:chars+6]
            decoded_ciphertext += utilities.decode(to_decode, self.get_value('encoding'))
        
        #print("encoded plain: " + str(decoded_ciphertext))
                
        
        #reinsert the non-enciphered char
        ciphertext = decoded_ciphertext
        ciphertext = utilities.insert_positions(ciphertext, not_in_base)
        ciphertext = ciphertext.rstrip(self.get_value('pad'))
        
        return ciphertext
    
    
    
    def _decrypt_ECB(self,ciphertext):
        """
        ----------------------------------------------------
        Parameters:   ciphertext (str)
        Return:       plaintext (str)
        Description:  SDES decryption using ECB mode
        ---------------------------------------------------
        """
        #same idea, but we need to run the encryption bit backwards
        #then we need to run the rounds backwards n->0
        #we need to swap left and right back to original position
        
        
        #remove all the characters that are not in base before encryption 
        base = utilities.get_base(self.get_value('encoding'))
        
        not_in_base_str = ''
        for char in ciphertext:
            if char not in base:
                not_in_base_str += char
        
        not_in_base = utilities.get_positions(ciphertext, not_in_base_str)
        ciphertext = utilities.clean_text(ciphertext, not_in_base_str)   
        
        #pair each char group in cipherblocks to blocksize
        cipherblocks = utilities.text_to_blocks(ciphertext, 2, True, self.get_value('pad'))
        
        #encode each char in the cipherblock to B6 encoding
        encoded_cipher = ''
        for block in cipherblocks:
            for char in block:
                encoded_cipher += utilities.encode(char, self.get_value('encoding'))
        
        #split into block_sized blocks and run them the n rounds fiestal
        encoded_blocks = utilities.text_to_blocks(encoded_cipher, self.get_value('block_size'), True, self.get_value('pad'))
        
        encrypted_block_code = ''
        cipherstream = ''
        rounds = self.get_value('rounds') 
                
        for block_code in encoded_blocks:
            
            #print("\ncurrent codeblock: " + str(block_code))
            #we need to start with the last round swap and then the subkeys in inverse of encryption
            for i in range(rounds-1, -2, -1):
                
                if i == rounds-1:
                    #print("current subkey: " + str(i) + " -> " + str(self.get_subkey(i)))
                    encrypted_block_code = self.feistel(block_code, self.get_subkey(i))
                
                elif i < rounds and i != -1:
                    #print("current subkey: " + str(i) + " -> " + str(self.get_subkey(i)))
                    encrypted_block_code = self.feistel(encrypted_block_code, self.get_subkey(i))
                
                else:
                #for the last "round" we need to swap the left half and the right half for ECB
                    #print('I swap')
                    middle = len(encrypted_block_code)//2
                    right = encrypted_block_code[middle:]
                    left = encrypted_block_code[:middle]
                    
                    encrypted_block_code = right + left
                    
                    #add final to the cipherstream
                    cipherstream += encrypted_block_code
                    
                #print("encrypted_block_code: " + str(i) + " -> " + str(encrypted_block_code))
        
        
        #print("cipherstream: " + str(cipherstream))
        #decode encrypted_code back into characters
        decoded_plaintext = ''
        for chars in range(0, len(cipherstream), 6):
            to_decode = cipherstream[chars:chars+6]
            decoded_plaintext += utilities.decode(to_decode, self.get_value('encoding'))        
        
        #reinsert the non-enciphered char
        plaintext = decoded_plaintext
        plaintext = utilities.insert_positions(plaintext, not_in_base)
        plaintext = plaintext.rstrip(self.get_value('pad'))
        
        return plaintext        
        
        
    
    def _encrypt_CBC(self,plaintext):
        """
        ----------------------------------------------------
        Parameters:   plaintext (str)
        Return:       ciphertext (str)
        Description:  SDES encryption using CBC mode
        ---------------------------------------------------
        """ 
        #pretty sure itll be the same as the ECB but:
        #1 - we need to xor IV with the plaintext binary first
        #2 - after we get our cipher binary, we then save it to use as the next IV
        #3 - repeat steps 1 and 2
        
        iv = self.get_IV()
        #print("IV: " + str(iv))
        
        #remove all the characters that are not in base before encryption 
        base = utilities.get_base(self.get_value('encoding'))        
        not_in_base_str = ''
        for char in plaintext:
            if char not in base:
                not_in_base_str += char
        
        not_in_base = utilities.get_positions(plaintext, not_in_base_str)
        plaintext = utilities.clean_text(plaintext, not_in_base_str)   
        
        #pair each char group in cipherblocks to blocksize
        plainblocks = utilities.text_to_blocks(plaintext, 2, True, self.get_value('pad'))
        
        #encode each char in the cipherblock to B6 encoding
        encoded_plain = ''
        for block in plainblocks:
            for char in block:
                encoded_plain += utilities.encode(char, self.get_value('encoding'))
                
        #split into block_sized blocks
        encoded_blocks = utilities.text_to_blocks(encoded_plain, self.get_value('block_size'), True, self.get_value('pad'))
        
        #run them the n rounds fiestal
        encrypted_block_code = ''
        prev_encrypted_block_code = iv
        cipherstream = ''
        rounds = self.get_value('rounds') 
        for block_code in encoded_blocks:
            
            #now we need to XOR the next encrypted_block with the previous block or iv on first iteration
            block_code = utilities.xor(prev_encrypted_block_code, block_code)
            
            #print("\ncurrent codeblock: " + str(block_code))
            for i in range(rounds+1):
                
                if i == 0:
                    #print("current subkey: " + str(i) + " -> " + str(self.get_subkey(i)))
                    encrypted_block_code = self.feistel(block_code, self.get_subkey(i))
                
                elif i < rounds:
                    #print("current subkey: " + str(i) + " -> " + str(self.get_subkey(i)))
                    encrypted_block_code = self.feistel(encrypted_block_code, self.get_subkey(i))
                
                else:
                    #for the last "round" we need to swap the left half and the right half for ECB
                    middle = len(encrypted_block_code)//2
                    right = encrypted_block_code[middle:]
                    left = encrypted_block_code[:middle]
                    
                    encrypted_block_code = right + left
                    
                    #add final to the cipherstream
                    cipherstream += encrypted_block_code
                
                
                #print("encrypted_block_code: " + str(i) + " -> " + str(encrypted_block_code))
            
            prev_encrypted_block_code = encrypted_block_code
            #print('------------------------')

    
        #decode encrypted_code back into characters
        decoded_ciphertext = ''
        for chars in range(0, len(cipherstream), 6):
            to_decode = cipherstream[chars:chars+6]
            decoded_ciphertext += utilities.decode(to_decode, self.get_value('encoding'))
                        
        
        #reinsert the non-enciphered char
        ciphertext = decoded_ciphertext
        ciphertext = utilities.insert_positions(ciphertext, not_in_base)
        ciphertext = ciphertext.rstrip(self.get_value('pad'))
        
        return ciphertext
        
        
    def get_IV(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       iv (str): binary number
        Description:  prepares an IV for CBC and OFB modes
                      see PDF for instructions
        ---------------------------------------------------
        """ 
        #the IG is the binary representation of the key_length
        #number of bits is equal to block_size
        #number of registers is equivalent to the key_length divided by 2
        IG =  utilities.dec_to_bin(self.get_value('key_length'), None)
        bits = self.get_value('block_size')
        registers = self.get_value('key_length')//2
        
        #the c vector is a binary stream that alternates between 0 and 1 for number of times equal to the number of registers
        #get the c vector and convert it to a feedback string for LFSR
        feedback = ''
        c = []
        swap = True
        for _ in range(registers):
            if swap:
                c.append(0)
                swap = False
            else:
                c.append(1)
                swap = True
        
        for bit in c:
            feedback += str(bit)
        
        #print(c)
        #print(feedback)
        #print(IG)
        iv = PRNG.LFSR(str(feedback), IG, bits)
                
        return iv


    def _decrypt_CBC(self,ciphertext):   
        """
        ----------------------------------------------------
        Parameters:   ciphertext (str)
        Return:       plaintext (str)
        Description:  SDES decryption using CBC mode
        ---------------------------------------------------
        """     
        #print('------------------------decrypt------------------------------')
        
        #so for decryption:
        #1 - we xor the first iteration with the iv AFTER decryption
        #2 - then subsequent iterations we xor with the previous ciphercode BEFORE it was decrypted 
        
        #get the iv
        iv = self.get_IV()
        
        #remove all the characters that are not in base before encryption 
        base = utilities.get_base(self.get_value('encoding'))
        
        not_in_base_str = ''
        for char in ciphertext:
            if char not in base:
                not_in_base_str += char
        
        not_in_base = utilities.get_positions(ciphertext, not_in_base_str)
        ciphertext = utilities.clean_text(ciphertext, not_in_base_str)   
        
        #pair each char group in cipherblocks to blocksize
        cipherblocks = utilities.text_to_blocks(ciphertext, 2, True, self.get_value('pad'))
        
        #encode each char in the cipherblock to B6 encoding
        encoded_cipher = ''
        for block in cipherblocks:
            for char in block:
                encoded_cipher += utilities.encode(char, self.get_value('encoding'))
        
        #split into block_sized blocks and run them the n rounds fiestal
        encoded_blocks = utilities.text_to_blocks(encoded_cipher, self.get_value('block_size'), True, self.get_value('pad'))
        
        encrypted_block_code = ''
        prev_cipher_block_code = iv
        cipherstream = ''
        rounds = self.get_value('rounds') 
        for block_code in encoded_blocks:
                        
            
            #print("\ncurrent codeblock: " + str(block_code))
            #we need to start with the last round swap and then the subkeys in inverse of encryption
            for i in range(rounds-1, -2, -1):
                
                if i == rounds-1:
                    encrypted_block_code = self.feistel(block_code, self.get_subkey(i))
                
                elif i < rounds and i != -1:
                    encrypted_block_code = self.feistel(encrypted_block_code, self.get_subkey(i))
                
                else:                    
                    
                    #for the last "round" we need to swap the left half and the right half for ECB
                    middle = len(encrypted_block_code)//2
                    right = encrypted_block_code[middle:]
                    left = encrypted_block_code[:middle]
                    
                    encrypted_block_code = right + left
                    
                    #perform the xor
                    encrypted_block_code = utilities.xor(prev_cipher_block_code, encrypted_block_code)
                    
                    #add final to the cipherstream
                    cipherstream += encrypted_block_code
                
                #print("encrypted_block_code: " + str(i) + " -> " + str(encrypted_block_code))
            
            prev_cipher_block_code = block_code
            
            #print('------------------------')
        
        #print("cipherstream: " + str(cipherstream))
        #decode encrypted_code back into characters
        decoded_plaintext = ''
        for chars in range(0, len(cipherstream), 6):
            to_decode = cipherstream[chars:chars+6]
            decoded_plaintext += utilities.decode(to_decode, self.get_value('encoding'))        
        
        #reinsert the non-enciphered char
        plaintext = decoded_plaintext
        plaintext = utilities.insert_positions(plaintext, not_in_base)
        plaintext = plaintext.rstrip(self.get_value('pad'))
        
        return plaintext
        
        
    def _encrypt_OFB(self,plaintext):
        """
        ----------------------------------------------------
        Parameters:   plaintext (str)
        Return:       ciphertext (str)
        Description:  SDES encryption using OFB mode
        ---------------------------------------------------
        """      
        
        #so the main differences:
        #1 - we need to encrypt IV this time, we call it "nonce"
        #2 - we then run the encryption on the Nonce
        #3 - our ciphertext is produced by the XOR of our plaintext_block and the Nonce output
        #4 - repeat 2 and 3 for all blocks
        #5 - Note: the last block is not padded, so we want to take only the MSB (most sig. bits) from the key
        iv = self.get_IV()
        
        #remove all the characters that are not in base before encryption 
        base = utilities.get_base(self.get_value('encoding'))        
        not_in_base_str = ''
        for char in plaintext:
            if char not in base:
                not_in_base_str += char
        
        not_in_base = utilities.get_positions(plaintext, not_in_base_str)
        plaintext = utilities.clean_text(plaintext, not_in_base_str)   
        
        
        #if the plaintext is not a power of 2 then it would normally need padded:
        #but for OFB we dont do padding so we need to set a boolean to remind us
        msb_case = False
        if len(plaintext) % 2 != 0:
            msb_case = True
        
        
        #pair each char group in cipherblocks to blocksize
        plainblocks = utilities.text_to_blocks(plaintext, 2, False, None)
        
        #encode each char in the cipherblock to B6 encoding
        encoded_plain = ''
        for block in plainblocks:
            for char in block:
                encoded_plain += utilities.encode(char, self.get_value('encoding'))
                
        #split into block_sized blocks, no padding for OFB
        encoded_blocks = utilities.text_to_blocks(encoded_plain, self.get_value('block_size'), False, None)
        
        #print(encoded_blocks)
        
        #run them the n rounds fiestal
        nonce = ''
        prev_nonce = iv
        cipherstream = ''
        rounds = self.get_value('rounds') 
        for block_code in encoded_blocks:
        
            #print("current codeblock: " + str(block_code))
            for i in range(rounds+1):
                
                if i == 0:
                    nonce = self.feistel(prev_nonce, self.get_subkey(i))
                
                elif i < rounds:
                    nonce = self.feistel(nonce, self.get_subkey(i))
                
                else:
                    #for the last "round" we need to swap the left half and the right half for ECB
                    middle = len(nonce)//2
                    right = nonce[middle:]
                    left = nonce[:middle]
                    
                    nonce = right + left
                    
                    #set the new prev_nonce for next round
                    prev_nonce = nonce
                    
                    #our ciphertext is produced by the XOR of our plaintext_block and the Nonce output
                    if msb_case and block_code == encoded_blocks[-1]:
                        encrypted_block_code = utilities.xor(nonce[:middle], block_code)
                    else:
                        encrypted_block_code = utilities.xor(nonce, block_code)
    
                    #add final to the cipherstream
                    cipherstream += encrypted_block_code
            
            #print("current nonce: " + str(nonce))
    
    
        #decode encrypted_code back into characters
        decoded_ciphertext = ''
        for chars in range(0, len(cipherstream), 6):
            to_decode = cipherstream[chars:chars+6]
            decoded_ciphertext += utilities.decode(to_decode, self.get_value('encoding'))
                        
        
        #reinsert the non-enciphered char
        ciphertext = decoded_ciphertext
        ciphertext = utilities.insert_positions(ciphertext, not_in_base)
        ciphertext = ciphertext.rstrip(self.get_value('pad'))
        
        return ciphertext



    def _decrypt_OFB(self,ciphertext):
        """
        ----------------------------------------------------
        Parameters:   ciphertext (str)
        Return:       plaintext (str)
        Description:  SDES decryption using OFB mode
        ---------------------------------------------------
        """
        #Encryption and Decryption are exactly the same logically
        #so all we have to do is "re-encrypt" the ciphertext and we get our plaintext
        plaintext = self._encrypt_OFB(ciphertext)
        return plaintext
    
    
    
    
    
    