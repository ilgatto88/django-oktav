"""
from oktav.static.austria_gemeinden import create_gemeinde_dict
from region.models import Municipality

data = create_gemeinde_dict(insert_bl=True)

for k,v in data.items():
    print(k,v['name'], v['bl'])
    if v['bl'] != 'Südtirol':
        m = Municipality(name = v['name'], gkz=k, bundesland = v['bl'])
        m.save()
    else:
        print('Municipality from Südtirol, wont be uploaded')
"""