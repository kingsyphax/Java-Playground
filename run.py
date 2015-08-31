#!/usr/bin/env python

import subprocess
import os
import sys

history = "-h" in sys.argv

try:
    outerhistory = ""
    innerhistory = ""
    while True:
        outer = ""
        inner = ""

        outerbraces = 0
        innerbraces = 0
        lastbrace = None

        javafile = open("Main.java", "w")

        javafile.write("import java.util.*;")
        javafile.write("import java.io.*;")

        nextline = raw_input("> ").strip()
        while len(nextline) > 0 and nextline[0] == ">":
            nextline = nextline[1:].strip()
        while nextline != "":
            #if nextline[-1] not in ";{}[(":
            #    nextline += ";"

            if nextline[-1] != ";" and "{" not in nextline and "}" not in nextline:
                nextline = "System.out.println(" + nextline + ");"

            if "{" in nextline:
                if "class" in nextline or "enum" in nextline or "void" in nextline or "public" in nextline or "private" in nextline:
                    outerbraces += 1
                    lastbrace = "outer"
                else:
                    innerbraces += 1
                    lastbrace = "inner"

            if outerbraces > 0:
                outer += nextline
                if history:
                    outerhistory += nextline
            else:
                inner += nextline
                if history:
                    innerhistory += nextline

            if "}" in nextline:
                if lastbrace == "outer":
                    outerbraces -= 1
                else:
                    innerbraces -= 1
            
            nextline = raw_input("> ").strip()
            while len(nextline) > 0 and nextline[0] == ">":
                nextline = nextline[1:].strip()

        javafile.write(outer)
        javafile.write("public class Main {")
        javafile.write("    public static void main(String[] args) {")
        javafile.write(inner)
        javafile.write("    }")
        javafile.write("}")

        javafile.close()

        print("\n")

        subprocess.call("javac -Xlint:none Main.java", shell = True)

        subprocess.call("java Main", shell = True) 

        print("\n")
except (KeyboardInterrupt, EOFError):
    subprocess.call("rm Main.java", shell = True)
    if "Main.class" in os.listdir("."):
        subprocess.call("rm Main.class", shell = True)

    print("")
