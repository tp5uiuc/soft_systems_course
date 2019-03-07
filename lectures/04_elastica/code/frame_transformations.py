
# coding: utf-8

# In[1]:


# All imports and setup code goes here
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns #If you have not installed seaborn uncomment this line
from mpl_toolkits.mplot3d import Axes3D, proj3d
from matplotlib.patches import FancyArrowPatch, Patch
import copy
sns.set_context("talk", font_scale=1.5, rc={"lines.linewidth": 2.5})
sns.set_style("whitegrid")
get_ipython().run_line_magic('matplotlib', 'inline')


# ## Frame transformations
# Frequently, in scientific applications (modeling, controls etc.), geometry and computer graphics/vision, we need to transform between a local frame (or local/object frame/coordinates, denoted by $ \mathbf{x}_\mathcal{L} $ ) and a laboratory frame (or global/world frame/coordinates, denoted by $\mathbf{x} $). Note that the local frame can be at a different location (or) have a different orientation with respect to the global frame coordinates. In this notebook, we will see different ways of achieving the same.

# In[3]:


class Arrow3D(FancyArrowPatch):
    """ An arrow in 3 dimensions, that renders according to the view
    set in the mpl global 3D frame
    """
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs
        self.update(xs, ys, zs)

    def __copy__(self):
        obj = type(self).__new__(self.__class__)
        obj.__dict__.update(self.__dict__)
        return obj

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)

    def update(self, xs, ys, zs):
        self._verts3d = xs, ys, zs


# In[4]:


class frame_3D(object):
    """ 3D frame class. Class for different rotation
    and translation strategies. Implementation is kept generic
    for OOP.
    
    Default alignment to the global axes
    """

    def __init__(self, t_origin, *args, **kwargs):
        """ Initialize members using an iterable
        """
        # Instantaneous data structures
        self.n_iter = -1
        self.origin = np.zeros(3,)
        self.frame_limits = np.eye(3)
        self.last_rot_axis = None
        self.color_dict = [{'color':'r'}, {'color':'g'}, {'color':'b'}] 
        self.axes = [None for i in np.arange(3)]

        # History
        self.origin_dict = {}
        self.frame_dict = {}
        self.axes_dict = {}
        
        # Origin has an update
        self.set_origin(t_origin)

        # Sets all initial properties
        self.__prepare_draw(*args, **kwargs)

        # To solve the origin problem. The dictionary is now numbered from
        # 1 to n. 
        self.n_iter += 1

    def __update_history(self):
        """ Stores history of the path in dicts
        
        Also updates old arrow properties
        """
        # Append to history data structures
        self.n_iter += 1
        self.origin_dict.update({self.n_iter : self.origin.copy()})
        self.frame_dict.update({self.n_iter: self.frame_limits.copy()})

        temp_axes = [None for i in np.arange(3)]
        # Can't list comprehend because of the damn copy thing
        for i in np.arange(3):
            # copy method on the entire list does not work because
            # deepcopy fails for mpl objects
            temp_axes[i] = copy.copy(self.axes[i])

            # Update linestyles and alphas for the old arrow3Ds
            temp_axes[i].set_linestyle('--')
            temp_axes[i].set_alpha(0.5)            
            
        # Finally update the axes dict with the new arrow3Ds
        self.axes_dict.update({self.n_iter: temp_axes})

        # Weight alphas exponentially with base of 0.5
        for iterno, iteraxis in self.axes_dict.items():
            for i in np.arange(3):
                iteraxis[i].set_alpha(0.5*np.exp(iterno-self.n_iter))
        
    def __refresh(self):
        """ For the current data, refresh the arrows 
        to later redraw the canvas
        """
        # Redraw canvas with the current data
        data3D = self.__prepare_data(self.origin, self.frame_limits)
        [self.axes[i].update(data3D[3*i], data3D[3*i+1], data3D[3*i+2]) for i in np.arange(3)]

    def __prepare_data(self, t_origin, t_frame_limits, *args, **kwargs):
        """ Prepare data to be draw on canvas """
        origin3D = t_origin.reshape(1, -1) - 0.0*t_origin.reshape(-1, 1)
        data3D = np.dstack((origin3D, origin3D + t_frame_limits))
        data3D = data3D.reshape(-1, 2)    
        return data3D
        
    def __prepare_draw(self, *args, **kwargs):
        """ Constructor-like class for drawing the first time on the canvas"""
        data3D = self.__prepare_data(self.origin, self.frame_limits)

        for i in np.arange(3):
            # Can't list comprehend because of this damn thing
            kwargs.update(self.color_dict[i])
            # Update axes now
            self.axes[i] = Arrow3D(data3D[3*i], data3D[3*i+1], data3D[3*i+2], *args, **kwargs)
 
    def clear(self):
        """ Clear histories """
        self.n_iter = 0
        self.origin_dict.clear()
        self.frame_dict.clear()
        self.axes_dict.clear()
        
    def set_origin(self, t_origin):
        t_origin = np.array(t_origin)
        if len(t_origin) == 3:
            if not np.allclose(self.origin, t_origin):
                # Update only if not first
                if self.n_iter + 1:
                    self.__update_history()
                self.origin = np.array(t_origin)
                self.last_rot_axis = None
                if self.n_iter + 1:
                    self.__refresh()
            else:
                from warnings import warn
                warn("Origin retained because the new origin is the same as the old origin")
        else:
            raise RuntimeError("Cannot initialize frame3D object with more than 3 coordinates")

    def process_origin(self, func, *func_args, **func_kwargs):
        """ Takes in a function, and optional arguments
        and makes it act on the origin 
        """
        try:
            tmp = func(self.origin, *func_args, **func_kwargs)
        except:
            raise RuntimeError("Could not process function!")
            return 1
        self.__update_history()
        self.origin = tmp
        self.last_rot_axis = None
        self.__refresh()    

    def process_frames(self, func, *func_args, **func_kwargs):
        """ Takes in a function, and optional arguments
        and makes it act on the frames 
        """
        try:
            tmp_frame, tmp_rot_axis = func(self.frame_limits, *func_args, **func_kwargs)
        except:
            raise RuntimeError("Could not process function!")
            return 1
        self.__update_history()
        self.frame_limits = tmp_frame
        self.last_rot_axis = tmp_rot_axis
        self.__refresh()            
       
    def draw(self, renderer):
        """Draws axis on a given canvas"""
        # Clear the renderer first
        renderer.clear()
        
        # Draws the current arrows
        [renderer.add_artist(ax) for ax in self.axes]

        # Draws the current rotation axis, if not None
        if np.any(self.last_rot_axis):
            neg_tmp = self.origin - self.last_rot_axis
            pos_tmp = self.origin + self.last_rot_axis
            renderer.plot([neg_tmp[0], pos_tmp[0]],[neg_tmp[1], pos_tmp[1]],[neg_tmp[2], pos_tmp[2]], 'k.-', alpha=0.2)
        
        # Draws all the previous frames, but with different arrow styles
        for _, vals in self.axes_dict.items():
            [renderer.add_artist(ax) for ax in vals]
        
        # Draws the current origin
        renderer.scatter(self.origin[0], self.origin[1], self.origin[2], s=30, c='k')
        renderer.text(self.origin[0]-0.4, self.origin[1]-0.4, self.origin[2]-0.4, "{}".format(self.n_iter + 1), size=20)

#         # Draws all the previous origins, but with some transparenct and connecting lines
#         for key, vals in self.origin_dict.items():
#             renderer.scatter(vals[0], vals[1], vals[2], s=30, c='k', alpha=0.5)
#             renderer.text(vals[0]-0.4, vals[1]-0.4, vals[2]-0.4, "{}".format(key), size=20)
#             renderer.plot([tmp[0], vals[0]],[tmp[1], vals[1]], [tmp[2], vals[2]], 'k--')

        # Draws all the previous origins, but with some transparency and connecting lines
        tmp = self.origin
        min_dist = np.min(tmp)
        max_dist = np.max(tmp)
        # Do it this way to also draw the lines connecting them
        # The above way is more efficient, but if we need to iterate in reverse,
        # we lose more time.
        for key in np.arange(self.n_iter, 0, -1):
            vals = self.origin_dict[key]
            renderer.scatter(vals[0], vals[1], vals[2], s=30, c='k', alpha=0.5)
            renderer.text(vals[0]-0.4, vals[1]-0.4, vals[2]-0.4, "{}".format(key), size=20)
            renderer.plot([tmp[0], vals[0]],[tmp[1], vals[1]], [tmp[2], vals[2]], 'k--', alpha=0.3)
            tmp = vals
            min_dist = min(min_dist, np.min(vals))
            max_dist = max(max_dist, np.max(vals))
            
        # Put it in another class maybe?
        extension = 1.0
        renderer.set_xlim(min(0.0, min_dist) - extension, max(0.0, max_dist) + extension)
        renderer.set_ylim(min(0.0, min_dist) - extension, max(0.0, max_dist) + extension)
        renderer.set_zlim(min(0.0, min_dist) - extension, max(0.0, max_dist) + extension)
        renderer.set_xlabel(r'$x$')
        renderer.set_ylabel(r'$y$')
        renderer.set_zlabel(r'$z$') 
        renderer.set_aspect('equal')


# In[5]:


# produce figure
fig = plt.figure(figsize=(5,5), dpi=200)
ax = fig.add_subplot(111, projection='3d')

# define origin
o = np.array([0,0,0])

a = frame_3D([0.0, 0.0, 0.0], mutation_scale=20, arrowstyle='-|>')
a.draw(ax)


# In[6]:


a.set_origin([0.0, 1.0, 2.0])
a.draw(ax)
fig


# In[ ]:


def set_and_display(t_frame, t_arg):
    t_frame.set_origin(t_arg)
    t_frame.draw(ax)


# In[ ]:


set_and_display(a, [0.0, 2.0 ,3.0])
print(a.n_iter)
fig


# ## Frame translation
# The first serious attempt at describing a frame with only displacements to the origin of the frame is translation. This is given by the following formula 
# 
# $$ \mathbf{x}_\mathcal{L} = \mathbf{x} + \mathbf{t} $$
# 
# Here $ \mathbf{t} $ is the notation for the translation vector. We show an example of this below.

# In[8]:


def translate(t_o, t_t):
    """Translates to different location"""
    t_t = np.array(t_t)
    if not (np.linalg.norm(t_t, 2) < 1e-6):
        return t_o + t_t
    else:
        raise RuntimeError("Not translating because the translation should not be infinitesimal")


# In[9]:


a.process_origin(translate, [3.0, 0.0, 0.0])
a.draw(ax)
fig


# In[ ]:


def rotate_about_axis(t_frame, t_angle, about='x', rad=False):
    """Rotates about one of the base axes"""

    # Throw error if it does not make sense
    if about.lower() not in ['x','y','z']:
        raise NotImplementedError("Not one of x,y,z!")
    
    # Check if its in radian or degree
    # Default assumed to be degree
    if not rad:
        t_angle = np.deg2rad(t_angle)

    # Form the 2D rotation matrix
    c_angle = np.cos(t_angle)
    s_angle = np.sin(t_angle)
    cs_matrix = np.array([[c_angle, s_angle],[-s_angle, c_angle]])
    # For y it is different
    cs_matrix = cs_matrix.T if about.lower()=='y' else cs_matrix

    # DS for 3D Euler rotation matrix
    # Composed of 2D matrices
    rot_matrix = np.eye(3)
    tmp = rot_matrix.copy()
    
#     if about.lower() == 'x':
#         start_id = 1
#         end_id = 3
#         skip_id = 1
#     elif about.lower() == 'y':
#         start_id = 0
#         end_id = 3
#         skip_id = 2             
#     elif about.lower() == 'z':
#         start_id = 0
#         end_id = 2
#         skip_id = 1        

    # Form slicing indices
    start_id = 1 if about.lower()=='x' else 0
    stop_id = 2 if about.lower()=='z' else 3
    skip_id = 2 if about.lower()=='y' else 1
    idxy = slice(start_id, stop_id, skip_id)

    # Finally form the matrix
    rot_matrix[idxy, idxy] = cs_matrix

    if not (np.allclose(rot_matrix, tmp)):
        # actually do the rotation
        # The last argument returns the row. But the code is obfuscated as hell
        # just because
        return rot_matrix @ t_frame, tmp[ord(about.lower())-ord('x')]
    else:
        raise RuntimeError("Not rotating because rotation is identity")


# In[ ]:


a = frame_3D([0.0, 0.0, 0.0], mutation_scale=20, arrowstyle='-|>')
a.process_origin(translate, [1.0, 0.0, 0.0])
a.process_frames(rotate_about_axis, 45.0, about='z', rad=False)
a.draw(ax)
fig


# In[ ]:


a.process_origin(translate, [1.0, 0.0, 0.0])
a.process_frames(rotate_about_axis, 45.0, about='z', rad=False)
a.draw(ax)
fig


# In[ ]:


def rotate_rodrigues(t_frame, t_angle, about=[0.0,0.0,1.0], rad=False):
    """Translates to different location"""

    # Check if its in radian or degree
    # Default assumed to be degree
    if not rad:
        t_angle = np.deg2rad(t_angle)
        
    def normalize(v):
        """ Normalize a vector/ matrix """
        norm = np.linalg.norm(v)
        if np.isclose(norm, 0.0):
            raise RuntimeError("Not rotating because axis specified to be zero")
            return v
        return v / norm

    def skew_symmetrize(v):
        """ Generate an orthogonal matrix from vector elements"""
        # Hard coded. Others are more verbose or not worth it
        return np.array([[0.0,-v[2],v[1]],
                         [v[2],0.0,-v[0]],
                         [-v[1],v[0],0.0]])
        
        
    # Convert about to np.array and normalize it
    about = normalize(np.array(about))

    # Form the 2D Euler rotation matrix
    c_angle = np.cos(t_angle)
    s_angle = np.sin(t_angle)

    # DS for 3D Euler rotation matrix
    # Composed of 2D matrices
    tmp = np.eye(3)
    U_mat = skew_symmetrize(about)
    rot_matrix = tmp + U_mat @ (s_angle * tmp + (1-c_angle)* U_mat)
    print(rot_matrix, U_mat)
    
    if not (np.allclose(rot_matrix, tmp)):
        # actually do the rotation
        return rot_matrix @ t_frame, about
    else:
        raise RuntimeError("Not rotating because rotation is identity")


# In[ ]:


a = frame_3D([0.0, 0.0, 0.0], mutation_scale=20, arrowstyle='-|>')
a.process_origin(translate, [1.0, 0.0, 0.0])
a.process_frames(rotate_rodrigues, 45.0, about=[0.0, 0.0, -1.0], rad=False)
a.draw(ax)
fig

