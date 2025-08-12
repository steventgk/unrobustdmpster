import numpy as np
import pynbody as pb

class TipsySnap():
    def __init__(self, nstar, nDM, ngas, ndim=3, order='star,gas,dm',name='created',time=0.0):
        self.ndm = nDM
        self.nstar = nstar
        self.ngas = ngas
        self.ndim = ndim
        self.order = order
        self.name = name
        
    def newtipsy(self):
        newtipsy = pb.snapshot.new(dm=self.ndm, star=self.nstar,
                                   gas=self.ngas, ndim=self.ndim,
                                   order=self.order)
        newtipsy._filename = self.name

        write=[]
        for w, ndim in ("pos", 3), ("vel", 3), ("mass", 1):
            newtipsy._create_array(w, ndim, zeros=True)
            write.append(w)
        for w in "rho", "temp":
            newtipsy.gas._create_array(w, zeros=True)
            write.append(w)

        newtipsy.gas._create_array("metals", zeros=True)
        newtipsy.star._create_array("metals", zeros=True)
        write.append("metals")

        newtipsy.star._create_array("tform", zeros=True)
        write.append("tform")

        return newtipsy
    
def data_to_tipsysnap(stars, gas, dm, name='mytipsysnap', time=0.0):

    nm_star, nm_gas, nm_dm = len(stars), 1, 1
    newTS = TipsySnap(nm_star, nm_dm, nm_gas, name=name).newtipsy()
    newTS.properties['time'] = time

    #### Stars ##############################################################
    coords = np.column_stack([stars['x'],stars['y'],stars['z']])
    vcoords = np.column_stack([stars['vx'],stars['vy'],stars['vz']])
    newTS.star['pos'] = pb.array.SimArray(coords,'kpc')
    newTS.star['vel'] = pb.array.SimArray(vcoords,'km s**-1')
    newTS.star['mass'] = pb.array.SimArray(stars['m'], 'Msol') 

    return newTS


# set up the directory for the output images and input file
datdir = '/Users/victordebattista/Research/Publications/InProgress/moatwall/Models/Auriga/'

# read in the simulation
fn = 'halo_18_sim_data.npy'

# dtype=[('x', '<f4'), ('y', '<f4'), ('z', '<f4'), ('vx', '<f4'), ('vy', '<f4'), ('vz', '<f4'), ('m', '<f4')])
stars = np.load(datdir+fn)
print(stars.dtype)

# added fn[:-4] so you dont end up with a file called xyz.npy.tipsy
sim = data_to_tipsysnap(stars, None, None, name = datdir+fn[:-4]+'.tipsy')
pb.snapshot.tipsy.TipsySnap._write(sim,sim._filename,cosmological=False)