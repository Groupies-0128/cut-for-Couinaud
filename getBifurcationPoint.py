import SimpleITK as sitk
import cv2
import numpy as np

# ===========================================
# Input: nrrd, which have been single_voxeled.
#
# Output: The coordination of three kinds of points.
# ===========================================

blackpoint_list = list()

def neighborhood_6(p):
    temp = list()
    temp.append([p[0] - 1, p[1], p[2]])
    temp.append([p[0] + 1, p[1], p[2]])
    temp.append([p[0], p[1] - 1, p[2]])
    temp.append([p[0], p[1] + 1, p[2]])
    temp.append([p[0], p[1], p[2] - 1])
    temp.append([p[0], p[1], p[2] + 1])

    return temp


def neighborhood_18(p):
    temp = list()
    temp.append([p[0] + 1, p[1], p[2] + 1])
    temp.append([p[0] + 1, p[1] + 1, p[2]])
    temp.append([p[0] + 1, p[1], p[2] - 1])
    temp.append([p[0] + 1, p[1] - 1, p[2]])
    temp.append([p[0] + 1, p[1], p[2]])
    temp.append([p[0], p[1], p[2] + 1])
    temp.append([p[0], p[1] + 1, p[2] + 1])
    temp.append([p[0], p[1] + 1, p[2]])
    temp.append([p[0], p[1] + 1, p[2] - 1])
    temp.append([p[0], p[1], p[2] - 1])
    temp.append([p[0], p[1] - 1, p[2] - 1])
    temp.append([p[0], p[1] - 1, p[2]])
    temp.append([p[0], p[1] - 1, p[2] + 1])
    temp.append([p[0] - 1, p[1], p[2] + 1])
    temp.append([p[0] - 1, p[1] + 1, p[2]])
    temp.append([p[0] - 1, p[1], p[2] - 1])
    temp.append([p[0] - 1, p[1] - 1, p[2]])
    temp.append([p[0] - 1, p[1], p[2]])

    return temp


def neighborhood_26(p):
    temp = list()
    temp.append([p[0] + 1, p[1], p[2] + 1])
    temp.append([p[0] + 1, p[1] + 1, p[2] + 1])
    temp.append([p[0] + 1, p[1] + 1, p[2]])
    temp.append([p[0] + 1, p[1] + 1, p[2] - 1])
    temp.append([p[0] + 1, p[1], p[2] - 1])
    temp.append([p[0] + 1, p[1] - 1, p[2] - 1])
    temp.append([p[0] + 1, p[1] - 1, p[2]])
    temp.append([p[0] + 1, p[1] - 1, p[2] + 1])
    temp.append([p[0] + 1, p[1], p[2]])
    temp.append([p[0], p[1], p[2] + 1])
    temp.append([p[0], p[1] + 1, p[2] + 1])
    temp.append([p[0], p[1] + 1, p[2]])
    temp.append([p[0], p[1] + 1, p[2] - 1])
    temp.append([p[0], p[1], p[2] - 1])
    temp.append([p[0], p[1] - 1, p[2] - 1])
    temp.append([p[0], p[1] - 1, p[2]])
    temp.append([p[0], p[1] - 1, p[2] + 1])
    temp.append([p[0] - 1, p[1], p[2] + 1])
    temp.append([p[0] - 1, p[1] + 1, p[2] + 1])
    temp.append([p[0] - 1, p[1] + 1, p[2]])
    temp.append([p[0] - 1, p[1] + 1, p[2] - 1])
    temp.append([p[0] - 1, p[1], p[2] - 1])
    temp.append([p[0] - 1, p[1] - 1, p[2] - 1])
    temp.append([p[0] - 1, p[1] - 1, p[2]])
    temp.append([p[0] - 1, p[1] - 1, p[2] + 1])
    temp.append([p[0] - 1, p[1], p[2]])

    return temp


def neighborhood_18except6(p):
    temp = list()
    temp.append([p[0] + 1, p[1], p[2] + 1])
    temp.append([p[0] + 1, p[1] + 1, p[2]])
    temp.append([p[0] + 1, p[1], p[2] - 1])
    temp.append([p[0] + 1, p[1] - 1, p[2]])
    temp.append([p[0], p[1] + 1, p[2] + 1])
    temp.append([p[0], p[1] + 1, p[2] - 1])
    temp.append([p[0], p[1] - 1, p[2] - 1])
    temp.append([p[0], p[1] - 1, p[2] + 1])
    temp.append([p[0] - 1, p[1], p[2] + 1])
    temp.append([p[0] - 1, p[1] + 1, p[2]])
    temp.append([p[0] - 1, p[1], p[2] - 1])
    temp.append([p[0] - 1, p[1] - 1, p[2]])

    return temp


def neighborhood_26except18(p):
    temp = list()
    temp.append([p[0] + 1, p[1] + 1, p[2] + 1])
    temp.append([p[0] + 1, p[1] + 1, p[2] - 1])
    temp.append([p[0] + 1, p[1] - 1, p[2] - 1])
    temp.append([p[0] + 1, p[1] - 1, p[2] + 1])
    temp.append([p[0] - 1, p[1] + 1, p[2] + 1])
    temp.append([p[0] - 1, p[1] + 1, p[2] - 1])
    temp.append([p[0] - 1, p[1] - 1, p[2] - 1])
    temp.append([p[0] - 1, p[1] - 1, p[2] + 1])

    return temp


def get_blackpoint(array):
    xx, yy, zz = np.where(array == 1)
    for i in range(len(xx)):
        blackpoint_list.append([xx[i], yy[i], zz[i]])

    return blackpoint_list


def condition(blackpoint_list, array):

    end_point = list()
    normal_point = list()
    bifurcation_point = list()
    print(len(blackpoint_list))

    for p in blackpoint_list:

        counter = 0
        x = list()              # The list contains the points which are black in range.
        x_18 = list()
        p_18except6 = list()
        p_26except18 = list()
        condition1_1 = True
        condition1_2 = True

        for i in neighborhood_6(p):
            if array[i[0]][i[1]][i[2]] == 1:
                x.append([i[0], i[1], i[2]])            # Get the black points x in 6-neighborhood of p.

        for i in x:
            for j in neighborhood_18(i):
                if array[j[0]][j[1]][j[2]] == 1:
                    x_18.append([j[0], j[1], j[2]])
            for j in neighborhood_18except6(p):
                if array[j[0]][j[1]][j[2]] == 1:
                    p_18except6.append([j[0], j[1], j[2]])
            for j in neighborhood_26except18(p):
                if array[j[0]][j[1]][j[2]] == 1:
                    p_26except18.append([j[0], j[1], j[2]])

            flag1 = False
            flag2 = False
            for j in x_18:
                for k in p_18except6:
                    if j == k:
                        flag1 = True
                        break
                if flag1:
                    condition1_1 = False
                    break
            for j in x_18:
                for k in p_26except18:
                    if j == k:
                        flag2 = True
                        break
                if flag2:
                    condition1_2 = False
                    break

            if condition1_1 and condition1_2:
                counter = counter + 1                   # condition 1
        # print(counter)

        x = list()
        x_6 = list()
        p_26except18 = list()
        for i in neighborhood_18except6(p):
            if array[i[0]][i[1]][i[2]] == 1:
                x.append([i[0], i[1], i[2]])            # Get the black points x in 18(except6)-neighborhood of p.

        for i in x:
            for j in neighborhood_6(i):
                if array[j[0]][j[1]][j[2]] == 1:
                    x_6.append([j[0], j[1], j[2]])
            for j in neighborhood_26except18(p):
                if array[j[0]][j[1]][j[2]] == 1:
                    p_26except18.append([j[0], j[1], j[2]])

            flag = False
            for j in x_6:
                for k in p_26except18:
                    if j == k:
                        flag = True
                        break
                if flag:
                    break
            if not flag:
                counter = counter + 1                   # condition 2
        # print(counter)

        x = list()
        for i in neighborhood_26except18(p):
            if array[i[0]][i[1]][i[2]] == 1:
                x.append([i[0], i[1], i[2]])            # Get the black points x in 26(except18)-neighborhood of p.

        for i in x:
            counter = counter + 1                       # condition 3

        # print(counter)

        if counter == 1:
            end_point.append(p)
        if counter == 2:
            normal_point.append(p)
        if counter > 2:
            bifurcation_point.append(p)

    print(len(end_point), 'end points: ', end_point)
    print(len(normal_point), 'normal points: ', normal_point)
    print(len(bifurcation_point), 'bifurcation points: ', bifurcation_point)

    # print('---------------------')


if __name__ == '__main__':
    path = input()
    itk_img = sitk.ReadImage(path)
    itk_arr = sitk.GetArrayFromImage(itk_img)

    condition(get_blackpoint(itk_arr), itk_arr)
