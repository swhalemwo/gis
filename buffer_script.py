import os
import arcpy
import csv

arcpy.env.workspace = "H:/final_gis/env2/"


for fid in list(range(195)):
  
  # buffer1: buffer shapefile
  arcpy.SelectLayerByAttribute_management("buffer1", "NEW_SELECTION", '"FID" = {}'.format(fid))
  arcpy.Intersect_analysis(["buffer1", "ADAM_NBH"], "intsect_xx", "ALL", "", "")
  
  
  arcpy.AddField_management("intsect_xx","Shape_Area","DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
  arcpy.CalculateField_management("intsect_xx","Shape_Area","!shape.area@squaremeters!","PYTHON_9.3","#")  

  arcpy.AddField_management("intsect_xx","area_prop","DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
  arcpy.CalculateField_management("intsect_xx", "area_prop", "[Shape_Area]/[area_ttl]")
  
  
  arcpy.AddField_management("intsect_xx", "nw_pct2", "FLOAT", 10, 2)
  arcpy.CalculateField_management("intsect_xx", "nw_pct2", "[NW0011] * [area_prop]")

# =====================  

  arcpy.AddField_management("intsect_xx", "rest_pct2", "FLOAT", 10, 2)
  arcpy.CalculateField_management("intsect_xx", "rest_pct2", "[REST0011] * [area_prop]")

  summed_nw=0
  with arcpy.da.SearchCursor("intsect_xx", "nw_pct2") as cursor:
    for row in cursor:
      summed_nw=summed_nw+ row[0]
  
  summed_rest=0
  with arcpy.da.SearchCursor("intsect_xx", "rest_pct2") as cursor:
    for row in cursor:
      summed_rest=summed_rest+ row[0]
  
  env2_pct=summed_nw/(summed_rest+summed_nw)

  name_raw=arcpy.SearchCursor("buffer1", """FID = fid""", "", 'naam')
  for x in name_raw:
    name_pr = x.naam
  
  
  # saving results
  with open("res_fnl1.csv", "a") as fo:
    wr=csv.writer(fo)
    wr.writerow([fid, env2_pct, summed_nw, summed_rest, name_pr])
 
  # cleaning up for next loop
  arcpy.Delete_management("intsect_xx")
  

  mydir="H:/final_gis/env2/"
  
  filelist = [ f for f in os.listdir(mydir)]
  for f in filelist:
    os.remove(os.path.join(mydir, f))

  
 
