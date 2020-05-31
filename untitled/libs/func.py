res = []
def get_level(data,p_id=0,level=0,is_clear=True):
    if is_clear:
        res.clear()
    for item in data:
        if item['parent_id']==p_id:
            item["level"]=level
            res.append(item)
            # print(item)
            get_level(data,p_id=item['id'],level=level+1,is_clear=False)
    return res


all_id=[]
def get_all_child(data,p_id,is_clear=True):
    if is_clear:
        all_id.clear()
        all_id.append(p_id)
    for item in data:
        if item['parent_id']==p_id:
            all_id.append(item['cat_id'])
            get_all_child(data,p_id=item['cat_id'],is_clear=False)
    return all_id