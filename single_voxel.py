import numpy
import SimpleITK as sitk
# ==============================================================================


T = numpy.array([[[1, 0, 0],
                  [0, 0, 0],
                  [0, 0, 0]],

                 [[0, 1, 1],
                  [0, 1, 0],
                  [0, 0, 0]],

                 [[0, 0, 0],
                  [0, 0, 1],
                  [0, 0, 0]]])

T_distanceError = numpy.array([[[1, 0, 0],
                  [1, 1, 1],
                  [1, 1, 1]],

                 [[0, 0, 1],
                  [1, 1, 1],
                  [0, 0, 1]],

                 [[1, 0, 0],
                  [0, 0, 1],
                  [1, 0, 0]]])


T_positionError1 = numpy.array([[[1, 0, 1],
                  [1, 0, 1],
                  [1, 0, 1]],

                 [[1, 0, 1],
                  [1, 0, 1],
                  [1, 0, 1]],

                 [[1, 0, 1],
                  [1, 0, 1],
                  [1, 0, 1]]])


T_positionError2 = numpy.array([[[0, 0, 0],
                  [0, 0, 0],
                  [0, 0, 0]],

                 [[0, 0, 0],
                  [0, 0, 0],
                  [0, 0, 0]],

                 [[0, 0, 0],
                  [0, 0, 0],
                  [0, 0, 0]]])


def Edis_3D(x1, y1, z1, x2, y2, z2):
    distance = numpy.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)
    return distance


def _build_mask():
    M1 = numpy.array([[['a', 'a', 'a'],
                       ['.', '.', '.'],
                       ['.', '.', '.']],

                      [['b', 'b', 'b'],
                       ['.', 'p', '.'],
                       ['.', '.', '.']],

                      [['.', '.', '.'],
                       ['d', 'd', 'd'],
                       ['e', 'e', 'e']]])

    M2 = numpy.array([[['.', '.', '.'],
                       ['.', '.', '.'],
                       ['.', '.', '.']],

                      [['b', 'b', 'b'],
                       ['.', 'p', '.'],
                       ['f', 'f', 'f']],

                      [['c', 'c', 'c'],
                       ['d', 'd', 'd'],
                       ['e', 'e', 'e']]])

    M3 = numpy.array([[['.', '.', '.'],
                       ['.', '.', '.'],
                       ['.', '.', '.']],

                      [['.', '.', '.'],
                       ['.', 'p', '.'],
                       ['.', '.', '.']],

                      [['c', 'c', 'c'],
                       ['d', 'd', 'd'],
                       ['e', 'e', 'e']]])

    NW = [M1, M2, M3]            # upside

    NE = list()
    ES = list()
    SW = list()
    UN = list()
    UE = list()
    US = list()
    UW = list()
    ND = list()
    ED = list()
    SD = list()
    WD = list()
    directions = list()

    for M in NW:
        tmp = M

        NE.append(numpy.rot90(tmp))

        ES.append(numpy.rot90(tmp, 2))

        SW.append(numpy.rot90(tmp, 3))          # four directions

    for M in NW:
        tmp = numpy.zeros_like(M)
        tmp[0, :, :] = numpy.rot90(M[0, :, :], 1)
        tmp[1, :, :] = numpy.rot90(M[1, :, :], 1)
        tmp[2, :, :] = numpy.rot90(M[2, :, :], 1)

        ND.append(tmp)
        ED.append(numpy.rot90(tmp))
        SD.append(numpy.rot90(tmp, 2))
        WD.append(numpy.rot90(tmp, 3))

    for M in NW:
        tmp = numpy.zeros_like(M)
        tmp[0, :, :] = numpy.rot90(M[0, :, :], 3)
        tmp[1, :, :] = numpy.rot90(M[1, :, :], 3)
        tmp[2, :, :] = numpy.rot90(M[2, :, :], 3)

        UN.append(tmp)
        UE.append(numpy.rot90(tmp))
        US.append(numpy.rot90(tmp, 2))
        UW.append(numpy.rot90(tmp, 3))

    directions.append(NW)
    directions.append(NE)
    directions.append(ES)
    directions.append(SW)
    directions.append(ND)
    directions.append(ED)
    directions.append(SD)
    directions.append(WD)
    directions.append(UN)
    directions.append(UE)
    directions.append(US)
    directions.append(UW)            # get all templates: 1.direction; 2.template; 3.surface; 4.line; 5.point

    return directions


def position(T, M, letter):           # char
    temp = []
    for i in range(3):
        for j in range(3):
            for k in range(3):
                if M[i][j][k] == letter and T[i][j][k] == 1:
                    temp.append([i, j, k])

    if len(temp) == 0:
        return False
    elif len(temp) == 2 and Edis_3D(temp[0][0], temp[0][1], temp[0][2], temp[1][0], temp[1][1], temp[1][2]) == 2:
        return False
    else:
        return True


def distance(M, T, letter1, letter2, dis):

    flag = False
    letter1_list = list()
    letter2_list = list()

    for i in range(3):
        for j in range(3):
            for k in range(3):
                if M[i][j][k] == letter1 and T[i][j][k] == 1:
                    letter1_list.append([i, j, k])
                if M[i][j][k] == letter2 and T[i][j][k] == 1:
                    letter2_list.append([i, j, k])

    for i in range(len(letter1_list)):
        for j in range(len(letter2_list)):
            if Edis_3D(letter1_list[i][0], letter1_list[i][1], letter1_list[i][2], letter2_list[j][0], letter2_list[j][1], letter2_list[j][2]) < dis:
                flag = True
                break
        if flag:
            break
    return flag


def condition1(T, directions):          # 1.at least 1 point;  2.be neighbourhood
    flag = False

    # print('condition1: ')
    for i in range(len(directions)):
        for j in range(3):
            if j == 0 and position(T, directions[i][j], 'a') and position(T, directions[i][j], 'b') and position(T, directions[i][j], 'd') and position(T, directions[i][j], 'e'):
                # print('template no: ', [i, j])
                flag = True
                break
            if j == 1 and position(T, directions[i][j], 'b') and position(T, directions[i][j], 'c') and position(T, directions[i][j], 'd') and position(T, directions[i][j], 'e') and position(T, directions[i][j], 'f'):
                # print('template no: ', [i, j])
                flag = True
                break
            if j == 2 and position(T, directions[i][j], 'c') and position(T, directions[i][j], 'd') and position(T, directions[i][j], 'e'):
                # print('template no: ', [i, j])
                flag = True
                break
    return flag


def condition2(T, directions):          # 1.at least 1 point;  2.be neighbourhood
    flag = False

    # print('condition2: ')
    for i in range(len(directions)):
        for j in range(3):
            if j == 0 and distance(directions[i][j], T, 'a', 'b', 1.5) and distance(directions[i][j], T, 'b', 'd', 1.8) and distance(directions[i][j], T, 'd', 'e', 1.5):
                # print('template no: ', [i, j])
                flag = True
            if j == 1 and distance(directions[i][j], T, 'b', 'c', 1.5) and distance(directions[i][j], T, 'c', 'd', 1.8) and distance(directions[i][j], T, 'd', 'e', 1.5) and distance(directions[i][j], T, 'e', 'f', 1.5):
                # print('template no: ', [i, j])
                flag = True
            if j == 2 and distance(directions[i][j], T, 'c', 'd', 1.5) and distance(directions[i][j], T, 'd', 'e', 1.5):
                # print('template no: ', [i, j])
                flag = True
    return flag


def condition(T, directions):
    if condition1(T, directions) and condition2(T, directions):
        return True
    else:
        return False


def judgement(T, directions):
    tmp = numpy.zeros_like(T)
    xx, yy, zz = numpy.where(T == 1)
    for i in range(len(xx)):
        x, y, z = xx[i], yy[i], zz[i]
        block = T[x - 1:x + 2, y - 1:y + 2, z - 1:z + 2]

        if condition(block, directions):
            tmp[x, y, z] = 1

    return T - tmp


def skeletonize_thinning(img):
    """ A 3D 6-subiteration thinning algorithm for extracting medial lines
    of Kalman Palagyi and Attila Kuba implementation
    Parameters
    ----------
    img : ndarray, 3D
    Returns
    -------
    skeleton : ndarray
        The thinned image.
    """

    mat_len_x, mat_len_y, mat_len_z = img.shape
    mat_tmp = numpy.zeros((mat_len_x + 2, mat_len_y + 2, mat_len_z + 2),
                          dtype=int)                                        # patch 2 pixels
    mat_tmp[1:-1, 1:-1, 1:-1] = img.astype(int)         # convert to int

    directions = _build_mask()                    # templates in different directions

    # ==========================================================================

    # print('number of voxels: ', numpy.count_nonzero(mat_tmp))

    iter = 0
    while True:
        print('iter: ', iter)

        iter += 1
        nb1 = numpy.count_nonzero(mat_tmp)              # count the number of the elements which aren't zero
        mat_tmp = judgement(mat_tmp, directions)

        nb2 = numpy.count_nonzero(mat_tmp)
        if nb1 == nb2:
            # print('remain voxels: ', nb1)
            break

    # ==========================================================================

    return mat_tmp[1:-1, 1:-1, 1:-1]


def get_difference(path1, path2):
    itk_img1 = sitk.ReadImage(path1)
    itk_img2 = sitk.ReadImage(path2)

    itk_arr1 = sitk.GetArrayFromImage(itk_img1)
    itk_arr2 = sitk.GetArrayFromImage(itk_img2)

    arr1_list = list()
    arr2_list = list()

    for i1 in range(len(itk_arr1)):
        for j1 in range(512):
            for k1 in range(512):
                if itk_arr1[i1][j1][k1]:
                    arr1_list.append([i1, j1, k1])
    print('before: ', len(arr1_list))

    for i2 in range(len(itk_arr1)):
        for j2 in range(512):
            for k2 in range(512):
                if itk_arr2[i2][j2][k2]:
                    arr2_list.append([i2, j2, k2])
    print('after: ', len(arr2_list))

    delete_point = list()
    for i in arr1_list:
        flag = False
        for j in arr2_list:
            if i != j:
                continue
            else:
                flag = True
                break
        if not flag:
            delete_point.append(i)

    print('delete ' + str(len(delete_point)) + ' points: ', delete_point)


if __name__ == '__main__':
    directions = _build_mask()

    in_path = 'data_023_portal_vein_12thin.nrrd'
    out_path = 'data_023_portal_vein_12thin_single.nrrd'
    image = sitk.ReadImage(in_path)
    image_arr = sitk.GetArrayFromImage(image)
    img_arr = skeletonize_thinning(image_arr)
    img_arr = img_arr
    img = sitk.GetImageFromArray(img_arr)
    sitk.WriteImage(img, out_path)
    get_difference('data_023_portal_vein_12thin.nrrd', 'data_023_portal_vein_12thin_single.nrrd')
