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
        while b > 0: 
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
            #print("bruh: " + str(MOD.gcd(a,b)))
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