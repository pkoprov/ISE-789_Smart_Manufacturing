import os
import pandas as pd


labels = pd.DataFrame()
for f in os.listdir(r'C:\Users\pkoprov\OneDrive - North Carolina State University\ISE 789 Smart Manufacturing\Semester Project\Images'):
    if ".jpg" in f:
        c = open(r'C:\Users\pkoprov\OneDrive - North Carolina State University\ISE 789 Smart Manufacturing\Semester Project\COde\darknet\build\darknet\x64\data\train.txt','a+')
        c.write('data/obj/'+f+"\n")
        c.close()
c.close()
        x.insert(0,"image",f)
        labels = labels.append(x, ignore_index=True)

labels.columns = ['image','label', 'xmin','ymin','xmax','ymax']
labels = labels.drop(labels.tail(5).index)


labels.iloc[labels[labels["label"]==0].index,1] = '1x1_TALL'
labels.iloc[labels[labels["label"]==1].index,1] = '1x2_LOW'
labels.iloc[labels[labels["label"]==2].index,1] = '2x2_LOW'
labels.iloc[labels[labels["label"]==3].index,1] = '1x1_TALL'
labels.iloc[labels[labels["label"]==4].index,1] = '1x3_TALL'
labels.iloc[labels[labels["label"]==5].index,1] = '1x4_TALL'

labels.to_csv(r'C:\Users\pkoprov\OneDrive - North Carolina State University\ISE 789 Smart Manufacturing\Semester Project\COde\TrainYourOwnYOLO\Data\Source_Images\Training_Images\vott-csv-export\Annotations-export.csv')

