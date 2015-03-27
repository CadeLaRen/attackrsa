#!/usr/bin/env python

import Wiener
import Fermat
import Hastad
import ChosenCipher
import argparse
import sys

def autoInt(n):
    res = n.split(",")
    if len(res)==1:
        return int(res[0],0)
    else:
        return [int(x,0) for x in res]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-t", dest="technique", help="Available techniques: wiener, fermat, hastad, chosen-cipher") 
    parser.add_argument("-p", dest="p", help="Prime number", type=autoInt) 
    parser.add_argument("-q", dest="q", help="Prime number", type=autoInt) 
    parser.add_argument("-n", dest="n", help="Modulus", type=autoInt) 
    parser.add_argument("-e", dest="e", help="Public exponent", type=autoInt) 
    parser.add_argument("-c", dest="c", help="Cipher text", type=autoInt) 
    parser.add_argument("-f", dest="f", help="A factor used in chosen cipher text", type=autoInt) 
    parser.add_argument("-P", dest="P", help="The plain text decrypted from the chosen cipher", type=autoInt) 

    args = parser.parse_args()

    if not args.technique:
        print "Please choose a technique.\n"
        parser.print_help()
        exit(1)
    if args.technique == "wiener":
        if not args.n:
            print "Please provide the modulus.\n"
            parser.print_help()
            exit(1)
        if not args.e:
            print "Please provide the public exponent.\n"
            parser.print_help()
            exit(1)
        t = Wiener.Wiener(args.n, args.e)
        if t.crack():
            print "====== Cracked! ======="
            print "d is %s" % hex(t.d)
            print "p is %s" % hex(t.p)
            print "q is %s" % hex(t.q)
        else:
            print "====== Wiener attack fails! ======="
            exit(2)
        if args.c:
            pt = t.decrypt(args.c)
            print "Plain text is %s" % hex(pt)
            #print "Guessed message: %s" % hex(pt)[2:].rstrip('L').decode("hex")
    elif args.technique == "fermat":
        if not args.n:
            print "Please provide the modulus.\n"
            parser.print_help()
            exit(1)
        t = Fermat.Fermat(args.n)
        if t.crack():
            print "====== Cracked! ======="
            if args.e:
                t.e = args.e
                print "d is %s" % hex(t.getPrivKey())
            print "p is %s" % hex(t.p)
            print "q is %s" % hex(t.q)
        else:
            print "====== Fermat attack fails! ======="
            exit(2)
        if args.c:
            pt = t.decrypt(args.c)
            print "Plain text is %s" % hex(pt)
            #print "Guessed message: %s" % hex(pt)[2:].rstrip('L').decode("hex")
    elif args.technique == "hastad":
        if (not type(args.n) is list) or len(args.n)<3:
            print "At least 3 modulus are needed."
            exit(1)
        if (not type(args.c) is list) or len(args.c)<3:
            print "At least 3 cipher texts are needed."
            exit(1)
        if not args.e:
            print "A common public key is needed."
            exit(1)
        t = Hastad.Hastad(args.n, args.e, args.c)
        pt = t.decrypt()
        print "Plain text is %s" % hex(pt)
        #print "Guessed message: %s" % hex(pt)[2:].rstrip('L').decode("hex")
    elif args.technique == "chosen-cipher":
        if not args.n or not args.e or not args.c:
            print "Missing arguments. Please provide the modulus, public exponent and the cipher text."
            exit(1)
        t = ChosenCipher.ChosenCipher(args.n, args.e, args.c)
        if not args.f or not args.P:
            print "Missing arguments. Please provide a multiplication factor used to generate a new cipher text, and the corresponding plain text."
            exit(1)
        pt = t.decrypt(args.f, args.P)
        print "Plain text is %s" % hex(pt)
    else:
        print "Invalid technique %s" % args.technique
