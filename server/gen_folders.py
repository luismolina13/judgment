import os
for i in range(0,100):
    os.makedirs('files/' + str(i))
    os.makedirs('files/' + str(i)+'/del_keys/')
    os.makedirs('files/' + str(i)+'/downloads/')
    os.makedirs('files/' + str(i)+'/uploads/')
