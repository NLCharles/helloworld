import os
import numpy as np
import glob
from mayavi import mlab
import argparse
#Parsers
base_path=os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser()
parser.add_argument('--tool', default='plot', help='tools: pcd2txt, mayavi plot,rename06d,...')
parser.add_argument('--filetype', default=None, help='file type for tools, use \',\' to split types')
parser.add_argument('--path', default='lidarpoint', help='File or folder path')
parser.add_argument('--save_fig', action='store_true',default=False, help='Save figure when plot tool called')
parser.add_argument('--nocopy', action='store_true',default=False, help='no copy option for some tools')
FLAGS = parser.parse_args()

pcdpath = FLAGS.path
switch = FLAGS.tool
save_fig=FLAGS.save_fig
types=FLAGS.filetype  #Will check if multiple types input
nocopy=FLAGS.nocopy

#Tools
def pcdReplaceline(f):
    """
    Get Lester's pcd file and convert it to normal txt file. Change suffix only.
    input: pcd file filename
    a pcd file has the following format
    line 1-11  : string descriptions
    line 12-?  : data, ?x4 matrix with columns splitted by 1 space ' '
    output: txt, ?x4 matrix splitted by ','. In the same folder as files to convert.
    
    """
    try:
        with open(f,'r') as f1:
            newfile=os.path.dirname(f)+'/'+f.split('/')[-1].split('.pcd')[0]+'.txt' # for '~/~.pcd' to '~/~.txt'
            lines=f1.readlines()
            with open(newfile,'a+') as g:
                for x in range(len(lines)-11):
                    line=lines[x+11].replace(' ',',')
                    g.writelines(line)
    except:
        print('Invalid file.')
    

def pcd2txt(path):
    """
    Get Lester's pcd file and convert it to normal txt file. Change suffix only.
    input: pcd file(ascii) folder path or filename(not for recursive convertion)
    a pcd file has the following format
    line 1-11  : string descriptions
    line 12-?  : data, ?x4 matrix with columns splitted by 1 space ' '
    input list
    path: single '*.pcd' file path
    output: txt, ?x4 matrix splitted by ','. In the same folder as files to convert.
    
    """
    try : 
        files=os.listdir(path)
        for f in glob.glob(os.path.join(base_path,path,'*.pcd')):
            pcdReplaceline(f)
    except :
        try:
            pcdReplaceline(path)
        except:
            print('Invalid pcd folder path or file name. ')


def plotfile(f,fig):
    try:
        data=np.loadtxt(f,delimiter=',')
    except:
        print('Invalid data. ')
        return -1
    
    mlab.points3d(data[:,0], data[:,1], data[:,2], data[:,2], color=None, mode='point',\
                  colormap = 'gnuplot', scale_factor=1, figure=fig)
    mlab.view(azimuth=240, elevation=0, focalpoint=[0, 0, 0], distance=30, figure=fig)
    if save_fig:
        mlab.savefig('%.jpg'%(f.split('/')[-1].split('.pcd')[0]), figure=fig)
    raw_input()
    mlab.clf()
    
def plot(path):
    """
    Plot pointcloud data.
    input list
    path:nx4 or nx3 pointcloud data, txt file
    
    """
    fig = mlab.figure(figure=None, bgcolor=(0,0,0), fgcolor=None, engine=None, size=(800, 600))
    try : 
        files=glob.glob(os.path.join(base_path,path,'*.txt'))
        if not files: 
            print('No files to plot.')
            mlab.close()
            return -1
        else:
            for f in files:
                plotfile(f,fig)
    except :
        try:
            plotfile(path,fig)
        except:
            print('Invalid pcd folder path or file name. ')
            
def rename06d(path,types,nocopy,newfolder='renamed') :
    '''
    rename06d: rename all pcdfiles named by time.abc to %06d.xyz
    input list
    path   : folder
    types  : input file type and output file type, default is 'txt,txt'
    output : renamed files in the folder 'renamed'
    
    '''
    abc,xyz=types.split(',')
    if not os.path.exists(os.path.join(path,newfolder)):    os.mkdir(os.path.join(path,newfolder))
    tmp=[]
    for namef in glob.glob(os.path.join(path,'*.%s'%abc)):
        tmp.append(namef.split('_as')[0].split('/')[-1])
    floatfiles=np.array(tmp).astype(np.float64)
    ind=floatfiles.argsort()
    for i in range(len(ind)):
        old=os.path.join(path,tmp[ind[i]]+'_ascii.%s'%abc)
        new=os.path.join(path,newfolder,'%06d'%i +'.%s'%xyz)
        os.rename(old,new) if nocopy else os.system('cp %s %s'%(old,new))
            
if __name__ == '__main__':
    if switch == 'pcd2txt':
        print('Current directory:  '+base_path+'\n'+'Current tool:  '+switch+'\n')
        pcd2txt(pcdpath)
    if switch == 'plot':
        print('Current directory:  '+base_path+'\n'+'Current tool:  '+switch+'\n')
        plot(pcdpath)
    if switch == 'rename06d':
        print('Current directory:  '+base_path+'\n'+'Current tool:  '+switch+'\n')
        rename06d(pcdpath,types,nocopy)
