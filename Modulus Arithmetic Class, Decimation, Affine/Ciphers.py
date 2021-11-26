"""
-------------------------------------
File: Ciphers.py
File description
Cryptanalysis class, shift cipher, Vigenere implementations
-------------------------------------
Author:  Chandler Mayberry
Version  2021-11-03
-------------------------------------
"""

import utilities

class MOD:
    """
    ----------------------------------------------------
    Description: Modular Arithmetic Library
    ----------------------------------------------------
    """
    DEFAULT_VALUE = 0
    DEFAULT_MOD = 2
    
    def __init__(self,value=DEFAULT_VALUE,mod=DEFAULT_MOD):
        """
        ----------------------------------------------------
        Parameters:   _value (int): default value = 0
                      _mod(int): default value = 2
        Description:  Creates a number in modular format
                      sets _value and _mod
        ---------------------------------------------------
        """
        self._value = self.DEFAULT_VALUE
        if value != self.DEFAULT_VALUE:
            self.set_value(value)
            
        self._mod = self.DEFAULT_MOD
        if mod != self.DEFAULT_MOD:
            self.set_mod(mod)
        
        return
    
    
    def __str__(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       output (str)
        Description:  Constructs and returns a string representation of 
                      a MOD object
                      output format:
                      <_value>
        ---------------------------------------------------
        """
        
        return str(self._value)
    
    
    def print(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       -
        Description:  prints string representation of 
                      a MOD object in the following format:
                      <_value> mod <_mod>
        ---------------------------------------------------
        """
        print(str(self.get_value()) + " mod " + str(self.get_mod()))
        return 
    
    
    def set_value(self,value):
        """
        ----------------------------------------------------
        Parameters:   value (int): an arbitrary integer
        Return:       success: True/False
        Description:  Sets MOD object value to given value
                      if invalid value (i.e., not an integer) --> 
                          set to default value
        ---------------------------------------------------
        """ 
        success = False
        
        if type(value) != int:
            self._value = self.DEFAULT_VALUE
        else:
            success = True
            self._value = value
        
        return success
    
    
    def set_mod(self,mod):
        """
        ----------------------------------------------------
        Parameters:   mod (int): an arbitrary integer
        Return:       success: True/False
        Description:  Sets MOD object mod to given value
                      if invalid mod (i.e., anything but integers >= 2) --> 
                          set to default mod
        ---------------------------------------------------
        """ 
        success = False
        
        if type(mod) != int or self._mod < 2:
            self._mod = self.DEFAULT_MOD
        else:
            success = True
            self._mod = mod
        
        return success
    
    
    def get_value(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       value (int)
        Description:  Returns a copy of the value
        ---------------------------------------------------
        """
        return self._value
    
    
    def get_residue(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       residue (int)
        Description:  Returns the residue of the stored value
                        using the stored mod
                      A residue is the smallest positive integer
                      that is congruent to value mod m
                      Example:  residue 16 mod 5 --> 1
        ---------------------------------------------------
        """
        #residue is just the leftovers from a mod operation
        value = self._value
        mod = self._mod
        residue = value % mod
        return residue
    
    
    def get_mod(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       mod (int)
        Description:  Returns a copy of the mod
        ---------------------------------------------------
        """
        return self._mod


    def get_residue_list(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       residue_list (list)
        Description:  Constructs and returns a list that contains
                        All integers from 0 up to mod -1
                      Example: residue_list(5) --> [0,1,2,3,4]
        ---------------------------------------------------
        """
        #less of a residue list and more of 0-n-1 with n being the mod #
        return [i for i in range(self._mod)]
    
    
    def is_congruent(self, num2):
        """
        ----------------------------------------------------
        Parameters:   num2 (MOD): an arbitrary MOD object
        Return:       True/False
        Description:  Checks if current number and given num2 
                        are congruent to each other
                      Both numbers should be of the same mod
        Errors:       if input is not a MOD object return:
                        'Error(MOD.is_congruent): invalid input'
        ---------------------------------------------------
        """
        
        if type(num2) != MOD:
            'Error(MOD.is_congruent): invalid input'
            return
                
        congruent = False
        
        #two numbers are congruent under these conditions if they both result in the same remainder
        #after mod and share the same mod
        if num2.get_mod() == self.get_mod():

            remainder1 = self.get_residue()
            remainder2 = num2.get_residue()
    
            #print(remainder1)
            #print(remainder2)
            
            if remainder1 == remainder2:
                congruent = True
        
        
        return congruent

    @staticmethod
    def add(a,b):
        """
        ----------------------------------------------------
        Static Method
        Parameters:   a (MOD): an arbitrary MOD object
                      b (MOD): an arbitrary MOD object
        Return:       result (MOD): a + b mod m
        Description:  Adds the values of <a> and <b> and 
                        returns a MOD object containing the residue
                      Example: MOD(11,5) + MOD(3,5) = MOD(4,5)
        Errors:       if one of the inputs is not a MOD object
                      or if <a> and <b> mods are not equal:
                        return 'Error(MOD.add): invalid input'
        ---------------------------------------------------
        """
        #if they are not mod objects or if they do not share the same mod value
        if type(a) != MOD or type(b) != MOD or a.get_mod() != b.get_mod():
            return 'Error(MOD.add): invalid input'      
        
        mod = (a.get_value() + b.get_value()) % a.get_mod()
        
        #return new mod object                
        return MOD(mod, a.get_mod())


    @staticmethod
    def sub(a,b):
        """
        ----------------------------------------------------
        Static Method
        Parameters:   a (MOD): an arbitrary MOD object
                      b (MOD): an arbitrary MOD object
        Return:       result (MOD): <a> - <b> mod m
        Description:  Subtracts the values of <b> from <a> and 
                        returns a MOD object containing the residue
                      Example: MOD(11,5) - MOD(3,5) = MOD(3,5)
        Errors:       if one of the inputs is not a MOD object
                      or if <a> and <b> mods are inequal:
                        return 'Error(MOD.sub): invalid input'
        ---------------------------------------------------
        """
        #if they are not mod objects or if they do not share the same mod value
        if type(a) != MOD or type(b) != MOD or a.get_mod() != b.get_mod():
            return 'Error(MOD.sub): invalid input'     
        
        mod = (a.get_value() - b.get_value()) % a.get_mod()
        
        #return new mod object                
        return MOD(mod, a.get_mod())
    
    
    def get_add_inv(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       result (int): additive inverse of current object
        Description:  Computes and returns the additive inverse of the 
                        current object
                      Example: additive inverse of 3 mod 5 is 2
        ---------------------------------------------------
        """
        
        #basically the opposite of leftovers, its the number that fills k up to mod ^^
        value = self.get_value() % self.get_mod()
        result = self.get_mod() - value
        
        return result


    @staticmethod
    def get_add_table(m):
        """
        ----------------------------------------------------
        Static Method
        Parameters:   m (int): an arbitrary mod
        Return:       add_table (2d list)
        Description:  Construct and return addition table mod m
                        element [r][c] represent r+c mod m
                      Example: MOD.get_add_table(2) --> [[0,1],[1,0]]
        Errors:       if m is not an integer >= 2:
                        return 'Error(MOD.get_add_table): invalid input'
        ---------------------------------------------------
        """
        add_table = []
        
        #error check
        if type(m) != int or m <= 1:
            return 'Error(MOD.get_add_table): invalid input'
            
        #for every position in the list, create a mod add table
        for pos1 in range(m):
            inner_list = []
            
            for pos2 in range(m):
                #this causes each inner list to shift to the right
                add_modded = (pos1 + pos2) % m
                inner_list.append(add_modded)
                
            add_table.append(inner_list)                
        
        return add_table


    @staticmethod
    def get_sub_table(m):
        """
        ----------------------------------------------------
        Static Method
        Parameters:   m (int): an arbitrary mod
        Return:       sub_table (2d list)
        Description:  Construct and return subtraction table mod m
                        element [r][c] represent r-c mod m
                      Example: MOD.get_sub_table(3) --> [[[0,2,1],[1,0,2],[2,1,0]]
        Errors:       if m is not an integer >= 2:
                        return 'Error(MOD.get_sub_table): invalid input'
        ---------------------------------------------------
        """
        sub_table = []
        
        #error check
        if type(m) != int or m <= 1:
            return 'Error(Mod.get_sub_table): invalid input'
            
        #for every position in the list, create a mod sub table
        for pos1 in range(m):
            
            inner_list = []
            for pos2 in range(m, 0, -1):
                #this causes each inner list to shift to the left
                sub_modded = (pos1 + pos2) % m
                inner_list.append(sub_modded)
                
            sub_table.append(inner_list)    
        
     
        
        return sub_table

    @staticmethod
    def get_add_inv_table(m):
        """
        ----------------------------------------------------
        Static Method
        Parameters:   m (int): an arbitrary mod
        Return:       add_inv_table (2d list)
        Description:  Construct and return additive inverse table mod m
                        Top row is num, bottom row is additive inverse
                      Example: MOD.get_add_inv_table(5) --> [[0,1,2,3,4],[0,4,3,2,1]]
        Errors:       if m is not an integer >= 2:
                        return 'Error(MOD.get_add_inv_table): invalid input'
        ---------------------------------------------------
        """
        #error check
        if type(m) != int or m <= 1:
            return 'Error(MOD.get_add_inv_table): invalid input'
            
        top_row_num = [i for i in range(m)]
        bot_row_inverse = [i for i in range(m)]
        
        #get both the current number for top row and its inverse for the opposite list
        for curr_digit in range(m):
            top_row_num[curr_digit] = curr_digit
            bot_row_inverse[curr_digit] = (m - curr_digit) % m
        
        add_inv_table = [top_row_num, bot_row_inverse]
        
        return add_inv_table
    
    
    @staticmethod
    def mul(a,b):
        """
        ----------------------------------------------------
        Static Method
        Parameters:   a (MOD): an arbitrary MOD object
                      b (MOD): an arbitrary MOD object
        Return:       result (MOD): <a> * <b> mod m
        Description:  Multiplies the values of <a> by <b> and 
                        returns a Mod object containing the residue
                      Example: MOD(11,5) - MOD(2,5) = MOD(2,5)
        Errors:       if one of the inputs is not a MOD object
                      or if <a> and <b> mods are inequal:
                        return 'Error(MOD.mul): invalid input'
        ---------------------------------------------------
        """        
        
        if type(a) != MOD or type(b) != MOD or a.get_mod() != b.get_mod():
            return 'Error(MOD.mul): invalid input'
        
        mod = MOD((a.get_value() * b.get_value()) % a.get_mod(), a.get_mod())
        
        return mod
    
    @staticmethod
    def get_mul_table(m):
        """
        ----------------------------------------------------
        Static Method
        Parameters:   m (int): an arbitrary mod
        Return:       mul_table (2d list)
        Description:  Construct and return multiplication table mod m
                        element [r][c] represent r*c mod m
                      Example: Mod.get_mul_table(4) --> 
                       [[0, 0, 0, 0], [0, 1, 2, 3], [0, 2, 0, 2], [0, 3, 2, 1]]
        Errors:       if m is not an integer >= 2:
                        return 'Error(MOD.get_mul_table): invalid input'
        ---------------------------------------------------
        """
        mul_table = []
                
        #error check
        if type(m) != int or m <= 1:
            return 'Error(MOD.get_mul_table): invalid input'
            
        #for every position in the list, create a mod mult table
        for pos1 in range(m):
            inner_list = []
            for pos2 in range(m):
                #get the multiples mod
                mult_modded = (pos1 * pos2) % m
                inner_list.append(mult_modded)
                
            mul_table.append(inner_list)    
        
        return mul_table

    @staticmethod
    def is_prime(n):
        """
        ----------------------------------------------------
        Static Method
        Parameters:   n (int): an arbitrary integer
        Return:       True/False
        Description:  Check if the given input is a prime number
                      Search Online for an efficient implementation
        ---------------------------------------------------
        """
        isprime = True
        
        #first we check if the number is greater than 1, as 1 is not prime
        if n > 1:
            
            #now, iterate through the inner digits of n, to check validity of prime
            inner_digits = int(n/2) + 1
            for i in range(2, inner_digits):
                
                #if at anytime, the mod of n is equal to 0 (meaning it was divisible by another number)
                #then we know it is not prime, therefore break and end
                if n % i == 0:
                    isprime = False
                    break
                
        else:
            
            isprime = False
                                                  
        return isprime


    @staticmethod
    def gcd(a,b):
        """
        ----------------------------------------------------
        Static Method
        Parameters:   a (int): an arbitrary integer
                      b (int): an arbitrary integer
        Return:       result (int): the GCD of a and b
        Description:  Computes and returns the greatest common divider using
                      the standard Eculidean Algorithm.
                      The implementation can be iterative or recursive
        Errors:       if a or b is non integer or equal to 0, return:
                        'Error(MOD.gcd): invalid input'
        ---------------------------------------------------
        """
        #error check
        if type(a) != int or type(b) != int or a == 0 or b == 0:
            return 'Error(MOD.gcd): invalid input'
                
        #using the euclidean algorthim: 
        #method of factorizing both nums and multiplying their common factors
        #to find the gcd of the pair. We can do this with a type of recursive like iteration
        while b != 0: 
            a, b = b, a % b
        
        #the final number left is the greatest common divisor, abs to get rid of hanging negative sign 
        gcd = abs(a)
        
        return gcd


    @staticmethod
    def is_relatively_prime(a,b):
        """
        ----------------------------------------------------
        Static Method
        Parameters:   a (int): an arbitrary integer
                      b (int): an arbitrary integer
        Return:       True/False
        Description:  Check if <a> and <b> are relatively prime
                          i.e., gcd(a,b) equals 1
        Errors:       if a or b are non positive integers, return:
                        'Error(Mod.is_relatively_prime): invalid input'
        ---------------------------------------------------
        """
        #error check
        if type(a) != int or type(b) != int or a < 0 or b < 0:
            return 'Error(MOD.is_relatively_prime): invalid input'
            
        coprime = False
        
        #if the gcd equals 1 then it is co-prime
        if MOD.gcd(a, b) == 1:
            coprime = True
        
        return coprime

    def has_mul_inv(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       True/False
        Description:  Check if current value has a multiplicative inverse mod m
        ---------------------------------------------------
        """
        #the mult. inverse of modulo m exists iff a and m are coprime :QED:
        is_coprime = MOD.is_relatively_prime(self.get_value(), self.get_mod())
        return is_coprime


    @staticmethod
    def EEA(a,b):
        """
        ----------------------------------------------------
        Static Method
        Parameters:   a (int): an arbitrary integer
                      b (int): an arbitrary integer
        Return:       result (list): [gcd(a,b), s, t]
        Description:  Uses Extended Euclidean Algorithm to find:
                        gcd(a,b) and <s> and <t> such that:
                        as + bt = gcd(a,b), i.e., Bezout's identity
        Errors:       if a or b are 0 or non-integers
                        'Error(MOD.EEA): invalid input'
        ---------------------------------------------------
        """
        #error catch
        if type(a) != int or type(b) != int or a == 0 or b == 0:
            return 'Error(MOD.EEA): invalid input'
        
        result = []
        
        #initialize variables
        #for negative numbers, use absolute value, in our case we will do this anyways
        a = abs(a)
        b = abs(b)
        
        #using these as temp swap values for each iteration
        s_swap1 = 0
        s_swap2 = 1
        t_swap1 = 1
        t_swap2 = 0
        
        #now we need to find the values of s and t in the equation: as + bt = gcd(a, b) => r=a-qb  && a = qb+r
        #*like in the example in the note
        #while b is greater than 0, run the algorithm until b hits 0
        while b != 0:
            
            #perform calculations using the formulas
            q = a // b 
            
            t = t_swap2 - q * t_swap1
            s = s_swap2 - q * s_swap1
            r = a - b * q

            #swap values for the next iteration   
            a = b
            b = r
            s_swap2 = s_swap1
            t_swap2 = t_swap1
            s_swap1 = s
            t_swap1 = t
        
        
        #get the remainders, ie. bezout identities:
        gcd = a
        s = s_swap2
        t = t_swap2
        
        result.append(gcd)
        result.append(s)
        result.append(t)

        return result
    
    
    def get_mul_inv(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       mul_inv (int or 'NA')
        Description:  Computes and returns the multiplicative inverse of 
                        current value mod m
                      if it does not exist returns 'NA'
        ---------------------------------------------------
        """
        #if it has a multiplicative inverse then: 
        if self.has_mul_inv():
            mult_inverse = pow(self.get_value(), -1, self.get_mod()) #equilvalent to using EEA for finding it
        else:
            return 'NA'
        
        return mult_inverse

    @staticmethod
    def get_mul_inv_table(m):
        """
        ----------------------------------------------------
        Static Method
        Parameters:   m (int): an arbitrary mod
        Return:       mul_inv_table (2d list)
        Description:  Construct and return multiplicative inverse table mod m
                        Top row are numbers 0 --> mod - 1
                        Bottom row is multplicative inverses
                      Example: Mod.get_mul_inv_table(5) --> 
                          [[0,1,2,3,4],['NA',1,3,2,4]]
        Errors:       if m is not an integer >= 2:
                        return 'Error(MOD.get_mul_inv_table): invalid input'
        ---------------------------------------------------
        """        
        #error check
        if type(m) != int or m <= 1:
            return 'Error(MOD.get_mul_inv_table): invalid input'
            
        top_row_num = [i for i in range(m)]
        bot_row_inverse = [i for i in range(m)]
        
        #get both the current number for top row and its mult. inverse for the opposite list
        for curr_digit in range(m):
            top_row_num[curr_digit] = curr_digit
            
            modobj = MOD(curr_digit, m)
            bot_row_inverse[curr_digit] = modobj.get_mul_inv()
        
        mul_inv_table = [top_row_num, bot_row_inverse]
        
        return mul_inv_table
        
    
    
class Decimation:
    """
    ----------------------------------------------------
    Cipher name: Decimation Cipher
    Key:         (k, start, end)
    Type:        Substitution Cipher
    Description: y = kx mod m
                 x = k(-1)y mod m
                 base = BASE[start:end]
                 m = len(base)
                 Applies only to characters defined in the base
    ----------------------------------------------------
    """
    BASE = utilities.get_base('lower') + ' ' + utilities.get_base('nonalpha') + utilities.get_base('upper')
    DEFAULT_KEY = (3,0,26)

    def __init__(self, key=DEFAULT_KEY):
        """
        ----------------------------------------------------
        Parameters:   _key (tuple(int,int,int)): (k,start,end)
        Description:  Decimation cipher constructor
                      sets _key
        ---------------------------------------------------
        """
        self._key = self.DEFAULT_KEY
        if key != self.DEFAULT_KEY:
            self.set_key(key)
            
        self._base = self.BASE
    
    
    def get_key(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       key (int,str)
        Description:  Returns a copy of the Decimation key
        ---------------------------------------------------
        """
        return self._key


    def get_base(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       base (str)
        Description:  Returns a copy of the decimation base
                        which is a subset of BASE
        ---------------------------------------------------
        """
        _, start, end = self.get_key()
        return self.BASE[start:end]
    
    def set_key(self,key):
        """
        ----------------------------------------------------
        Parameters:   key (tuple): tuple(int,int,int)
        Return:       success: True/False
        Description:  Sets Decimation cipher key to given key
                      and k is stored as a residue value
                      if invalid key --> set to default key
        ---------------------------------------------------
        """ 
        success = False
        
        if self.valid_key(key):
            success = True
            
            #k is stored as the residue value of m
            mod = key[2] - key[1]
            k = key[0] % mod
            
            
            new_key = k, key[1], key[2]
            self._key = new_key
            
        else:
            self._key = self.DEFAULT_KEY
        
        return success
    
    def __str__(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       output (str)
        Description:  Constructs and returns a string representation of 
                      Decimation object. Used for testing
                      output format:
                      Decimation Cipher:
                      y = <k>x mod <m>
                      x = <k-1>y mod <m>
        ---------------------------------------------------
        """ 
        #modobj is used to get the mult. inverse for k in <k-1> => <k-1> = mult. inverse
        modobj = MOD(self.get_key()[0], self.get_key()[2] - self.get_key()[1])
        output = 'Decimation Cipher:\ny = ' + str(self.get_key()[0]) + 'x mod ' + str(len(self.get_base())) + '\nx = ' + str(modobj.get_mul_inv()) + 'y mod ' + str(len(self.get_base()))
        return output
    
    @staticmethod
    def valid_key(key):
        """
        ----------------------------------------------------
        Static Method
        Parameters:   key (?):
        Returns:      True/False
        Description:  Checks if given key is a valid Decimation key
                      A valid key should be a tuple consisting of three integers
                      <k> should have a multiplicative inverse in mod m
                      start < end, and both are positive valid indexes for BASE
                      The base should contain at least two chars
        ---------------------------------------------------
        """
        success = False
        
        #I added a condition to valid key, where k != 1 as no encipherment happens at 1,
        if type(key) == tuple and len(key) == 3 and type(key[0]) == int and type(key[1]) == int and type(key[2]) == int and key[0] != 1:
            
            #k should have a multiplicative inverse in m
            #decimationobj = Decimation(key) ->bad
            start = key[1]
            end = key[2]
            
            #the mod is the len of base
            BASE = utilities.get_base('lower') + ' ' + utilities.get_base('nonalpha') + utilities.get_base('upper')            
            m = key[2] - key[1]
            
            modobj = MOD(key[0], m)

            #print(m)
            #has mult. inverse, start < end, start >= 0, end < len(base), base should contain at least two char (m)
            if modobj.has_mul_inv() and start < end and start >=0 and end <= len(BASE) and m >= 2:
                success = True
        
        return success
    
    
    def encrypt(self, plaintext):
        """
        ----------------------------------------------------
        Parameters:   plaintext (str)
        Return:       ciphertext (str)
        Description:  Encryption using Decimation Cipher
        Asserts:      plaintext is a string
        ---------------------------------------------------
        """
        assert type(plaintext) is str, 'invalid input'

        #The encryption and decryption apply only to characters in the base
        #The case of the letters should be preserved.
           
        #using the equation: y = kx mod m  find the index of the char in the list from 0-n
        #where n is the number x in the equation. The result is the index of the new char 
        #base = BASE[start:end]
        #m = len(base)
        
        ciphertext = ''
        #print(self.get_base())
        
        #get attributes
        key = self.get_key()
        k, start, end = key[0], key[1], key[2]
        mod = end - start
        base = self.get_base()
        
        for char in plaintext:
            
            if char in base:
                #print('\n')
                #print(char)
                #plain_index_getter
                plain_index = 0
                for base_char in base:
                    if base_char == char:
                        break;
                    plain_index += 1
                        
                #print(plain_index)
                #y = kx mod m
                cipher_index = ( k * plain_index ) % mod                
                
                ciphertext += base[cipher_index]
            
            else:
                ciphertext += char    
        
        return ciphertext
    
    
    def decrypt(self,ciphertext):
        """
        ----------------------------------------------------
        Parameters:   ciphertext (str)
        Return:       plaintext (str)
        Description:  Decryption using Decimation Cipher
        Asserts:      ciphertext is a string
        ---------------------------------------------------
        """
        assert type(ciphertext) is str, 'invalid input'

        #The encryption and decryption apply only to characters in the base
        #The case of the letters should be preserved.
           
        #using the equation: x = k(-1)y mod m find the index of the char in the list from 0-n
        #where n is the number y in the equation. The result is the index of the new char 
        #base = BASE[start:end]
        #m = len(base)
                
        plaintext = ''
        #print('\n')
        #print(self.get_base())
        
        #get attributes
        key = self.get_key()
        k, start, end = key[0], key[1], key[2]
        mod = end - start
        base = self.get_base()
        
        for char in ciphertext:
            
            if char in base:
                #print('\n')
                #print(char)
                #ciphertext_index_getter
                cipher_index = 0
                for base_char in base:
                    if base_char == char:
                        break;
                    cipher_index += 1
                        
                #print(plain_index)
                #x = k(-1)y mod m
                modobj = MOD(k, mod)
                plain_index = ( modobj.get_mul_inv() * cipher_index ) % mod                
                
                plaintext += base[plain_index]
            
            else:
                plaintext += char    
        
        return plaintext
    
    
    @staticmethod
    def cryptanalyze_keys(args=[-1,-1,-1]):
        """
        ----------------------------------------------------
        Parameters:   args (list):
                          k (int): if unknown = -1
                          start (int): if unknown = -1
                          end (int): if unknown = -1
        Return:       keys (list)
        Description:  Returns all valid keys
                      Excludes keys which result in no encipherment
                      Assume that at least one arg is known
        ---------------------------------------------------
        """
        #get args
        k, start, end = args
        
        #get all valid keys
        #assume at least one earg is known
        valid_keys = []
        base = Decimation.BASE
        
        #base case: we have everything
        if k != -1 and start != -1 and end != -1:
            
            key = (k, start, end)
            if Decimation.valid_key(key):
                valid_keys.append(key)
        
        #k is not known, start is known, end is known
        elif k == -1 and start != -1 and end != -1:
            
            #conditions: k < len(base) for finding k
            base = base[start:end]

            #k will not start at 1 as gcd no worky at 1 by default
            #remove all even numbers that k could be
            #remove all uneven numbers that gcd(k, mod) != 1
            
            #print(len(base))
            for curr_k in range(2, len(base)):
                #print(curr_k)
                key = (curr_k, start, end)
                if curr_k % 2 != 0 and Decimation.valid_key(key):
                    valid_keys.append(key)
                    
            
        #k is known, start is not known, end is known
        elif k != -1 and start == -1 and end != -1:
            
            #go through each possible start from 0-end and test against validkey
            for curr_start in range(end):
                key = (k, curr_start, end)
                if Decimation.valid_key(key):
                    valid_keys.append(key)
           
            
        #k is known, start is known, end is not known
        elif k != -1 and start != -1 and end == -1:
            
            #go through each possible start from 0-end and test against validkey
            for curr_end in range(len(base) + 1):
                key = (k, start, curr_end)
                if Decimation.valid_key(key):
                    valid_keys.append(key)


        #k is not known, start is not known, end is known
        elif k == -1 and start == -1 and end != -1:
            
            #key = (8, 2, 9)
            #print(str(Decimation.valid_key(key)))
            #print(MOD.gcd(8, 7))
        
            #we need to try every possible start from 0-end
            base = base[:end] 
            for curr_start in range(end):
                
                #we need to try every k from 2-end, ensuring that it is less than current len(base) (end-curr_start) 
                for curr_k in range(2, end):
                    key = (curr_k, curr_start, end)
                    if curr_k < (end-curr_start) and Decimation.valid_key(key):
                        valid_keys.append(key)
                    
            
        #k is not known, start is known, end is not known
        elif k == -1 and start != -1 and end == -1:
            
            #we need to try every possible end from start-len(base)
            for curr_end in range(start, len(base)+1):
                #we need to try every k from 2-curr-end, ensuring that it is less than current len(base) (curr_end-start) 
                for curr_k in range(2, curr_end):
                    key = (curr_k, start, curr_end)
                    if curr_k < (curr_end-start) and Decimation.valid_key(key):
                        valid_keys.append(key)
            
            
        #k is known, start is not known, end is not known
        elif k != -1 and start == -1 and end == -1:
            
            #make sure k != -1 by default, either this should have been done in valid_key
            #or here, im going to put it here for now, shouldnt make a difference overall
            
            #the only possible values for start, are any 0-n value in the difference
            #of the len(base) - k
            possible_starts = len(base) - k
            for curr_start in range(possible_starts):
                #end > k 
                #try every end in our range
                for curr_end in range(curr_start, len(base) + 1):
                    key = (k, curr_start, curr_end)
                    if k < (curr_end-curr_start) and Decimation.valid_key(key):
                        valid_keys.append(key)

        
        return valid_keys
       
    @staticmethod
    def cryptanalyze(ciphertext,args=[-1,-1,-1,None,0.8]):
        """
        ----------------------------------------------------
        Parameters:   ciphertext (str)
                      args (list):
                          dict_file (str): dictionary file name
                          threshold (float): to be used in is_plaintext
        Return:       key,plaintext
        Description:  Performs cryptanalysis of decimation cipher
                      Assume that the base is some subset of utilitiles.get_base('all')
                      starting at base[0] with an arbitrary length
        ---------------------------------------------------
        """
        final_key = ('','','')
        plaintext = ''
        
        #grab args
        k, start, end, dict_file, threshold = args
          
        possible_keys = Decimation.cryptanalyze_keys([k,start,end])
        
        print(possible_keys) #output has this

        dict_list = utilities.load_dictionary(dict_file)
        #print(dict_list)
        
        #try every key that we got from the list of valid keys 
        for key in possible_keys:
            #k, start, end = key
            decimationObj = Decimation(key)
            curr_plaintext = decimationObj.decrypt(ciphertext)
            #print(curr_plaintext)
            
            #if its close to english we have the key
            keyfound = utilities.is_plaintext(curr_plaintext, dict_list, threshold) 
            if keyfound:
                plaintext = curr_plaintext
                final_key = key
                break
        
        return final_key, plaintext
   
    
class Affine:
    """
    ----------------------------------------------------
    Cipher name: Affine Cipher
    Key:         (a,b,start,end)
    Type:        Substitution Cipher
    Description: y = ax + b mod m
                 x = a_inv * (y - b) mod m
                 base = BASE[start:end]
                 m = len(base)
                 Applies only to characters defined in the base
    ----------------------------------------------------
    """
    BASE = utilities.get_base('lower') + ' ' + utilities.get_base('nonalpha') + utilities.get_base('upper')
    DEFAULT_KEY = (17,9,0,26)

    def __init__(self,key=DEFAULT_KEY):
        """
        ----------------------------------------------------
        Parameters:   _key (tuple(int,int,int,int)): (a,b,start,end)
        Description:  Affine Cipher constructor
                      sets _key
        ---------------------------------------------------
        """
        self._key = self.DEFAULT_KEY
        if key != self.DEFAULT_KEY:
            self.set_key(key)
            
        self._base = self.BASE
    
    def get_key(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       key (int,str)
        Description:  Returns a copy of the Affine key
        ---------------------------------------------------
        """
        return self._key

    def get_base(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       base (str)
        Description:  Returns a copy of the Affine base
                        which is a subset of BASE
        ---------------------------------------------------
        """
        _, _, start, end = self.get_key()
        return self.BASE[start:end]
        
    def set_key(self,key):
        """
        ----------------------------------------------------
        Parameters:   key (tuple): tuple(int,int,int,int)
        Return:       success: True/False
        Description:  Sets Affine cipher key to given key
                      If necessary sets a and b to residue values
                      if invalid key --> set to default key
        ---------------------------------------------------
        """ 
        success = False
        
        if self.valid_key(key):
            success = True
            
            #set a and b to residue values if neccessary
            mod = key[3] - key[2]
            #print("mod: " + str(mod))
            
            a = key[0]
            b = key[1]
            
            #if negative, we need to do something a little different, I think
            #we need to subtract it from the end of the largest base amount???
            if a < 0:
                a = key[3] + a
            else:
                a = a % mod
                
                
            if b < 0:
                b = key[3] + b
            else:
                b = b % mod
            
            new_key = a, b, key[2], key[3]
            self._key = new_key
        else:
            self._key = self.DEFAULT_KEY
            
            
        return success
    
    def __str__(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       output (str)
        Description:  Constructs and returns a string representation of 
                      Affine object. Used for testing
                      output format:
                      Affine Cipher:
                      y = <a>x + <b> mod <m>
                      x = inv(<a>)*(y - <b>) mod <m>
        ---------------------------------------------------
        """
        modobj = MOD(self.get_key()[0], len(self.get_base()))
        output = 'Affine Cipher:\ny = ' + str(self.get_key()[0]) + 'x + ' + str(self.get_key()[1]) + ' mod ' + str(len(self.get_base())) + '\nx = ' + str(MOD.get_mul_inv(modobj)) + '(y - ' + str(self.get_key()[1]) + ') mod ' + str(self.get_key()[3]-self.get_key()[2])
        return output
    
    @staticmethod
    def valid_key(key):
        """
        ----------------------------------------------------
        Static Method
        Parameters:   key (?):
        Returns:      True/False
        Description:  Checks if given key is a valid Affine key
                      A valid key is a tuple of 4 integers (a,b,start,end)
                      <a> should have a multiplicative inverse in mod m
                      start < end, and both are positive valid indexes for BASE
                      The base should contain at least two chars
        ---------------------------------------------------
        """
        success = False
        
        if type(key) == tuple and len(key) == 4 and type(key[0]) == int and type(key[1]) == int and type(key[2]) == int and type(key[3]):
            
            #k should have a multiplicative inverse in m
            #decimationobj = Decimation(key) ->bad
            start = key[2]
            end = key[3]
            
            #the mod is the len of base
            BASE = utilities.get_base('lower') + ' ' + utilities.get_base('nonalpha') + utilities.get_base('upper')            
            m = len(BASE[start:end])
            
            modobj = MOD(key[0], m)

            #print(m)
            #has mult. inverse, start < end, start >= 0, end < len(base), base should contain at least two char (m)
            if modobj.has_mul_inv() and start < end and start >=0 and end <= len(BASE) and m >= 2:
                
                #if a = 1 and b = 0 then no encipherment happens, I added this condition
                if key[0] != 1 or key[1] != 0:
                    success = True
        
        return success
    
    
    def encrypt(self,plaintext):
        """
        ----------------------------------------------------
        Parameters:   plaintext (str)
        Return:       ciphertext (str)
        Description:  Encryption using Decimation Cipher
        Asserts:      plaintext is a string
        ---------------------------------------------------
        """
        assert type(plaintext) is str, 'invalid input'
        
        #The encryption and decryption apply only to characters in the base
        #The case of the letters should be preserved.
           
        #using the equation: y = ax + b mod m  find the index of the char in the list from 0-n
        #where n is the number a in the equation and b is the shift number
        #The result is the index of the new char 
        #base = BASE[start:end]
        
        ciphertext = ''
                
        #key = (a,b,start,end)
        #get attributes
        key = self.get_key()
        a, b, start, end = key[0], key[1], key[2], key[3]
        mod = end - start
        base = self.get_base()
        
        for char in plaintext:
            
            if char in base:
                
                #plain_index_getter
                plain_index = 0
                for base_char in base:
                    if base_char == char:
                        break
                    plain_index += 1
                
                #y = ax + b mod m
                cipher_index = ((a*plain_index) + b) % mod
                
                ciphertext += base[cipher_index]
                
            else:
                ciphertext += char
        
        
        return ciphertext
    
    
    def decrypt(self,ciphertext):
        """
        ----------------------------------------------------
        Parameters:   ciphertext (str)
        Return:       plaintext (str)
        Description:  Decryption using Affine Cipher
        Asserts:      ciphertext is a string
        ---------------------------------------------------
        """        
        assert type(ciphertext) is str, 'invalid input'
        
        #The encryption and decryption apply only to characters in the base
        #The case of the letters should be preserved.
           
        #using the equation: x = a_inv * (y - b) mod m  find the index of the char in the list from 0-n
        #where n is the number a in the equation and b is the shift number
        #The result is the index of the new char 
        #base = BASE[start:end]
        
        plaintext = ''
       
        #get attributes
        key = self.get_key()
        a, b, start, end = key[0], key[1], key[2], key[3]
        mod = end - start
        base = self.get_base()
        
        #print(base)
        
        for char in ciphertext:
            
            if char in base:
                #print('\n')
                #print(char)
                #ciphertext_index_getter
                cipher_index = 0
                for base_char in base:
                    if base_char == char:
                        break;
                    cipher_index += 1
                        
                #print(plain_index)
                #x = a_inv * (y - b) mod m
                modobj = MOD(a, mod)
                plain_index = (modobj.get_mul_inv() * (cipher_index - b)) % mod            
                
                plaintext += base[plain_index]
            
            else:
                plaintext += char    
        
        
        
        return plaintext
    
    
    @staticmethod
    def cryptanalyze_keys(args=[-1,-1,-1,-1]):
        """
        ----------------------------------------------------
        Parameters:   args (list):
                          a (int): if unknown = -1
                          b (int): if unknown = -1
                          start (int): if unknown = -1
                          end (int): if unknown = -1
        Return:       keys (list)
        Description:  Returns all valid keys
                      Excludes keys which result in no encipherment
                      Assume that no more than one argument is unknown
        ---------------------------------------------------
        """
        
        #get args
        a, b, start, end = args
        
        #get all valid keys
        #assume at least only 1 arg is not known
        valid_keys = []
        base = Affine.BASE
        
        #base case: all arguments are known:
        if a != -1 and b != -1 and start != -1 and end != -1:
            key = (a, b, start, end)
            if Affine.valid_key(key):
                valid_keys.append(key)
            
        #a is known, b is not known, start is known, end is known
        elif a != -1 and b == -1 and start != -1 and end != -1:
            
            start_val = 0
            if a == 1: #if a==1 then b cannot be 0 as a=1 and b=0 is would cause no encipherment
                start_val = 1
            
            base = base[start:end]
            
            #every key up to the max of b
            for curr_b in range(start_val, len(base) + 1): #+1 because shift can be a value from 0-len(base) inclusive
                key = a, curr_b, start, end
                if Affine.valid_key(key):
                    valid_keys.append(key)
            
            #print(valid_keys)
            
            
        #a is not known, b is known, start is known, end is known
        elif a == -1 and b != -1 and start != -1 and end != -1:
            
            start_val = 1
            if b == 0: #if there is no shift given, then having a = 1 would cause no encipherment
                start_val = 2
            
            #go through all possible index values inside the base[start:end]
            base = base[start:end]
            for curr_a in range(start_val, len(base)):
                key = (curr_a, b, start, end)
                if Affine.valid_key(key):
                    valid_keys.append(key)
        
        
        #a is known, b is known, start is not known, end is known
        elif a != -1 and b != -1 and start == -1 and end != -1:
            
            #go through each possible start from 0-end and test against validkey
            for curr_start in range(end):
                key = (a, b, curr_start, end)
                if Affine.valid_key(key):
                    valid_keys.append(key)
            
        #a is known, b is known, start is known, end is not known
        elif a != -1 and b != -1 and start != -1 and end == -1:
            
            #go through each possible start from 0-end and test against validkey
            for curr_end in range(len(base) + 1):
                key = (a, b, start, curr_end)
                if Affine.valid_key(key):
                    valid_keys.append(key)
            
            
        return valid_keys
           
            
    @staticmethod
    def cryptanalyze(ciphertext,args=[-1,-1,-1,-1,None,0.8]):
        """
        ----------------------------------------------------
        Parameters:   ciphertext (str)
                      args (list):
                          a (int): if unknown = -1
                          b (int): if unknown = -1
                          start (int): if unknown = -1
                          end (int): if unknown = -1
                          dict_file (str): dictionary file name
                          threshold (float): to be used in is_plaintext
        Return:       key,plaintext
        Description:  Performs cryptanalysis of affine cipher
                      Attempts keys from cryptanalyze_keys
                      returns two empty strings if it fails
        ---------------------------------------------------
        """
        final_key = ('','','')
        plaintext = ''
        
        #grab args
        a, b, start, end, dict_file, threshold = args
          
        possible_keys = Affine.cryptanalyze_keys([a,b,start,end])
        
        print(possible_keys) #output has this
        
        dict_list = utilities.load_dictionary(dict_file)
        #print(dict_list)
        
        #try every key that we got from the list of valid keys 
        for key in possible_keys:
            
            #a, b, start, end = key
            affineObj = Affine(key)
            curr_plaintext = affineObj.decrypt(ciphertext)
            #print(curr_plaintext)
            
            #see if its close to english, we found the key
            keyfound = utilities.is_plaintext(curr_plaintext, dict_list, threshold) 
            if keyfound:
                plaintext = curr_plaintext
                final_key = key
                break
        
        return final_key, plaintext
    
    
    