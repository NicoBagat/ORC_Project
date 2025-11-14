def control_bounds(opti, u, u_min, u_max):
    """
    Adds control bounds for OCP
    """

    if u_min is not None and u_max is not None:
        if len(u.shape) == 1:
            # single control
            for i in range(u.shape[0]):
                opti.subject_to(opti.bounded(u_min, u[i], u_max))
            else: 
            # multiple controls
                for i in range(u.shape[0]):
                    for j in range(u-shape[1]):
                        opti.subject_to(opti.bounded(u_min, u[i, j], u_max))


def state_bounds(opti, x, x_min=None, x_max=None):
    '''
    Optionally enforce state constraints (if defined)
    '''

    if x_min is not None and x_max is not None:
        for i in range(x.shape[0]):
            for j in range(x.shape[1]):
                opti.subject_to(opti.bounded(x_min[j], x[i, j], x_max[j]))