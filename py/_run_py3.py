__author__ = "Florian Thiery, Dennis Gottwald"
__copyright__ = "MIT Licence 2020, RGZM, Florian Thiery"
__credits__ = ["Florian Thiery, Dennis Gottwald"]
__license__ = "MIT"
__version__ = "1.0"
__maintainer__ = "Florian Thiery"
__email__ = "thiery@rgzm.de"
__status__ = "1.0"

import glob
import os
import os.path

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = dir_path.replace("\\", "/")
# print(dir_path)
print("start _run_py3.py...")
dir_path_ttl = dir_path.replace("py", "ttl")
filelist = glob.glob(os.path.join(dir_path_ttl, "*.ttl"))
for f in filelist:
    os.remove(f)
print("removed all ttl files...")
print("*****************************************")

# py3

# information carrier & inscription

exec(open(dir_path + "/informationcarrier.py").read())
exec(open(dir_path + "/inscriptiondie.py").read())
exec(open(dir_path + "/inscriptiongraffito.py").read())
exec(open(dir_path + "/inscriptionmakingtypedie.py").read())
exec(open(dir_path + "/inscriptionmakingtypestylus.py").read())

# potforms

exec(open(dir_path + "/genericpotform.py").read())
exec(open(dir_path + "/potformgaulish.py").read())
exec(open(dir_path + "/potformitalian.py").read())

# actors & entities

exec(open(dir_path + "/actorsasaconcept.py").read())
exec(open(dir_path + "/ae_chiefpotter.py").read())
exec(open(dir_path + "/ae_cooperationandchiefpotter.py").read())
exec(open(dir_path + "/ae_cooperationpotter.py").read())
exec(open(dir_path + "/ae_dependentpotter.py").read())
exec(open(dir_path + "/ae_independentpotter.py").read())
exec(open(dir_path + "/ae_partnerpotter.py").read())

# locations & place

exec(open(dir_path + "/loc_discoverysite.py").read())
exec(open(dir_path + "/loc_kilnregion.py").read())
exec(open(dir_path + "/loc_productioncentre.py").read())
exec(open(dir_path + "/loc_repositorylocation.py").read())
exec(open(dir_path + "/placeasaconcept.py").read())

# crosstables

exec(open(dir_path + "/ct_ac_ae.py").read())
exec(open(dir_path + "/ct_ae_pc.py").read())
exec(open(dir_path + "/ct_chp_dp.py").read())
exec(open(dir_path + "/ct_cp_pp.py").read())
exec(open(dir_path + "/ct_cpchp_dp.py").read())
exec(open(dir_path + "/ct_cpchp_pp.py").read())
exec(open(dir_path + "/ct_ic_ds.py").read())
exec(open(dir_path + "/ct_ic_in.py").read())
exec(open(dir_path + "/ct_ic_pc.py").read())
exec(open(dir_path + "/ct_ic_pf.py").read())
exec(open(dir_path + "/ct_ic_plc.py").read())
exec(open(dir_path + "/ct_ic_rl.py").read())
exec(open(dir_path + "/ct_in_ac.py").read())
exec(open(dir_path + "/ct_in_mt.py").read())
exec(open(dir_path + "/ct_pc_kr.py").read())
exec(open(dir_path + "/ct_pf_gf.py").read())
exec(open(dir_path + "/ct_plc_ds.py").read())
exec(open(dir_path + "/ct_plc_pc.py").read())
exec(open(dir_path + "/ct_plc_rl.py").read())
