from mod import MOD
import utilities


class PRNG:
    """
    ----------------------------------------------------
    Description: Pseudo random number generators
    ----------------------------------------------------
    """
    PRIMES_FILE = 'primes.txt'
    
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