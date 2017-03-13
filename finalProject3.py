#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 21:46:16 2017

@author: skylernorgaard
"""

import random
import sympy
import hashlib
from math import gcd
import gmpy2



#found a known p and q value from NSA Website and converted to integer
q = int("0xE950511EAB424B9A19A2AEB4E159B7844C589C4F",16)
p = int("E0A67598CD1B763BC98C8ABB333E5DDA0CD3AA0E5E1FB5BA8A7B4EABC10BA338FAE06DD4B90FDA70D7CF0CB0C638BE3341BEC0AF8A7330A3307DED2299A0EE606DF035177A239C34A912C202AA5F83B9C4A7CF0235B5316BFC6EFB9A248411258B30B839AF172440F32563056CB67A861158DDD90E6A894C72A5BBEF9E286C6B" ,16)
g = int("D29D5121B0423C2769AB21843E5A3240FF19CACC792264E3BB6BE4F78EDD1B15C4DFF7F1D905431F0AB16790E1F773B5CE01C804E509066A9919F5195F4ABC58189FD9FF987389CB5BEDF21B4DAB4F8B76A055FFE2770988FE2EC2DE11AD92219F0B351869AC24DA3D7BA87011A701CE8EE7BFE49486ED4527B7186CA4610A75",16)
h = 2
#print(hashlib.sha1())

#Method used to find modular inverse of a number,a. Originally written by Al Sweigart.        
def modInv(a, m):
    if gcd(a, m) != 1:
        return None # no mod inverse exists if a & m aren't relatively prime
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3 # // is the integer division operator
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m


#KEYS
def privatekey(q):
    x = random.randrange(1,q)
    return x

def publickey(g,x,p):
    return gmpy2.powmod(g,x,p)

#SIGNING

#Called k by Stallings
def kgen(q):
    return random.randrange(1,q)

#will also take forever...
def rgen(g,k,p,q):
    return gmpy2.powmod(g,k,p)%q


def sgen(message,k,x,r,q):
    kinv = modInv(k,q) #calculate modular inverse of k mod q
    messageEncode = message.encode('utf-8') #encode the message so it can be hashed
    hashval = int(hashlib.sha1(messageEncode).hexdigest(),16) #return int value of hash digest
    return (kinv*hashval+x*r)%q

#returns a list of the signature, and then the key elements that generated that signature
def signaturegen(g,p,q,message):
    x = privatekey(q)
    y = publickey(g,x,p)
    k = kgen(q)
    r = rgen(g,k,p,q)
    s = sgen(message,k,x,r,q)
    results = [r,s,x,y,k]
    return results
  
#rememebr s here is received s
def wgen(s,q):
    return modInv(s,q)%q

#would want to input the receied message
def u1gen(message,w,q):
    messageEncode = message.encode('utf-8') #encode the message so it can be hashed
    hm = int(hashlib.sha1(messageEncode).hexdigest(),16) #return int value of hash digest
    return (hm*w)%q

def u2gen(r,w,q):
    return (r*w)%q

def vgen(g,y,u1,u2,p,q):
    gu1 = gmpy2.powmod(g,u1,p)
    yu2 = gmpy2.powmod(y,u2,p)
    return ((gu1*yu2)%p)%q

def verification(s,q,message,r,g,y,p):
    w = wgen(s,q)
    u1 = u1gen(message,w,q)
    u2 = u2gen(r,w,q)
    v = vgen(g,y,u1,u2,p,q)
    if(v==r):
        return "Message Verified"
    else:
        return "Message not verified... watch out!"
    


message = "Hi Cadigan"
messagerec = "Hi Cafigan"
signature = signaturegen(g,p,q,message)
r = signature[0]
s = signature[1]
x = signature[2]
y = signature[3]
k = signature[4]
w = wgen(s,q)
u1 = u1gen(message,w,q)
u2 = u2gen(r,w,q)
v = vgen(g,y,u1,u2,p,q)

print(verification(s,q,message,r,g,y,p))
