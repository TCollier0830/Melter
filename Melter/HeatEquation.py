import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
import matplotlib.animation as animation
from skimage import data, color, io
from skimage.transform import rescale, resize, downscale_local_mean
from matplotlib import rcParams
rcParams['animation.ffmpeg_path'] = r'C:\Users\travi\FFmpeg\bin\ffmpeg.exe'


InitialDistribution = io.imread("Oval.png", as_gray=True)

#InitialDistribution = Image.open("export.png", gray=True)
w = h = 10.
dx = dy = 0.1
#InitialDistribution.thumbnail((int(w/dx),int(h/dy)))
InitialDistribution = resize(InitialDistribution, (int(w/dx),int(h/dy)), anti_aliasing=True)

#InitialDistribution.save('smiley.png')
np_im = np.array(InitialDistribution)

K = 0.07 #Gold
Tcool, Thot = 300, 700
nx, ny = int(w/dx), int(h/dy)
dx2, dy2 = dx*dx, dy*dy
dt = dx2 * dy2 / (2 * K * (dx2 + dy2))
u0 = Tcool * np.ones((nx, ny))
u = np.empty((nx, ny))

#Initial conditions
for i in range(nx):
    for j in range(ny):
        u0[i,j] = np_im[i][j]*Thot

def do_timestep(u0, u):
    #This part isn't really my own doing, the standard lib does this but I didn't want to import.
    u[1:-1, 1:-1] = u0[1:-1, 1:-1] + K * dt * (
          (u0[2:, 1:-1] - 2*u0[1:-1, 1:-1] + u0[:-2, 1:-1])/dx2
          + (u0[1:-1, 2:] - 2*u0[1:-1, 1:-1] + u0[1:-1, :-2])/dy2 )

    u0 = u.copy()
    return u0, u

# Number of timesteps
nsteps = 300
TimeSolution = []
fig = plt.figure()
plt.style.use("dark_background")
for m in range(nsteps):
    u0, u = do_timestep(u0, u)
    ttl = plt.text(10, -2, "TIME: " + str(m*dt*1000) + ' ms', horizontalalignment='center', verticalalignment='bottom')
    im = plt.imshow(u, cmap=plt.get_cmap('hot'), vmin=0,vmax=Thot, animated=True) 
    TimeSolution.append([im, ttl])

ani = ArtistAnimation(fig, TimeSolution, interval=100, blit=True)
Writer = animation.writers['ffmpeg']

writer = Writer(fps=60, metadata=dict(artist='Me'), bitrate=1800)
fig.colorbar(im)
ani.save('Alcoholic_Oval.mp4',writer = writer)