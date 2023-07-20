org=[[1,2],[2,3],[3,4],[5,6]]
removed_list=[[1,2],[2,3]]
dict_test={}
l3=[x for x in org if x not in removed_list]
dict_test["0"]=removed_list
removed_list.clear()
print(dict_test)
print(l3)
