org=[[1,2],[2,3],[3,4],[5,6]]
removed_list=[[1,2],[2,3]]
l3=[x for x in org if x not in removed_list]
print(l3)
