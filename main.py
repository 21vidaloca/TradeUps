import requests
import json
from typing import Optional, Dict, Any
from urllib.parse import quote 
import re 
from pret import get_skin_price
from conditie import get_condition
from iesiri import get_outcome
from posibilitati import get_possible_outcome_for
from combinatie import find_best_tradeup_combo
from price_gemini import fetch_skin_price

# FACEM BAZA DE DATE ###############################################
skins=[]
with open("skins.json", "r", encoding="utf-8") as f:
    skins = json.load(f)
skin_db=[]
with open("collections.json", 'r', encoding='utf-8') as f:
	skin_db=json.load(f)

skin_name = "AK-47 | Redline"
skin_condition = "Field Tested"
skin_float = 0.16
pret=float(fetch_skin_price(skin_name, skin_condition, skin_float or None)["text"].strip("$"))
print(pret)
# FACEM INTRAREA
# GENERAM TOATE POSIBILITATILE CU DOUA SKIN URI

# lista=find_best_tradeup

# for x in skins:
#     if(x["category"]["name"]!="Knives" and x["category"]["name"]!="Gloves"):
#         print(x["pattern"]["name"])
#####################################################################

# def get_skin_price(weapon_name: str, skin_name: str, condition: str) -> Optional[Dict[str, Any]]:
# def get_condition(float_value):
# lista=[]
# weapon_name="R8 Revolver"
# skin_name="Survivalist"
# collection="The Horizon Collection"
# condition="Factory New"
# min_float=0
# max_float=0.7
# float_value=0.035
# outcomes=get_possible_outcome_for(weapon_name, skin_name, skin_db)
# weapon=(weapon_name, skin_name, condition, collection, outcomes,min_float,max_float, float_value)

# for i in range(0,4):
#     lista.append(weapon)

# weapon_name="G3SG1"
# skin_name="Ventilator"
# collection="The Gamma 2 Collection"
# condition="Minimal Wear"
# min_float=0
# max_float=0.45
# float_value=0.09
# outcomes=get_possible_outcome_for(weapon_name, skin_name, skin_db)
# weapon=(weapon_name, skin_name, condition, collection, outcomes, min_float, max_float, float_value)

# for i in range(0,6):
#     lista.append(weapon)
    
# # for x in lista:
# # 	print(x)

# # print(get_skin_price(weapon_name, skin_name, condition))
# # for x in skins:
# # 	if(x["category"]["name"]!="Knives" and x["category"]["name"]!="Gloves"):
# # 		weapon_name=x["weapon"]["name"]
# # 		skin_name=x["pattern"]["name"]
# # 		condition=x["wears"][0]["name"]
# # 		collection=x["collections"]["name"]
# # 		print(get_skin_price(weapon_name, skin_name, condition))
    
# # calculam outcome contract


# input=[]
# for x in lista:
# 	weapon_name=x[0]
# 	skin_name=x[1]
# 	condition=x[2]
# 	float_val=x[7]
# 	preturi=get_skin_price(weapon_name, skin_name, condition)
# 	pret=preturi["median_price"]
# 	input.append((weapon_name,skin_name,condition,float_val,pret))

# prob_final=get_outcome(lista,skins)
# output=[]
# for x in prob_final:
# 	intrare={}
# 	for ceva in skins:
# 		if ceva["name"] == x:
# 			intrare=ceva
# 			break
# 	weapon_name=intrare["weapon"]["name"]
# 	skin_name=intrare["pattern"]["name"]
# 	condition=prob_final[x][2]
# 	float_val=x[1]
# 	preturi=get_skin_price(weapon_name, skin_name, condition)
# 	pret=preturi["median_price"]
# 	prob=str(prob_final[x][0]*100)+"%"
# 	output.append((weapon_name,skin_name,condition,float_val,prob,pret))
# # for x in prob_final:
# # 	print(x,prob_final[x])
# print("INTRARE")
# for x in input:
# 	print(x)
# print("IESIRE")
# for x in output:
#  	print(x)

# # AICI AVEM PROBABILITATILE SI CELE NECESARE PENTRU A CALCULA PROFITABILITATEA
# # intrare
# suma_intrare=0
# for x in input:
# 	# print(x)
# 	suma_intrare+=x[4]
# print("Intram cu ",suma_intrare," dolari")
# # iesire
# for x in output:
# 	# print(x)
# 	p=x[4]
# 	n=x[0]
# 	s=x[1]
# 	pr=x[5]
# 	dif=pr-suma_intrare
# 	if(dif>0):
# 		text="Posibilitate de "+p+" pentru "+n+"|"+s+" cu valoare de "+str(pr)
# 		print(f"\033[32m{text}\033[0m")
# 	elif dif<0:
# 		text="Posibilitate de "+p+" pentru "+n+"|"+s+" cu valoare de "+str(pr)
# 		print(f"\033[31m{text}\033[0m")
# 	elif dif==0:
# 		text="Posibilitate de "+p+" pentru "+n+"|"+s+" cu valoare de "+str(pr)
# 		print(f"\033[33m{text}\033[0m")