#!/usr/bin/python
#   This library is free software; you can redistribute it and/or
#   modify it under the terms of the GNU Lesser General Public
#   License as published by the Free Software Foundation; either
#   version 2.1 of the License, or (at your option) any later version.
#
#   This library is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#   Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public
#   License along with this library; if not, write to the
#     Free Software Foundation, Inc.,
#         59 Temple Place, Suite 330,
#           Boston, MA  02111-1307  USA
#    
#       Copyright 2010 jimmyromanticdevil <romanticdevil.jimmy@gmail.com>
#       http://jimmyromanticdevil.wordpress.com
#


import os
import urllib
import simplejson
from time import sleep, ctime


url_detech = 'http://ajax.googleapis.com/ajax/services/language/detect?'
url_translate = 'http://ajax.googleapis.com/ajax/services/language/translate?'
detect_params = {'v':'1.0', 'q':'',}
translate_params = {'v':'1.0', 'q':'', 'langpair':'',}



class InputError(Exception):

    def __init__(self, text, status):
        self.text = text
        self.status = status
        
        
def detect_language(text):
    detect_params['q'] = text

    url = url_detech + urllib.urlencode(detect_params)
    response = simplejson.load(urllib.urlopen(url))    

    data = response['responseData']
    
    return data

def translate_language(text, source_lang="", dest_lang=""):
    
    translate_params['q'] = text
    translate_params['langpair'] = source_lang + '|' + dest_lang
    url = url_translate + urllib.urlencode(translate_params)
    response = simplejson.load(urllib.urlopen(url))
    
    if response['responseStatus'] != 200:
        raise APIError(text, response['responseStatus'])
        
    data = response['responseData']
    
    return data
    
    

class translate_class(object):
    def __init__(self, text=()):
        self.text = text
        


    def clear(self):
        if os.name in ['nt', 'win32', 'dos']:
            os.system('cls')
        else:
            os.system('clear')

    def title(self):
        self.clear()
        print '^'*75
        print'''



                              
                        ___     
  __ _  ___   ___   __ _| | ___   
 / _` |/ _ \ / _ \ / _` | |/ _ \ 
| (_| | (_) | (_) | (_| | |  __/ 
 \__, |\___/ \___/ \__, |_|\___|  Translate 
 |___/             |___/                                                  

                   Develope by jimmyromanticdevil

'''
        print '~'*75+'\n\n'

        lt = ctime()
        print '[+] Starting googletranslate %s\n\n' %(lt)
        sleep(5)

    def translate_text(self):
        file_help = open('translatehelp.txt').read()
        print file_help
        try:
            try_google=raw_input("Try google translate ? (y/n)")
            if try_google=='y':
                while True:
                    from_language	=raw_input('[*]From Language :')
                    to_language	=raw_input('[*]To Language   :')
                    translate_text    =raw_input('[*]Enter Text fo Translate :')
                    Text1 = translate_language(translate_text, source_lang= from_language ,dest_lang= to_language)
                    print '[User@Googletranslator]> The Translate result is : '+Text1['translatedText']
            if try_google=='n':
                self.select()
        except KeyboardInterrupt:
                print '\n\n[+] Exiting.....'
                exit(1)




    def detech_lenguagee(self):
        file_help = open('detech.txt').read()
        print file_help
        try:
            chooise=raw_input("Try google translate ? (y/n)")
            if chooise=='y':   
                while True:
                    detech_text=raw_input('[+]Enter text :')
                    detech_lenguage = detect_language(detech_text)
                    print '[User@Googletranslator]> The Detech Result :'+detech_lenguage['language']
            if chooise=='n':
                self.select()
        except KeyboardInterrupt:
                print '\n\n[+] Exiting...'
                exit(0)
          
    def select(self):
        print '-'*25
        print 'select youre chooise:'
        print '-'*25
        print '\n1)Translate.\n2)Detech\n3)Exit\n'
        print '*'*25

    def main(self):
        self.title()
        sleep(3)
        while True:
            self.clear()
            self.select()
            try:
                choice = raw_input('\nYou Selected: ')
            except(KeyboardInterrupt):
                print '\n\n[!] Force Quitting..'
                sleep(2)
                exit(1)            
            if (choice in '123'):
                if (choice == '1'):
                    self.clear()
                    self.translate_text()
                elif (choice == '2'):
                    self.clear()
                    self.detech_lenguagee()
                elif (choice == '3'):
                    print '\n[*] Quitting..'
                    sleep(2)
                    exit(0)
            else:
                print '\n[-] Invalid Input! Try Again..'
                sleep(2)
                self.clear()

if __name__ == '__main__':
    class_translate = translate_class()
    class_translate.main()

