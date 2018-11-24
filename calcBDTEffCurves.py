import glob
from ROOT import TFile
from pprint import pprint as pp

ee_eff_dict_ZH = {}
ee_eff_dict_Single_top = {}
ee_eff_dict_TT = {}
ee_eff_dict_Drell_Yan = {}
ee_eff_dict_Dibosons = {}
ee_eff_dict_signal_hzz = {}
ee_eff_dict_signal_hww = {}


mm_eff_dict_ZH = {}
mm_eff_dict_Single_top = {}
mm_eff_dict_TT = {}
mm_eff_dict_Drell_Yan = {}
mm_eff_dict_Dibosons = {}
mm_eff_dict_signal_hzz = {}
mm_eff_dict_signal_hww = {}

masses = [250, 260, 270, 300, 350, 400, 450,    451,   600, 650, 900, 1000]

for d_e, d_m in zip(glob.glob("apr*eles*"), glob.glob("apr*muons*")):
    print 'd_e=', d_e
    print 'd_m=', d_m
    mass = int(d_e.split('_')[-1])
    if mass not in masses:
        continue
    ee_files = glob.glob(d_e + "/bdt*nom*SR*root")
    ee_bdt_before_cut = [x for x in ee_files if "after" not in x][0]
    ee_bdt_after_cut  = [x for x in ee_files if "after" in x][0]
    ee_file_bdt_before_cut = TFile (ee_bdt_before_cut)
    ee_file_bdt_after_cut = TFile (ee_bdt_after_cut)
    #print 'ee_eff_dict_signal_hww', ee_eff_dict_signal_hww
    #print 'ee_file_bdt_after_cut', ee_file_bdt_after_cut
    #print ee_file_bdt_after_cut.Get("ee_SR/ZH").GetEntries()
    #print ee_file_bdt_before_cut.Get("ee_SR/ZH").GetEntries()
    ee_eff_dict_ZH[mass] = 1.*(ee_file_bdt_after_cut.Get("ee_SR/ZH").GetEntries())/((ee_file_bdt_before_cut.Get("ee_SR/ZH")).GetEntries()) 
    ee_eff_dict_Single_top[mass] = 1.*(ee_file_bdt_after_cut.Get("ee_SR/ST")).GetEntries()/(ee_file_bdt_before_cut.Get("ee_SR/ST")).GetEntries() 
    ee_eff_dict_TT[mass] = 1.*(ee_file_bdt_after_cut.Get("ee_SR/TT")).GetEntries()/(ee_file_bdt_before_cut.Get("ee_SR/TT")).GetEntries() 
    ee_eff_dict_Drell_Yan[mass] = 1.*(ee_file_bdt_after_cut.Get("ee_SR/DY")).GetEntries()/(ee_file_bdt_before_cut.Get("ee_SR/DY")).GetEntries() 
    ee_eff_dict_Dibosons[mass] = 1.*(ee_file_bdt_after_cut.Get("ee_SR/VV")).GetEntries()/(ee_file_bdt_before_cut.Get("ee_SR/VV")).GetEntries() 
    ee_eff_dict_signal_hzz[mass] = 1.*(ee_file_bdt_after_cut.Get("ee_SR/signal_hzz")).GetEntries()/(ee_file_bdt_before_cut.Get("ee_SR/signal_hzz")).GetEntries() 
    ee_eff_dict_signal_hww[mass] = 1.*(ee_file_bdt_after_cut.Get("ee_SR/signal_hww")).GetEntries()/(ee_file_bdt_before_cut.Get("ee_SR/signal_hww")).GetEntries() 

    mm_files = glob.glob(d_m + "/bdt*nom*SR*root")
    mm_bdt_before_cut = [x for x in mm_files if "after" not in x][0]
    mm_bdt_after_cut  = [x for x in mm_files if "after" in x][0]
    mm_file_bdt_before_cut = TFile (mm_bdt_before_cut)
    mm_file_bdt_after_cut = TFile (mm_bdt_after_cut)

    mm_eff_dict_ZH[mass] = 1.*(mm_file_bdt_after_cut.Get("mm_SR/ZH").GetEntries())/((mm_file_bdt_before_cut.Get("mm_SR/ZH")).GetEntries()) 
    mm_eff_dict_Single_top[mass] = 1.*(mm_file_bdt_after_cut.Get("mm_SR/ST")).GetEntries()/(mm_file_bdt_before_cut.Get("mm_SR/ST")).GetEntries() 
    mm_eff_dict_TT[mass] = 1.*(mm_file_bdt_after_cut.Get("mm_SR/TT")).GetEntries()/(mm_file_bdt_before_cut.Get("mm_SR/TT")).GetEntries() 
    mm_eff_dict_Drell_Yan[mass] = 1.*(mm_file_bdt_after_cut.Get("mm_SR/DY")).GetEntries()/(mm_file_bdt_before_cut.Get("mm_SR/DY")).GetEntries() 
    mm_eff_dict_Dibosons[mass] = 1.*(mm_file_bdt_after_cut.Get("mm_SR/VV")).GetEntries()/(mm_file_bdt_before_cut.Get("mm_SR/VV")).GetEntries() 
    mm_eff_dict_signal_hzz[mass] = 1.*(mm_file_bdt_after_cut.Get("mm_SR/signal_hzz")).GetEntries()/(mm_file_bdt_before_cut.Get("mm_SR/signal_hzz")).GetEntries() 
    mm_eff_dict_signal_hww[mass] = 1.*(mm_file_bdt_after_cut.Get("mm_SR/signal_hww")).GetEntries()/(mm_file_bdt_before_cut.Get("mm_SR/signal_hww")).GetEntries() 


print '#ee channel'*5    
for name, dic in zip(["ZH", "ST", "TT", "DY", "VV", "HZZ", "HWW"], [ee_eff_dict_ZH, ee_eff_dict_Single_top, ee_eff_dict_TT, ee_eff_dict_Drell_Yan, ee_eff_dict_Dibosons, ee_eff_dict_signal_hzz, ee_eff_dict_signal_hww]):
    #print 'ee_eff_dict_%s=' % name
    #pp(dic)
    lists = sorted(dic.items()) # sorted by key, return a list of tuples                                                                                        
    masses,  values = zip(*lists) # unpack a list of pairs into two tuples                                                                                        
    print 'ee_eff_dict_%s_values=' % name, values



print '#mm channel'*5    
for name, dic in zip(["ZH", "ST", "TT", "DY", "VV", "HZZ", "HWW"], [mm_eff_dict_ZH, mm_eff_dict_Single_top, mm_eff_dict_TT, mm_eff_dict_Drell_Yan, mm_eff_dict_Dibosons, mm_eff_dict_signal_hzz, mm_eff_dict_signal_hww]):
    #print 'mm_eff_dict_%s=' % name
    #pp(dic)
    lists = sorted(dic.items()) # sorted by key, return a list of tuples
    masses,  values = zip(*lists) # unpack a list of pairs into two tuples
    print 'mm_eff_dict_%s_values=' % name, values

print 'masses=', masses

