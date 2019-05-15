#%%
class CA(object):
    
    cls_pre = 'aaaaa'

    def __init__(self):
        self.obj_pre = 'bbbbb'
#%%
a = CA()
b = CA()
#%%
print(a.cls_pre, a.obj_pre)
print(b.cls_pre, b.obj_pre)
#%%
CA.cls_pre = 'ccccc'
c = CA()
d = CA()
d.cls_pre = 'ddddd'

print(a.cls_pre, a.obj_pre)
print(b.cls_pre, b.obj_pre)
print(c.cls_pre, c.obj_pre)
print(d.cls_pre, d.obj_pre)

#%%
CA.cls_pre = [1,2]
c = CA()
print(c.cls_pre, c.obj_pre)