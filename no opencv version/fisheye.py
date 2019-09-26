import numpy as np


# input mat, radio of fisheye circle, the distance of input plane and output plane, output image expand pixel range
def undistort2(mat, r_, L, expand_r=0, expand_c=0):

    assert(r_ >= L)
    hgt, wid = mat.shape

    hgt_res = hgt + expand_r * 2
    wid_res = wid + expand_c * 2

    # input mat center
    ccol = (wid - 1) / 2.0
    crow = (hgt - 1) / 2.0

    # output center
    ccol_res = (wid_res - 1) / 2.0
    crow_res = (hgt_res - 1) / 2.0

    res = np.zeros((hgt_res, wid_res))

    # iterate eveey pixels on output plane
    for r in range(hgt_res):
        # convert to polar coordinates
        y = r - crow_res
        for c in range(wid_res):
	    # convert to polar coordinates
            x = c - ccol_res
            # calculate corresponding coordinate
            phi = math.atan2(y, x)
            R = get_dst_p2p([r, c], [crow_res, ccol_res])
            dst = (R**2 * r_**2 / (R**2 + L**2))**0.5
            v = dst * math.sin(phi)
            u = dst * math.cos(phi)
            # conver to cartesian coordinates
            v += crow
            u += ccol
            # linear interpolation
            v = int(round(v))
            u = int(round(u))

            if v >= 0 and v < hgt and u >= 0 and u < wid:
                res[r][c] = mat[v, u]

    return res


# optimize speed with matrix
def undistort3(mat, r_, L, expand_r=0, expand_c=0):
    assert (r_ >= L)
    hgt, wid = mat.shape
    hgt_res = hgt + expand_r * 2
    wid_res = wid + expand_c * 2

    # input mat center
    ccol = (wid - 1) / 2.0
    crow = (hgt - 1) / 2.0

    # output center
    ccol_res = (wid_res - 1) / 2.0
    crow_res = (hgt_res - 1) / 2.0

    # phi
    y, x = np.mgrid[:hgt_res, :wid_res]
    y = y - crow_res
    x = x - ccol_res
    phi = np.arctan2(y, x)

    # dst
    y, x = np.ogrid[:hgt_res, :wid_res]
    dst = ((y - crow_res)**2 + (x - ccol_res)**2)**0.5
    dst = (dst**2 * r_**2 / (dst**2 + L**2))**0.5

    v = (dst * np.sin(phi) + crow).astype(int)
    u = (dst * np.cos(phi) + ccol).astype(int)

    # in case out of boundary
    v[v < 0] = 0
    v[v >= hgt] = hgt - 1
    u[u < 0] = 0
    u[u >= wid] = wid - 1

    res = np.zeros((hgt_res, wid_res))
    res[:][:] = mat[v[:][:], u[:][:]]

    return res