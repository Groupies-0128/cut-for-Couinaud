import cv2
import numpy as np
import SimpleITK as sitk


def get_coronal_plane(case_no):
    itk_img = sitk.ReadImage('D:/dataset/DongBeiDaXue2/DongBeiDaXue2/hepatic_vein/data2_' + case_no +
                             '_hepatic_vein_label.mha')
    itk_array = sitk.GetArrayFromImage(itk_img) * 255
    itk_array = np.array(itk_array)
    largest = 0
    coordinate2 = 0
    for height in range(512):
        coronal_plane = itk_array[:, height, :]
        # gray = cv2.cvtColor(coronal_plane, cv2.COLOR_BGR2GRAY)
        # ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(coronal_plane, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) != 0:
            for num in range(len(contours)):
                count = 0
                x, y, w, h = cv2.boundingRect(contours[num])
                for i in range(x, x + w):
                    for j in range(y, y + h):
                        if coronal_plane[j, i] == 255:
                            count += 1
                if count > largest:
                    largest = count
                    coordinate2 = height
    cv2.imshow('das', itk_array[:, coordinate2, :])
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return coordinate2


def get_sagittal_plane(case_no):
    itk_img = sitk.ReadImage('D:/dataset/DongBeiDaXue2/DongBeiDaXue2/hepatic_vein/data2_' + case_no +
                             '_hepatic_vein_label.mha')
    itk_array = sitk.GetArrayFromImage(itk_img) * 255
    itk_array = np.array(itk_array)
    largest = 0
    coordinate1 = 0
    for width in range(512):
        coronal_plane = itk_array[:, :, width]
        # gray = cv2.cvtColor(coronal_plane, cv2.COLOR_BGR2GRAY)
        # ret, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(coronal_plane, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(contours) != 0:
            for num in range(len(contours)):
                count = 0
                x, y, w, h = cv2.boundingRect(contours[num])
                for i in range(x, x + w):
                    for j in range(y, y + h):
                        if coronal_plane[j, i] == 255:
                            count += 1
                if count > largest:
                    largest = count
                    coordinate1 = width
    cv2.imshow('das', itk_array[:, :, coordinate1])
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return coordinate1


if __name__ == '__main__':
    case_no = input('case_no:')
    x = get_sagittal_plane(case_no)
    y = get_coronal_plane(case_no)
    print('The center vertical line\'s coordinate is :', '(', x, ',', y, ')')