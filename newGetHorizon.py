import SimpleITK as sitk
import cv2
import numpy as np
import os
import prettytable as pt


slice_num = 0
slice_information = []
total_vessel_num = -1
KERNEL_SIZE = 6
x_boundary = 0
slice_no = 0
# start_slice_list = []
# end_slice_list = []
# total_tumor_size_list = []
# tumor_no_size_per_slice_list = []


def erode(case_no, kernel_size):
    itk_img = sitk.ReadImage('C:/Users/lrz/Desktop/DongBeiDaXue2/DongBeiDaXue2/portal_vein/data2_' + case_no + '_portal_vein_label.mha')
    bm = sitk.BinaryErodeImageFilter()
    bm.SetKernelType(sitk.sitkBall)
    bm.SetKernelRadius(kernel_size)
    bm.SetForegroundValue(1)
    itk_img = bm.Execute(itk_img)
    return itk_img


# def mha2jpg(case_no):
#     path = 'C:/Users/lrz/Desktop/jpg_label'
#     os.mkdir(path + '/' + case_no)
#     slices = sitk.ReadImage('C:/Users/lrz/Desktop/mha_label/data2_' + case_no + '_lesion_label.mha')
#     slices_data = sitk.GetArrayFromImage(slices)
#     for i in range(len(slices_data)):
#         slices_data[i] *= 255
#         cv2.imwrite('C:/Users/lrz/Desktop/jpg_label/' + case_no + '/' + str(i) + '.jpg', slices_data[i])
#     print(len(slices_data))


'''
获取切片的信息，格式为三维：
第一维：每张切片
第二维：每个肿瘤
第三维：肿瘤信息：[所在切片（可删），该切片第n个肿瘤，肿瘤序号，定位信息]
'''


def collect_tumor_information(itk_img):   # Path
    global slice_information
    global slice_num
    vessel_array = sitk.GetArrayFromImage(itk_img)
    slice_num = len(vessel_array)
    for slice_no in range(slice_num):
        contours, hierarchy = cv2.findContours(vessel_array[slice_no], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        inter_information = []
        if len(contours) != 0:
            for vessel_num in range(len(contours)):
                # draw_img = cv2.drawContours(img.copy(), contours, tumor_num, (0, 255, 0), 2)
                x, y, w, h = cv2.boundingRect(contours[vessel_num])  # [slice_num, [x, y], [x + w, y], [x, y + h], [x + w, y + h]]
                inter_information.append([slice_no, vessel_num, 0, x, y, w, h]) # [slice_no, tumor_num, tumor_no, location(4)]
            slice_information.append(inter_information)
        else:
            inter_information.append([slice_no, -1, -1, 0, 0, 0, 0])
            slice_information.append(inter_information)
    # print(slice_information)


'''
获取第一个和最后一个带有肿瘤的slice_no
返回值：first_slice：第一个带有肿瘤的切片；last_slice：第一个肿瘤消失的切片
'''


def first_and_last_slice():
    global slice_information
    global slice_num
    first_slice = 0
    for i in range(slice_num):
        if slice_information[i][0][1] != -1:    # have vessel
            first_slice = i
            break
    last_slice = 0
    for i in range(first_slice, slice_num):
        if slice_information[i][0][1] == -1:
            last_slice = i
            break
    return first_slice, last_slice


'''
将第一个有肿瘤切片中n个肿瘤标号：0,1,2,3...
'''


def first_vessel_no(first):
    global slice_information
    global total_vessel_num
    for i in range(slice_information[first][0][1] + 1):
        slice_information[first][i][2] = slice_information[first][i][1]     # 第一张切片的标号即为该张血管数量标记
        total_vessel_num += 1


'''
判断两肿瘤重叠率。
input：两肿瘤位置信息
output：返回overlap / before
'''


def rec_overlap_rate(x0, y0, w0, h0, x1, y1, w1, h1):     # x0, y0, w0, h0, x1, y1, w1, h1
    black0 = np.zeros((512, 512),dtype=np.uint8)
    black1 = np.zeros((512, 512), dtype=np.uint8)
    white0_pixel_num = 0
    for i in range(x0, x0 + w0):
        for j in range(y0, y0 + h0):
            black0[i][j] = 255
            white0_pixel_num += 1
    for i in range(x1, x1 + w1):
        for j in range(y1, y1 + h1):
            black1[i][j] = 255
    overlap_pixel_num = 0
    for i in range(x0, x0 + w0):
        for j in range(y0, y0 + h0):
            if black0[i][j] == black1[i][j]:
                overlap_pixel_num += 1
    overlap_rate = overlap_pixel_num / white0_pixel_num
    return overlap_rate


'''
修改每个切片上每个肿瘤的编号
'''


def get_vessel_no(first, last):
    global slice_information
    global total_vessel_num
    for i in range(first + 1, last - 1):
        for j in range(len(slice_information[i + 1])):
            for k in range(len(slice_information[i])):
                if rec_overlap_rate(slice_information[i][k][3], slice_information[i][k][4], slice_information[i][k][5], slice_information[i][k][6], slice_information[i + 1][j][3], slice_information[i + 1][j][4], slice_information[i + 1][j][5], slice_information[i + 1][j][6]) > 0:
                    slice_information[i + 1][j][2] = slice_information[i][k][2]
                    break
            else:
                total_vessel_num += 1
                slice_information[i + 1][j][2] = total_vessel_num
    # print(slice_information)


stop = False


def find_else_vessel(start, end):
    global slice_information
    global stop
    else_first_slice = 0
    for i in range(start, end):
        stop = True
        if slice_information[i][0][1] != -1:
            else_first_slice = i
            stop = False
            break

    else_last_slice = 0
    for i in range(else_first_slice, slice_num):
        if slice_information[i][0][1] == -1:
            else_last_slice = i
            break
    return else_first_slice, else_last_slice


def else_first_vessel_no(else_first):
    global slice_information
    global total_vessel_num
    for i in range(len(slice_information[else_first])):
        if stop:
            break
        else:
            total_vessel_num += 1
            slice_information[else_first][i][2] = total_vessel_num


def get_horizon_slice():
    global slice_information
    global slice_num
    global x_boundary
    get_slice = 0
    flag = False
    for i in range(slice_num):
        if len(slice_information[i]) > 1:
            for j in range(len(slice_information[i])):
                for k in range(j + 1, len(slice_information[i])):
                    if slice_information[i][j][2] == slice_information[i][k][2]:
                        get_slice = i
                        x_boundary = (slice_information[i][j][3] + slice_information[i][k][3] + slice_information[i][k][5]) / 2
                        flag = True
                        break
                if flag:
                    break
        if flag:
            break
    return get_slice, x_boundary


def pack(kernel):
    global slice_information
    slice_information = []
    itk_img = erode(case_no, kernel)
    collect_tumor_information(itk_img)
    first, last = first_and_last_slice()
    first_vessel_no(first)
    get_vessel_no(first, last)

    while not stop:
        first, last = find_else_vessel(last, slice_num)
        else_first_vessel_no(first)
        get_vessel_no(first - 1, last)

    return get_horizon_slice()


def loop():
    global slice_no
    for i in range(KERNEL_SIZE, 0, -1):
        # print(i)
        slice_no, boundary = pack(i)
        if slice_no != 0:
            print('center cut:', slice_no)
            break


def get_left_cut(slice_cut, boundary):
    global slice_num
    global slice_no
    left = 0
    left_width = 0
    itk_img = sitk.ReadImage('C:/Users/lrz/Desktop/DongBeiDaXue2/DongBeiDaXue2/portal_vein/data2_' + case_no + '_portal_vein_label.mha')
    itk_array = sitk.GetArrayFromImage(itk_img)
    for i in range(slice_cut + 5, slice_num):
        contours, hierarchy = cv2.findContours(itk_array[i], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) != 0:
            for j in range(len(contours)):
                x, y, w, h = cv2.boundingRect(contours[j])
                if left_width < w and (x + w) < boundary:
                    left_width = w
                    left = i
    left_cut = (slice_no + left) / 2
    print('left_cut:', left_cut)


def get_right_cut(slice_cut, boundary):
    global slice_num
    global slice_no
    right = 0
    right_width = 0
    itk_img = sitk.ReadImage('C:/Users/lrz/Desktop/DongBeiDaXue2/DongBeiDaXue2/portal_vein/data2_' + case_no + '_portal_vein_label.mha')
    itk_array = sitk.GetArrayFromImage(itk_img)
    for i in range(slice_cut + 5, slice_num):
        contours, hierarchy = cv2.findContours(itk_array[i], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) != 0:
            for j in range(len(contours)):
                x, y, w, h = cv2.boundingRect(contours[j])
                if right_width < w and x > boundary:
                    right_width = w
                    right = i
    right_cut = (slice_no + right) / 2
    print('right_cut:', right_cut)


if __name__ == '__main__':
    case_no = input('case_no:')
    loop()
    get_left_cut(slice_no, x_boundary)
    get_right_cut(slice_no, x_boundary)
