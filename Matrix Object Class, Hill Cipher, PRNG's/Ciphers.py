"""
-------------------------------------
File: Ciphers.py
File description
Matrix Methods Class, Hill Cipher, PRNG's implementations
-------------------------------------
Author:  Chandler Mayberry
Version  2021-11-18
-------------------------------------
"""

import utilities
from mod import MOD

class Matrix:
    def __init__(self,r=0,c=0,fill=0):
        """
        ----------------------------------------------------
        Parameters:   _matrix (list): default = []
        Description:  Matrix constructor
                      sets _matirx using Matrix.create(r,c,fill)
        ---------------------------------------------------
        """
        self._matrix = []
        
        if r != 0 or c != 0:
            
            #create the matrix
            matrix = []
            for _ in range(r):
                row = []
            
                for _ in range(c):
                    row.append(fill)
                
                matrix.append(row)  
            
            self._matrix = matrix
        
        
    def get_matrix(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       matrix (list)
        Description:  returns a copy of the current matrix as a list
        ---------------------------------------------------
        """
        return self._matrix
    
    
    def get_size(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       r (int): number of rows
                      c (int): number of columns
        Description:  returns the size of the current matrix, i.e.,
                        #rows and #columns
        ---------------------------------------------------
        """
        if not self.get_matrix(): #is empty list
            return 0, 0 #row, col
        else:
            #just a check if there is just one element
            if type(self.get_matrix()[0]) is list:
                return len(self.get_matrix()), len(self.get_matrix()[0])
            else:
                return 0, len(self.get_matrix())


    def get_row(self, i):
        """
        ----------------------------------------------------
        Parameters:   i (int): row number
        Return:       row (list): the ith row
        Description:  returns a copy of the ith row in the matrix
                      Supports positive values: 0 to r-1
                               negative values: -1 to -r
        Errors:       if invalid i, print error message and return ''
        ---------------------------------------------------
        """
        
        if self.get_size()[0] == 0 or self.get_size()[0] == 0:
            print("Error(Matrix.get_row): index out of range")
            return ''
        elif (i < self.get_size()[0] and i >= 0) or (i >= -1 and i >= -self.get_size()[0]):
            row = self.get_matrix()[i]
        else:
            print("Error(Matrix.get_row): index out of range")
            return ''
        
        return row
    
    def get_column(self, j):
        """
        ----------------------------------------------------
        Parameters:   j (int): column number
        Return:       column (list): the ith column
        Description:  returns a copy of the ith column in the matrix
                      Supports positive values: 0 to c-1
                               negative values: -1 to -c
        Errors:       if invalid i, print error message and return ''
        ---------------------------------------------------
        """
        if self.get_size()[0] == 0 or self.get_size()[0] == 0:
            print("Error(Matrix.get_column): index out of range")
            return ''
        elif (j < self.get_size()[1] and j >= 0) or (j >= -1 and j >= -self.get_size()[1]):
            
            column = []
            for row in self.get_matrix():
                column.append([row[j]])
            
        else:
            print("Error(Matrix.get_column): index out of range")
            return ''
        
        return column
        
        
    def get_item(self,i,j):
        """
        ----------------------------------------------------
        Parameters:   i (int): row number
                      j (int): column number
        Return:       column (list): the ith column
        Description:  returns a copy of item [i][j] in the matrix
                      Supports positive and negative values for i and j
        Errors:       if invalid i, print error message and return ''
        ---------------------------------------------------
        """
        column = []
        x, y = self.get_size()
        
        if i < x and j < y:
            column = self.get_matrix()[i][j]
        else:
            print('Error(Matrix.get_item): index out of range')
            return ''
        
        return column
        
        
    
    def is_empty(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       True/False
        Description:  checks if the current matrix is empty
        ----------------------------------------------------
        """
        if not self.get_matrix():
            empty = True
        else:
            empty = False
        return empty
    
    
    def is_vector(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       True/False
        Description:  checks if the current matrix is a vector
        ----------------------------------------------------
        """
        #a matrix with either one row or column is a vector
        is_vector = False
        
        x, y = self.get_size();
        
        if x <= 1 or y <= 1:
            is_vector = True
        
        return is_vector
    
    
    def is_square(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       True/False
        Description:  Check if current matrix is square
                        #rows equal to #columns
        ---------------------------------------------------
        """
        #check to see if the matrix is square nxn
        x, y = self.get_size();
        square = False
        
        if x == y:
            square = True
        
        return square

    def is_identity(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       True/False
        Description:  Check if current matrix is an identity matrix
                      Diagonal elements [from top left to bottom right] = 1
                      All other elements = 0
        ---------------------------------------------------
        """
        #check to see if the matrix input is an identity matrix
        rownum, colnum = self.get_size();
        
        is_identity = True
    
        if rownum != 0 and colnum != 0:
            
            for i in range(rownum):
                for j in range(colnum):
                    
                    #check to see if all values outside of the diagonal are 0
                    if (i!=j and self.get_matrix()[i][j] != 0):
                        is_identity = False
                        break
                    
                    #check to see if all values inside of the diagonal are 1
                    elif (i==j and self.get_matrix()[i][j] != 1):
                        is_identity = False
                        break
        else:
            is_identity = False
            
        return is_identity


    @staticmethod
    def to_matrix(list1):
        """
        ----------------------------------------------------
        Parameters:   list1: a list representing a matrix
        Return:       m: a Matrix objectc
        Description:  Creates a matrix object that has same items as list1
                      if list1 is not a valid matrix: 
                          return empty Matrix object
        ---------------------------------------------------
        """
        
        if Matrix.valid_matrix(list1):
            
            nrow = len(list1)
            ncol = 0
            
            #check to make sure that the first element in the list is a list, or if the list1 is a vector
            if nrow > 0 and type(list1[0]) is list:
                ncol = len(list1[0])
            
            m = Matrix(nrow, ncol, 0)
            
            for row in range(nrow):
                
                #if its a vector list then we dont have to worry about the col as there isnt any
                if type(list1[row]) is not list and type(list1[row]) is int:
                    m._matrix[row] = list1[row]
                
                #else its a 2D list, make list the matrix object
                elif type(list1[row]) is list:
                    
                    len_column = len(list1[row])
                    
                    #if the len_col does not equal the standard size for all columns then its
                    #not a valid matrix
                    if len_column != ncol:
                        m._matrix = []
                        return m      
                    
                    #else continue to fill the m matrix object 
                    else:
                        for col in range(len_column):
                            m._matrix[row][col] = list1[row][col]
                        
            
        else:
            m = Matrix()
        
        return m
        
    def __str__(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       output (str)
        Description:  Constructs and returns a string representation of 
                      a Matrix object
                      output format:
                      if empty or vecotr: print _matrix
                      Otherwise, print each row in a separate line
        ---------------------------------------------------
        """
        matrix = self.get_matrix()
        
        #special case if the matrix is empty
        if matrix == []:
            output = '[]'
        
        else:
            output = ''
            
            #check if its a vector or a matrix
            if type(matrix[0]) is int:
                output += str(matrix)
            
            else:
                for row in matrix:
                    output += str(row) + '\n'
                    
                output = output.rstrip('\n')
        
        return output
    
    def to_list(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       matrix (list)
        Description:  Converts a Matrix object to a list
                      Same as get_matrix()
        ---------------------------------------------------
        """
        return self.get_matrix()
    
    
    def set_matrix(self,A):
        """
        ----------------------------------------------------
        Parameters:   A (list or Matrix)
        Return:      True/False
        Description:  sets _matrix data member by the given A
                      parameter A can be a list or a Matrix
                      Before setting, ensure it is a valid matrix
                      if invalid input --> print error message and return False
        ---------------------------------------------------
        """
        #basically set key
        set_matrix = False
        
        if self.valid_matrix(A) or self.valid_vector(A):
            self._matrix = A
            set_matrix = True
        else:
            print('Error(Matrix.set_matrix): invalid input')
        
        return set_matrix
    
    
    def set_item(self,i,j,value):
        """
        ----------------------------------------------------
        Parameters:   i (int): row number
                      j (int): column number
                      value (int)
        Return:      True/False
        Description:  sets _matrix[i][j] to given value
                      supports positive and negative values of i and j
                      if invalid input, print error msg and return False
        ---------------------------------------------------
        """
        set_item = False
        
        nrow, ncol = self.get_size()
        
        #abs to account for negative sizes
        if abs(i) < nrow and abs(j) <= ncol:
            new_matrix = self.get_matrix()
            
            new_matrix[i][j] = value
            
            #if the new matrix with the new value set properly, then set_item was successful
            set_item = self.set_matrix(new_matrix)
        
        else:
            print('Error(Matrix.set_item): index out of range')
            
        return set_item
    
    
    @staticmethod
    def valid_vector(A):
        """
        ----------------------------------------------------
        Parameters:   A (any input)
        Return:       True/False
        Description:  checks if the given input is a valid vector
                      A valid vector is a list in which all elements are integers
                      An empty list is a valid vector
                      Note: a matrix with a vertical vector (one item in each row)
                          is NOT a valid vector
        ----------------------------------------------------
        """
        isvalid = True
        
        if type(A) is list:            
            #as long as every element in the list is an int, then it will be a vector
            #if the element is a list then its not a vector            
            for i in A:
                if type(i) is not int:
                    isvalid = False
                    break
        else:
            isvalid = False
        
        
        return isvalid


    @staticmethod
    def valid_matrix(A):
        """
        ----------------------------------------------------
        Parameters:   A (any input)
        Return:       True/False
        Description:  checks if the given input is a valid matrix
                      A valid matrix is any object of type Matrix, or 
                      a 2D list that fits matrix properties
                      A matrix is a list in which all elements are valid vectors of equal size
                      Any valid vector is also a valid matrix
        ----------------------------------------------------
        """        

        isvalid = True
        
        #A valid matrix is any object of type Matrix
        if type(A) is list or type(A) is Matrix:
            
            #if not empty and the first element is a list then check all elements
            if A and type(A) is list and type(A[0]) is list:
                
                rowlength = len(A[0])
                for row in A:
                    #check each row as vector, if its true then it satisfies matrix conditions
                    if not Matrix.valid_vector(row): 
                        isvalid = False 
                        break
                    
                    #make sure every row is the same size, as to not have one random row bigger or smaller
                    if len(row) != rowlength:
                        isvalid = False
                        break
            
            #if the first element is an integer, then check if its a valid vector (valid vector == valid matrix)
            else:
                isvalid = Matrix.valid_vector(A)
                
        else:
            isvalid = False
           
        return isvalid
    
    
    @staticmethod
    def create(r=0,c=0,fill=0):
        """
        ----------------------------------------------------
        Parameters:   r: #rows (int)
                      c: #columns (int)
                      fill (?)
        Return:       matrix (2D List)
        Description:  Create a matrix (2D list not Matrix) of size r x c
                          All elements initialized to fill
                      if r or c is <= 0, return empty list
                      if r is 1 returns a vector (1D list)
                      Otherwise, returns a 2D list
        ---------------------------------------------------
        """
        matrix = []
        
        #if r or c is less than 0 return empty list
        if r <= 0 or c <= 0:
            return []
        
        for _ in range(r):
            row = []
            
            for _ in range(c):
                row.append(fill)
            
            matrix.append(row)  
        
        return matrix
    
    
    @staticmethod
    def I(size):
        """
        ----------------------------------------------------
        Parameters:   size (int): #rows = #columns in square matrix
        Return:       I (2D list): identity matrix
        Description:  returns the identity matrix of size:
                        size x size
                      The output is a 2D list (not a matrix object)
                      1 --> [1]
                      2 --> [[1,0],[0,1]]
        Errors:       if size is 0 or negative, print error message and return []
        ---------------------------------------------------
        """
        #identity matrix
        i_matrix = []
        
        #if we get a size 0 or negative size then we cant do anything with that
        if size > 0:
            
            #initialize the matrix to size n and fill it with 0's
            i_matrix = [[0 for _ in range(size)] for _ in range(size)]
            
            #make the diagonal from left to right == 1
            for i in range(size):
                for j in range(size):
                    if i == j:
                        i_matrix[i][j] = 1
        
        else:
            print('Error(Matrix.get_I): invalid size')

        
        return i_matrix
    
            
    @staticmethod
    def scalar_mul(c,A):
        """
        ----------------------------------------------------
        Parameters:   c (int): scalar value
                      A (Matrix or list): an arbitrary matrix
        Return:       B (Matrix): result of c.A
        Description:  Performs scalar multiplication of c with A
                      A can be a Matrix object or a valid matrix list
                      The result is a Matrix object
        Errors:       if one of the inputs is invalid:
                        print error message and return empty Matrix object
        ---------------------------------------------------
        """
        
        if Matrix.valid_matrix(A) and len(A) != 0:
            
            #check if its a vector list or if its an actual 2D list:
            if type(A[0]) is not list and type(A[0]) is int: #vector list
                
                if Matrix.valid_vector(A):
                    for i in range(len(A)):
                        A[i] = A[i] * c
                else: 
                    print("Error(Matrix.scalar_mul): invalid input")
                    B = Matrix()
                                    
            
            elif type(A[0]) is list: #matrix list
                
                for i in range(len(A)):
                    for j in range(len(A[i])):
                        
                        #multiply the value at [row][col] location by the scalar
                        if type(A[i][j]) is int:
                            A[i][j] = A[i][j] * c
                            
                        else: #if not an int, then its an invalid input matrix
                            print("Error(Matrix.scalar_mul): invalid input")
                            B = Matrix()
                            break
            
            B = Matrix.to_matrix(A)
                
        else:
            print('Error(Matrix.scalar_mul): invalid input')
            B = Matrix()
        
        return B
    
    
    @staticmethod
    def mul(A,B):
        """
        ----------------------------------------------------
        Parameters:   A (Matrix): an arbitrary Matrix object
                      B (Matrix): an arbitrary Matrix object
        Return:       C (Matrix): result of A x B
        Description:  Performs cross multiplication of c with A
                    
                      The result is a Matrix object
        Errors:       if one of the inputs is invalid or A(#columns) != B(#rows)
                        print error message and return empty Matrix object
        ---------------------------------------------------
        """
        
        m1 = A.to_list()
        #print(len(m1))
        m2 = B.to_list()
        #print(len(m2))
                
        #if the two lists are only of one element, we can just multiply them together and be done
        if len(m1) == 1 and len(m2) == 1:
            C = [0]
            C[0] = m1[0] * m2[0]
            C = Matrix.to_matrix(C)
        
        #else if they are of any other size, we need to perform other operations
        elif Matrix.valid_matrix(m1) and Matrix.valid_matrix(m2) and len(m1) != 0 and len(m2) != 0:
            
            C = []
        
            #matrix times a matrix
            #if type(A[0]) is not list and type(A[0]) is int:                       
            if type(m1[0]) is list and type(m2[0]) is list:
                
                # (m x n) * (n x k) = (m x k)
                m, n1 = A.get_size() #len(m1), len(m1[0])
                n2, k = B.get_size() #len(m1), len(m1[0])           
                
                #we need to make sure that A #columns != B #rows (rule of matrix-mult.)
                if n1 != n2:
                    print('Error(Matrix.mul): size mismatch')
                    C = Matrix.to_matrix([])
                    return C
                
                #IMPLEMENTATION OF MATRIX TIMES A MATRIX
                C = [[0 for _ in range(k)] for _ in range(m)]
                
                #iterate through all the rows in m1
                for i in range(len(m1)):
                    #iterate through all the cols in m2
                    for j in range(len(m2[0])):
                        #iterate through all the rows in m2         
                        for k in range(len(m2)):
                            
                            C[i][j] += m1[i][k] * m2[k][j]
                
                
    
            #vector times a matrix
            elif type(m1[0]) is not list and type(m2[0]) is list:
                
                #print('vector times a matrix')
                # (m x n) * (n x k) = (m x k)
                #m, n1 = A.get_size() #len(m1), len(m1[0])
                ##n2, k = B.get_size() #len(m1), len(m1[0])  
                m = 1
                n1 = len(m1)
                n2 = len(m2)
                k = len(m2[0])  
                
                #we need to make sure that A #columns != B #rows (rule of matrix-mult.)
                if n1 != n2:
                    print('Error(Matrix.mul): size mismatch')
                    C = Matrix.to_matrix([])
                    return C
                
                #print("-------------------------")
                #IMPLEMENTATION OF VECTOR TIMES A MATRIX

                C = [0 for _ in range(k)]
                #print(C)
                #print('m = ' + str(m))
                #print('k = ' + str(k))
                #print('n1 = ' + str(n1))
                #print('n2 = ' + str(n2))

                #print("-------------------------")
                
            
                    
                #iterate through all the cols in m2
                for i in range(k):
                    
                    #iterate through all the rows in m2 
                    for j in range(n2):
                        C[i] += m1[j] * m2[j][i]
                        #print('-------')
                        #print(m1[k])
                        #print(m2[k][j])
                        #print('j = ' + str(j))
                        #print('k = ' + str(k))
                        #print(C[j])
                        #print('addition: ' + str(m1[k] * m2[k][j]))
                        #C.append(m1[k] * m2[k][j])
                
                #print(C)
                
            
            #matrix times a vector 
            elif type(m1[0]) is not list and type(m2[0]) is list:
                
                #:::::::::IF I RUN INTO AN ERROR HERE ITS BECAUSE MY LOGIC OF M1 = M2 IS WRONG::::::::::
                #:::::::::THE LOGIC OF VECTOR * MATRIX DOES NOT WORK FOR MATRIX * VECTOR TRANSPOSED:::::::::::
                
                #swap the lists
                temp = m1
                m1 = m2
                m2 = temp
                
                m = 1
                n1 = len(m1)
                n2 = len(m2)
                k = len(m2[0])  
                
                #we need to make sure that A #columns != B #rows (rule of matrix-mult.)
                if n1 != n2:
                    print('Error(Matrix.mul): size mismatch')
                    C = Matrix.to_matrix([])
                    return C
                
                C = [0 for _ in range(k)]
            
                #iterate through all the cols in m2
                for i in range(k):
                    
                    #iterate through all the rows in m2 
                    for j in range(n2):
                        C[i] += m1[j] * m2[j][i]
                
                    
                #Now, we need to transpose to keep the original output if we didnt swap m1 and m2
                #by transposing it should result in the correct output
                temp = []
                for i in range(len(C[0])):
                    col = []
                    
                    for j in range(len(C)):
                        col.append(C[j][i])
                    
                    temp.append(col)
                
                C = temp
                
            
            else:
                print('Error(Matrix.mul): size mismatch')
                C = Matrix.to_matrix([])
                return C
                            
            C = Matrix.to_matrix(C)
                        
                            
        else:
            
            print('Error(Matrix.scalar_mul): invalid input')
            C = Matrix()
        
        
        return C
    
    
    @staticmethod
    def mod(A,m):
        """
        ----------------------------------------------------
        Parameters:   A (Matrix): an arbitrary Matrix object
                      m (int): mod
        Return:       B (Matrix): output matrix
        Description:  Return a matrix which has same elements as A
                      but with residue values mod m
        Errors:       if one of the inputs is invalid or A is empty:
                        print error msg
                        return empty Matrix object
        ---------------------------------------------------
        """
        matrix = A.to_list()
        #print(matrix)
        #print(len(matrix))
        nrow, ncol = A.get_size()
        
        #make sure its a valid mod >=2
        if type(m) is int and m >= 2:
            
            #traverse matrix and perform mod on the elements in each [row][col]
            if nrow != 0:
                B = [[1 for _ in range(ncol)] for _ in range(nrow)]
                for i in range(len(matrix)):
                    for j in range(len(matrix[i])):
                        modobj = MOD(matrix[i][j], m)
                        B[i][j] = modobj.get_residue()
            
            #traverse vector instead, same operations
            else:
                B = [1 for _ in range(ncol)]
                for i in range(len(matrix)):
                    modobj = MOD(matrix[i], m)
                    B[i] = modobj.get_residue()
         
        else:
            print('Error(Matrix.mod): invalid input')
            B = []
            
        #convert the list to the mod object
        B = Matrix.to_matrix(B)            
        return B      
    
    
    def det(self):
        """
        ----------------------------------------------------
        Parameters:   - 
        Return:       det (int): determinant
        Description:  Finds the determinant of current matrix
                      works only for 2x2 matrices
        Errors:       if current matrix is empty or non square, or
                      if size other than 2x2:
                        print error msg, return 0
        ---------------------------------------------------
        """
        
        nrow, ncol = self.get_size()
        
        matrix = self.get_matrix()
        
        #if its square but not 2x2 then unsupported matrix size, or if its just 1 element
        #if its empty or not square then the det. does not exist
        if nrow == 2 and nrow == ncol:
            matrix = self.to_list()
            
            #det = ad - cd
            det = matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
        
        elif len(matrix) == 0 or len(matrix) == 2:
            print("Error(Matrix.det): det does not exist")
            return 0
        
        else: 
            print("Error(Matrix.det): unsupported matrix size")
            return 0
        
        
        return det
    
    
    @staticmethod
    def inverse_mod(A, m):
        """
        ----------------------------------------------------
        Parameters:   A (Matrix): an arbitrary Matrix object
                      m (int): mod 
        Return:       B (Matrix): output matrix
        Description:  Finds the inverse of matrix A mod m
                      works only for 2x2 matrices
        Errors:       if invalid A or m, or invalid size, or inverse does not exist
                        return empty Matrix object
        ---------------------------------------------------
        """
        B = []
        
        nrow, ncol = A.get_size()
        
        if nrow == 2 and nrow == ncol and m >= 2:
            #step 1: find determinant of A and its equivalent with x mod m where x is the difference
            det = A.det()
            #print(det)
            if det < 0 and abs(det) < m: #we need to make sure that the det is also smaller than m
                det = m % abs(det)
            
            #step 2: Is the det(A) and m relatively prime? gcd(det(a), m) == 1
            relatively_prime = MOD.is_relatively_prime(det, m)
            #print(relatively_prime)
            
            #step 3: if they are relatively prime: find det(A)^-1 mod m (same as getting EEA)
            if relatively_prime and MOD.gcd(det, m) == 1: #for whatever reason in get_mul_inv its not checking gcd == 1 bc python gay
                modobj = MOD(det, m)
                #print("det: " + str(det))
                #print(m)
                #print(modobj.get_mod())
                #print(modobj.gcd(det, m))

                det_mod_inverse = modobj.get_mul_inv()
                
                #print("det_mod_inverse: " + str(det_mod_inverse))
                
                #step 4: scalar mult. det(A)^-1 * [[d, -b] [-c, a]
                B = A.to_list()
                a = B[0][0]
                b = B[0][1]
                c = B[1][0]
                d = B[1][1]
                
                B = [[d, -b], [-c, a]]
                
                #print(B)
                
                #perform the scalar_mul to the inverse mod, and then turn it into a matrix object and perform mod
                Matrix.scalar_mul(det_mod_inverse, B)
                B = Matrix.to_matrix(B)  
                B = Matrix.mod(B, m)
            
            else:
                B = Matrix.to_matrix([]) 
        else:
            B = Matrix.to_matrix([]) 
                
        return B


class Hill:
    """
    ----------------------------------------------------
    Cipher name: Hill Cipher
    Key:         (keyword,start,end)
    Type:        Substitution Cipher
    Description: y = kx mod m
                 x = k(-1)y mod m
                 k is the matrix representation of keyword
                 base = BASE[start:end]
                 m = len(base)
                 Applies only to characters defined in the base
                 Applies only to key matrices of size 2x2
    ----------------------------------------------------
    """
    BASE = utilities.get_base('lower') + ' ' + utilities.get_base('nonalpha') + utilities.get_base('upper')
    DEFAULT_KEY = ('food', 0, 26)
    DEFAULT_PAD = 'q'
    
    def __init__(self,key=DEFAULT_KEY,pad=DEFAULT_PAD):
        """
        ----------------------------------------------------
        Parameters:   _key (tuple(Matrix,int,int)): (k,start,end)
        Description:  Hill cipher constructor
                      sets _key and _pad
        ---------------------------------------------------
        """
        self._key = self.DEFAULT_KEY
        if key != self.DEFAULT_KEY:
            self._key = self.set_key(key)
            
        self._pad = self.DEFAULT_PAD
        if pad != self.DEFAULT_PAD:
            self._pad = self.set_pad(pad)

    @staticmethod
    def encode(keyword, base, size):
        """
        ----------------------------------------------------
        Parameters:   keyword (str): an arbitrary keyword
                      base (str): a sequence of unique characters
                      size (int): #columns in output matrix
        Return:       k (Matrix): matrix representation of the given key
        Description:  Takes a keyword and constructs a corresponding matrix
                      matrix items represent indices of keyword characters in base
                      The output matrix is always 2 x size
                      characters undefined in the base are removed from key
                      
                      if keyword is too long, use first elements
                      if key is too short, use running key
                      if invalid key, matrix or size --> return empty Matrix
        ---------------------------------------------------
        """
        
        #we cant use valid key, because the testing uses keys that ARE NOT VALID!!!!!!!!!!!!!!!!
        if type(keyword) is str or size <= 0:
            total_elements = 2 * size
            
            #we need to strip the keyword of anythiung thats not in base
            s_keyword = '' #stripped keyword
            for char in keyword:
                if char in base:
                    s_keyword += char
            
            
            #as long as there is a char left over, then we can make the matrix
            if s_keyword != 0:
                
                #if keyword is too long, use first elements
                #if key is too short, use running key
                if len(s_keyword) < total_elements:
                    s_keyword = s_keyword*100 #100 just so I know the key will always be long enough
                if len(s_keyword) > total_elements:
                    s_keyword = s_keyword[:total_elements]
                
                #key = (s_keyword, start, end)
                
                #print(s_keyword)
                k = [[0 for _ in range(int(total_elements/2))] for _ in range(2)]
                #print(k)
                
                curr = 0
                for i in range(2):
                    for j in range(int(total_elements/2)):
                        k[i][j] = base.find(s_keyword[curr])
                        curr += 1
                
                #print(k)
                k = Matrix.to_matrix(k)
            
            else:
                k = Matrix(0,0)
        else:
            k = Matrix(0,0)
            
        return k

    @staticmethod
    def decode(matrix, base):
        """
        ----------------------------------------------------
        Parameters:   matrix (obj): an arbitrary Matrix object
                      base (str): a sequence of unique characters
        Return:       keyword (str)
        Description:  Takes a square matrix and constructs a corresponding keyword
                      matrix items represent indices of keyword characters in base
                      The output is a string of length similar to #rows in matrix
                      if invalid matrix or base, return empty string
        ---------------------------------------------------
        """
        keyword = ''
        
        if type(matrix) is Matrix and base in Hill.BASE:
            
            #get the total number of char to go through
            nrums, ncols = matrix.get_size()
            total_chars = nrums*ncols
            
            matrix_list = matrix.to_list()
            
            #simply convert the position of the [row][col] back to the base indexes and thats it!
            for row in range(2):
                for col in range(int(total_chars/2)):
                    keyword += base[matrix_list[row][col]]
            
        
        return keyword
        
    def set_pad(self,pad):
        """
        ----------------------------------------------------
        Parameters:   pad (str): a padding character
        Return:       success: True/False
        Description:  Sets hill cipher pad to given character
                      a pad should be a single character from the base
                      if invalid pad, set to default value
        ---------------------------------------------------
        """ 
        success = False
        base = self.get_base()

        if type(pad) is str and len(pad) == 1 and pad in base:
            self._pad = pad
            success = True

        return success
    
    def get_pad(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       pad (str): current padding character
        Description:  Returns a copy of current padding character
        ---------------------------------------------------
        """ 
        return self._pad

    def get_key(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       key (Matrix,int,int)
        Description:  Returns a copy of the Hill cipher key
        ---------------------------------------------------
        """
        return self._key
       
    def get_key_matrix(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       k (Matrix)
        Description:  Returns a matrix representation of the keyword
        ---------------------------------------------------
        """ 
        
        keyword = self.get_key()[0]
        base = self.get_base()
                        
        #1- All characters undefined in the base are removed. 
        #2- Has at least one character from the base
        s_keyword = '' #stripped keyword
        for char in keyword:
            if char in base:
                s_keyword += char
                            
        if len(s_keyword) < 2:
            s_keyword = s_keyword*4
        if len(s_keyword) < 4:
            s_keyword = s_keyword*2
        if len(s_keyword) > 4:
            s_keyword = s_keyword[:4]
        
        #get the indexes of base for the first 4 char in the keyword
        index1 = base.find(s_keyword[0])
        index2 = base.find(s_keyword[1])
        index3 = base.find(s_keyword[2])
        index4 = base.find(s_keyword[3])
        
        #create list and convert back to matrix object
        key_matrix = [[index1, index2], [index3, index4]]
        key_matrix = Matrix.to_matrix(key_matrix)
        
        return key_matrix
    
    def set_key(self,key):
        """
        ----------------------------------------------------
        Parameters:   key (k,start,end): tuple(Matrix, int,int)
        Return:       success: True/False
        Description:  Sets Hill cipher key to given key
                      if invalid key --> set to default key
        ---------------------------------------------------
        """ 
        #any valid key can be set, and will not be stripped unless
        #operations are performed on it, which those methods will
        #take care of that
        success = False
        
        if Hill.valid_key(key):
            self._key = key
            success = True
        else:
            self._key = self.DEFAULT_KEY
            
        return success

    def get_base(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       base (str)
        Description:  Returns a copy of the Hill base
                        which is a subset of BASE
        ---------------------------------------------------
        """
        start = self._key[1]
        end = self._key[2]
        return self.BASE[start:end]
        
    def __str__(self):
        """
        ----------------------------------------------------
        Parameters:   -
        Return:       output (str)
        Description:  Constructs and returns a string representation of 
                      Hill cipher object. Used for testing
                      output format:
                      Hill Cipher:
                      key = <key>, pad = <pad>
        ---------------------------------------------------
        """
        return 'Hill Cipher:\nkey = ' + str(self.get_key()[0]) + ", m = " + str(self.get_key()[2] - self.get_key()[1]) + ", pad = " + str(self.get_pad()) 
    
    @staticmethod
    def valid_key(key):
        """
        ----------------------------------------------------
        Static Method
        Parameters:   key (?):
        Returns:      True/False
        Description:  Checks if given key is a valid Hill key
                      A valid key should be a tuple consisting of three parameters
                      <k> should be a keyword (str) that corresponds to:
                          a matrix of size 2x2 and has a multiplicative inverse in mod m
                      start < end, and both are positive valid indexes for BASE
                      The base should contain at least two chars
        ---------------------------------------------------
        """
        valid = False
        
        keyword = key[0]
        start = key[1]
        end = key[2]
        
        if type(keyword) is str and type(start) is int and type(end) is int: 
            if start >= 0 and end < len(Hill.BASE) and start < end and end-start>=2:
                
                #1- All characters undefined in the base are removed. 
                base = Hill.BASE[start:end]

                #2- Has at least one character from the base
                s_keyword = '' #stripped keyword
                for char in keyword:
                    if char in base:
                        s_keyword += char

                #2- Has at least one character from the base
                if len(s_keyword) > 1:

                    #3- Corresponds to a 2x2 matrix that is invertible mod m, *where m is the length of the base.*
                    #4- If the keyword is too long, only the first 4 characters are selected
                    #5- If the keyword is too short, a running key is used. 
                    m = len(Hill.BASE[start:end])
                    
                    if len(s_keyword) < 2:
                        s_keyword = s_keyword*4
                    if len(s_keyword) < 4:
                        s_keyword = s_keyword*2
                    if len(s_keyword) > 4:
                        s_keyword = s_keyword[:4]
                        
                    #get the indexes in base for the first 4 char in the keyword (only 4 char are required)
                    index1 = base.find(s_keyword[0])
                    index2 = base.find(s_keyword[1])
                    index3 = base.find(s_keyword[2])
                    index4 = base.find(s_keyword[3])    
                    
                    key_matrix = [[index1, index2], [index3, index4]]
                    
                    matrix = Matrix.to_matrix(key_matrix)
                    inverse_matrix = Matrix.inverse_mod(matrix, m)
                    #empty_matrix = Matrix.to_matrix([])
                    
                    #print("inverse" + str(inverse_matrix))
                    #print("empty" + str(empty_matrix))
                    inverse_list = inverse_matrix.to_list()
                    
                    #print('---------------')
                    #print(keyword)
                    #print(s_keyword)
                    #print(inverse_matrix)
                                        
                    if inverse_list != []:
                        valid = True
                    
        return valid

    def encrypt(self,plaintext):
        """
        ----------------------------------------------------
        Parameters:   plaintext (str)
        Return:       ciphertext (str)
        Description:  Encryption using Hill Cipher
        ---------------------------------------------------
        """
        assert type(plaintext) is str, 'invalid input'
        ciphertext = ''
        
        base = self.get_base()
        #print(base)
        not_in_base_str = ''
        
        #remove all the characters that are not in base before encryption
        for char in plaintext:
            if char not in base:
                not_in_base_str += char
        
        not_in_base = utilities.get_positions(plaintext, not_in_base_str)
        plaintext = utilities.clean_text(plaintext, not_in_base_str)      

        #pair each char in plainblocks to blocksize 2
        plainblocks = utilities.text_to_blocks(plaintext, 2, True, self.get_pad())

        #Assume blocksize will always be 1 for 2x1 matrix in encode  
        encoded_plainblocks = []
        for block in plainblocks:
            encoded_plainblocks.append(Hill.encode(block, self.get_base(), 1))
            #print(Hill.encode(block, self.get_base(), 2))
            
        
        #once encoded, we can perform the hill cipher operations of multiplying the
        #encoded blocks by the key and converting the result back to the char at base index n
        #thus enciphering the text
        keymatrix = self.get_key_matrix()
        #print("key:\n" + str(keymatrix.to_list()))
        for blockObj in encoded_plainblocks:

            #print("current block:\n" + str(blockObj.to_list()))
            result = []
            result = Matrix.mul(keymatrix, blockObj)
            #print("after mult:\n" + str(result))
            final = Matrix.mod(result, self.get_key()[2] - self.get_key()[1])
            #print("after mod:\n" + str(final))
            
            #decode gets us the converted char at base given the matrix object input
            ciphertext += Hill.decode(final, self.get_base())
            
        #reinsert the non-enciphered char
        ciphertext = utilities.insert_positions(ciphertext, not_in_base)
        
        return ciphertext
    
    
    def decrypt(self,ciphertext):
        """
        ----------------------------------------------------
        Parameters:   ciphertext(str)
        Return:       plaintext (str)
        Description:  Decryption using Hill Cipher
        ---------------------------------------------------
        """
        assert type(ciphertext) is str, 'invalid input'
        plaintext = ''

        #remove all the characters that are not in base before encryption        
        base = self.get_base()
        #print(base)
        not_in_base_str = ''
        for char in ciphertext:
            if char not in base:
                not_in_base_str += char
        
        not_in_base = utilities.get_positions(ciphertext, not_in_base_str)
        ciphertext = utilities.clean_text(ciphertext, not_in_base_str)   
        
        #pair each char in cipherblocks to blocksize 2
        cipherblocks = utilities.text_to_blocks(ciphertext, 2, True, self.get_pad())
        
        #Assume blocksize will always be 1 for 2x1 matrix in encode  
        encoded_cipherblocks = []
        for block in cipherblocks:
            encoded_cipherblocks.append(Hill.encode(block, self.get_base(), 1))
        
        
        #once encoded, we can perform the hill cipher operations of multiplying the
        #encoded blocks by the inverse key and converting the result back to the char at base index n
        #thus decrypting the text
        keymatrix = self.get_key_matrix()
        m = len(base)
        inv_keymatrix = Matrix.inverse_mod(keymatrix, m)
        
        for blockObj in encoded_cipherblocks:
            #print("current block:\n" + str(blockObj.to_list()))
            result = []
            result = Matrix.mul(inv_keymatrix, blockObj)
            #print("after mult:\n" + str(result))
            final = Matrix.mod(result, self.get_key()[2] - self.get_key()[1])
            #print("after mod:\n" + str(final))
        
            #decode gets us the converted char at base given the matrix object input
            plaintext += Hill.decode(final, self.get_base())
        
        #reinsert the non-enciphered char
        plaintext = utilities.insert_positions(plaintext, not_in_base)
        plaintext = plaintext.rstrip(self.get_pad())
            
        return plaintext


   
class PRNG:
    """
    ----------------------------------------------------
    Description: Pseudo random number generators
    ----------------------------------------------------
    """
    PRIMES_FILE = 'primes.txt'
    
    @staticmethod
    def LFSR(feedback, IG, bits):
        """
        ----------------------------------------------------
        Parameters:   feedback (str): a binary number representing feedback equation
                      IG (str): a binary number representing initial configuration state
                      bits (int): number of bits to generate
        Return:       output (str): random binary bits
        
        Description:  Linear Feedback Shift Register
                      Used for generating random bits
                      
                      feedback binary maps to feedback equation
                          Example 1: feedback = '01001'
                              0*b5 + 1*b4 + 0*b3 + 0*b2 + 1*b1
                          
                          Example 2: feedback = '0101'
                              0*b4 + 1*b3 + 0*b2 + 1*b1
                      
                      Number of bits in feedback and IG should be equal
                      If invalid input --> return error message
        ---------------------------------------------------
        """ 
        output = ''
        
        #make sure they are the same length and bits is non-negative
        if len(feedback) == len(IG) and bits >= 1:
            
            #we need to make sure that we are working in binary
            isbinary1 = utilities.is_binary(feedback)
            isbinary2 = utilities.is_binary(IG)
            
            if isbinary1 == False or isbinary2 == False:
                return 'Error(PRNG.LFSR): invalid input'
            
            
            #now we can perform the calculations
            #bits is the number of bits we want to generate for our solution
            #feedback is the equation, ie. the indexes we want to xor
            #IG is the initial state of the system 
            state = IG
            #we need to determine the first xor bit, then we can shift
            xor_pos = utilities.get_positions(feedback, '1')
            
            #print('----------')
            #print("intial state: " + state)
            
            output += state[-1]
            
            for _ in range(bits-1): #-1 as we already get the first bit from initial state                 
                                
                #print('----------')
                
                #get the xor values at the feedback positions
                stateXvals = []
                for i_xor in xor_pos:
                    stateXvals.append(state[i_xor[1]])                       
                
                #print("stateXvals = " + str(stateXvals))
                
                #perform xor on all values
                xor_bit = 2
                for bit in stateXvals:
                    if xor_bit == 2:
                        xor_bit = bit
                    else:
                        #print(xor_bit)
                        #print(bit)
                        xor_bit = utilities.xor(xor_bit, bit)

                #print('xor bit: ' + str(xor_bit))
                state = utilities.shift_string(state, 1, 'r')
                
                
                #after we shift we want to replace that first bit with the xor bit
                state = str(xor_bit) + state[1:len(state)]
                
                output += state[-1]
                #print("state: = " + state)
                #print("output: " + output)
        else:
            output = 'Error(PRNG.LFSR): invalid input'
            
        return output


    @staticmethod
    def BBS(p,q,bits):
        """
        ----------------------------------------------------
        Parameters:   p (int): a prime number
                      q (int): a prime number
                      bits (int): number of bits to generate
        Return:       output (str): random binary bits
        
        Description:  Blum Blum Shub PRNG Generator
                      p and q should be primes congruent to 3
                      The seed is the nth prime number, where n = p*q
                      
                      If the nth prime number is not relatively prime with n,
                          the next prime number is selected until a valid one is found
                          The prime numbers are read from the file PRIMES_FILE (starting n=1)
                      
                      If invalid input --> return error message
        ---------------------------------------------------
        """ 
        output = ''
        
        #ensure bits is positive number
        if bits > 0:
                    
            #p and q are positive integers congruent to:  3 mod 4 
            modp = MOD(p, 4)
            if type(p) is not int or p < 0 or modp.get_residue() != 3:
                return 'Error(PRNG.BBS): invalid p'
            
            modq = MOD(q, 4)
            if type(q) is not int or q < 0 or modq.get_residue() != 3:
                return 'Error(PRNG.BBS): invalid q'
            
            
            #compute n
            n = p * q
            
            #now get the nth prime number from the primes.txt
            #open primes file and make it a list
            primes = utilities.file_to_text('primes.txt')
            primes = primes.splitlines()
                        
            seed = int(primes[n-1]) #-1 as index starts at 0
            
            #if the nth prime number is not relatively prime with n, then get the next number 
            #until a valid prime is found
            
            coprime = MOD.is_relatively_prime(seed, n)
            
            if coprime == False:
                n = n - 1 #we do this to not skip the index between nth 0 and 2
                while(coprime == False):
                    n += 1
                    seed = int(primes[n])
                    coprime = MOD.is_relatively_prime(seed, n)
            
            #now we perform the algorithm
            #where x2 = (x1**2) % n;  where x1 starts at seed and chases x2, and n is p*q
            
            #print(seed)
            #print(n)
            
            x1 = (seed**2) % n
            for _ in range(bits):
                
                x2 = (x1**2) % n
                x1 = x2
                #print('new x2 = ' + str(x2))
                
                #mod 2 to determine 0 or 1 respectively
                if (x2 % 2) == 0:
                    output += '0'
                else:
                    output += '1'
            
        
        else:
            output = 'Error(PRNG.BBS): invalid bits'
        
        
        return output
    
    
    
    
    
    
    
    
    
    
    