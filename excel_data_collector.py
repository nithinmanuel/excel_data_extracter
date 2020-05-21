import os 
import glob
import fnmatch
import shutil
import re
import csv	
from csv import DictReader
import itertools
from collections import defaultdict
import copy
import json
import os.path
class Rewrite(object):

    def convert_file(self):
        self.params_dict = {}
        with open( r'C:\Users\nithi\Desktop\work\PARAMETRI_FRESE_M.csv', 'r') as file:
            self.dynamic_dict = csv.DictReader(file, delimiter=";")
            self.param_list = list(self.dynamic_dict)
            csv_params = copy.deepcopy(self.param_list)
            
           
    def manipulate(self):
        self.diameter = [] 
        removed_keys = ['LAVORAZIONE', 'TIPO', 'F NO HSC', 'N giri NO HSC',  '1|2|3', '4|5|7', '8', '\xa0'] 

        for idx, val in enumerate(self.param_list):
            for element in self.param_list[idx]['D']:
                self.diameter.append(element)
        for line in self.param_list:
            for element in removed_keys:   
                line.pop(element)        

    def mini_length(self): 
        rm_key = ['STEP MIN']     # for minimum length maximum step .  
        self.mini_len = copy.deepcopy(self.param_list)

        for line in self.mini_len:
            for key, value in line.items():
                if key == 'L MIN-MAX':
                    length = re.search(r'(?<=|)\w+', value)
                    for element in length.group(0):
                        line.update({key:element})

        for line in self.mini_len:
            for item in rm_key:
                line.pop(item)
                 
    def max_length(self):
        self.max_len = copy.deepcopy(self.param_list)
        rm_key = ['STEP MAX'] # for maximum length minimum step . 

        for line in self.max_len:
            for key, value in line.items():
                if key == 'L MIN-MAX':
                    length = re.search(r'(?<=|)\d{2}', value)
                    if length:
                        b = []
                        x = length.group(0)
                        b.append(x)
                        for element in b:
                            line.update({key:element}) 

        for line in self.max_len:
            for item in rm_key:
                line.pop(item)                                                        
                    

    def static_params(self):
        self.fixed_dict = {'&TP_TOL': '0.005', '&TP_CCTYPE':'1', '&TP_CCHOLDERNAME':'tlx-fs://wncdefault/Holder/TEST',
         '&TP_CPPNUM':'0', '&TP_FRRAPID':'50000','&TP_AUTOSTEPOVER':'0', '&TP_AUTOPKTW':'1', '&TP_AUTOZSTEP':'1',
         '&TP_CSIDE':'1', '&TP_ZSTEPTYPE':'2', '&TP_APPROACH':'3', '&TP_STOCK':'0','&TP_RETRACT':'5', '&TP_CCSTOCK':'1',
         '&TP_CTNUMBEROFTEETH':'1','&MANUF_NUMB_CUTTING_EDGES' :'1', '&TP_COOLANTCODE':'-1', '&TP_FRRAPID_MM':'50000', 
         '&TP_COLCHK_SPINDLE_CLEARANCE':'1', '&TP_COLCHK_EXTENSION_CLEARANCE':'0' }
        
        self.auto_gen = {'&TP_BRAD':'4D', '&TP_CRAD':'4D', '&TP_CCTOOLLENGTH':'50Length',
         '&TP_CSHANKRAD':'4D', '&TP_CTAPERANGLE':'0', '&TP_CCYLHEIGHT':'30', '&TP_CCUTHEIGHT':'30' }

    def calc_params(self):
        
        self.minior_dict =  copy.deepcopy(self.mini_len) # minimum step
        self.major_dict = copy.deepcopy(self.max_len) # maximum step 
        #collective_list = [self.minior_dict,self.major_dict ]

        b = ['D', 'L - min', '&TP_FRCUT', '&TP_SPINDLE', '&TP_STEP' ]
        d = []
        for line in self.minior_dict:
            c = list(line.values())
            #print(c)
            d.append(c) 
        
        #print(d) 

        minz_params = []
        jio = {}
        for q, a in zip(b, d):
            jio = (dict(zip(b, a)))
            minz_params.append(jio)  

           

        neededmin_params = copy.deepcopy(minz_params) # minimum step 
    
        for line in neededmin_params:
            line.pop('D')
            line.pop('L - min')
        
        f = []

        for line in self.major_dict:
            h = list(line.values())
            f.append(h)
            
        maz_params = []
        kio = {}

        for q, a in zip(b, f):
            kio = (dict(zip(b, a)))
            maz_params.append(kio)
          

        neededmaz_params = copy.deepcopy(maz_params)   # maximum step 

        for line in neededmaz_params:
            line.pop('D')
            line.pop('L - min')
            
            

        calculate_params =  copy.deepcopy(minz_params)    
            
        for line in calculate_params:
           for key , value in line.items():
               if key == '&TP_FRCUT':
                   pia = []
                   pia.append(value) 
                   value = float(value) * 0.8
                   club = []
                   club.append(value)
                   for element in club:
                       line.update({key:element})
                       
                           
           for key , value in line.items():
                if key == 'D':
                    value = int(value)/7
                    value  = '%.3f'%(value)
                    dia = []
                    dia.append(value)
                    for element in dia:
                        line.update({key:element})
        
        
           for key, value in line.items():
               if key == '&TP_SPINDLE':
                   for element in club:
                       line.update({key:element}) 
           for key, value in line.items():
               if key == 'L - min':
                   for element in pia:
                       line.update({key:element})           
        for line in calculate_params:
            line['&TP_FRAPPROACH'] = line.pop('&TP_FRCUT')
            line['&TP_FRAPPROACH_MM'] = line.pop('&TP_SPINDLE')
            line['&TP_HSMSRFSMTHRAD'] = line.pop('D')
            line['&TP_FRCUT_MM']  =  line.pop('L - min')
            line.pop('&TP_STEP') 
                      
        converted_minparams =  copy.deepcopy(calculate_params) 
        converted_mazparams = copy.deepcopy(calculate_params)                                       
        #####
        partial_param = []
        kappa = []
        jippa = []
        merged = []
        for line in converted_minparams:   # minimum step 
            t = list(line.items())
            kappa.append(t)
        for element in neededmin_params:
            s = list(element.items())
            jippa.append(s) 
        for q, a in zip(kappa, jippa):
            merged = (list(zip(q, a)))
            partial_param.append(merged)

        pk = []
        dyanamic_minvariables = [] 
        for item in partial_param:
            k = list(itertools.chain(*item))
            pk.append(k)
        for element in pk:
            rdp = dict(element)
            dyanamic_minvariables.append(rdp) 
        #print(dyanamic_minvariables)       
        
        for line in dyanamic_minvariables:
            line.update(self.fixed_dict)
        #print(dyanamic_minvariables)
        #######
        half_param = []
        asd = []
        ksp = []
        combined = []

        for line in converted_mazparams:   # minium step
            t = list(line.items())
            asd.append(t)
        for element in neededmaz_params:
            s = list(element.items())
            ksp.append(s) 
        for q, a in zip(asd, ksp):
            combined = (list(zip(q, a)))
            half_param.append(combined)
        sk = []
        dynamic_mazvaribales = []

        for item in half_param:
            k = list(itertools.chain(*item))
            sk.append(k)
        for element in sk:
            rdp = dict(element)
            dynamic_mazvaribales.append(rdp)
        #print(dynamic_mazvaribales)
        #print(neededmaz_params)   
        #print(neededmin_params)     
        
        for line in dynamic_mazvaribales:
            line.update(self.fixed_dict)
        #print(dynamic_mazvaribales)    
        
        self.output_min = copy.deepcopy(dyanamic_minvariables)
        self.output_max = copy.deepcopy(dynamic_mazvaribales)

    
    def transform(self):  

        print(self.output_min)
        x = self.output_min[0]

        with open(r'C:\Users\nithi\Desktop\tests\Ø2_G6\Fresa Sferica D2 G6 L65 Utile 10.wkz', 'w') as f:
            for key , value in x.items():
                f.writelines('%s%s%s=%s\n' %(key.ljust(18), ':'.ljust(7) , key, value))
                
        """
        
           for path, directories, files in os.walk('C:\dir1\dir2\startdir'):
           if file in files:
           print 'found %s' % os.path.join(path, file)        
        """       

                 
        
        


       
        

obj = Rewrite()
obj.convert_file()
obj.manipulate()
obj.mini_length()
obj.max_length()
obj.static_params()
obj.calc_params()
obj.transform()



    

 
