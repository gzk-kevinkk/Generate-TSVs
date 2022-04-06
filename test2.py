from audioop import add
from fileinput import filename
from glob import glob
import math
from turtle import clear

from matplotlib.pyplot import close

#Si   1
#Cu   2
#SiO2 3
#ILD  4
#BCB  5
_flag = 1

def point2str(point, point_len):
	ans = "{"
	ans += str(point[0])
	ans += ", "
	ans += str(point[1])
	ans += ", "
	ans += str(point[2])
	ans += ", "
	ans += str(point_len)
	ans += "}"
	return ans

def add_module(module_name, begin_index, module):
	module_len = len(module)
	temp_cnt = 0
	ans = ""
	for i in range(module_len):
		temp = module_name + "(" + str(begin_index + i) + ")= {"
		temp_cnt = 0
		for index in module[i]:
			if temp_cnt > 0:
				temp += ", "
			temp_cnt += 1
			temp += str(index)
		temp += "};\n"
		ans += temp
	return ans

def generate_modules(points, lines, surfaces, volume, point_begin_index, line_begin_index, \
	surface_begin_index, volume_index, file):
	str_points = ""
	str_lines = ""
	str_surfaces = ""
	str_volume = ""
	str_physical_surface = ""
	str_physical_volume = ""
	temp = ""
	points_num = len(points)
	curve_loop_num = len(surfaces)
	for i in range(points_num):
		temp = "Point(" + str(point_begin_index + i) + ") = " + point2str(points[i], "lc") + ";\n"
		str_points += temp
	print(str_points)
	str_points += "\n\n"
	f.write(str_points)

	temp = add_module("Line", line_begin_index, lines)
	str_lines += temp
	print(str_lines)
	str_lines += "\n\n"
	f.write(str_lines)	

	str_surfaces = add_module("Curve Loop", surface_begin_index, surfaces)
	str_surfaces += "\n"
	for i in range(curve_loop_num):
		temp = "Surface(" + str(i + surface_begin_index) + ")= {" \
			+ str(i + surface_begin_index) + "};\n"
		str_surfaces += temp
	print(str_surfaces)
	str_surfaces += "\n\n"
	f.write(str_surfaces)

	str_volume = add_module("Surface Loop", volume_index, volume)
	temp = "Volume(" + str(volume_index) + ") = {" + str(volume_index) +"};\n"
	str_volume += temp
	print(str_volume)
	str_volume += "\n\n"
	f.write(str_volume)

	temp_ls = []
	for i in range(curve_loop_num):
		temp_ls.append([surface_begin_index + i])
	temp = add_module("Physical Surface", surface_begin_index, temp_ls)
	print(temp)
	temp += "\n\n"
	f.write(temp)
	del(temp_ls)

	temp = "Physical Volume(" + str(volume_index) + ") = {" + str(volume_index) +"};\n"
	print(temp)
	temp += "\n\n"
	f.write(temp)

	temp = "Mesh 3;\n"
	temp += "Save \""
	temp += f.name.replace(".geo", ".mesh")
	temp += "\";\n"
	f.write(temp)

def generate_TSVs(boundary, landing_pad_size, center_points, points, lines, surfaces, volume):
	global _flag
	TSVs_num = len(center_points)
	points_num = 8 + TSVs_num * 4
	pos_vector = [[-1, -1], [1, -1], [1, 1], [-1, 1]]
	# left_lower_x = boundary[0][0]
	# left_lower_y = boundary[0][1]
	# left_lower_z = 15.0
	# right_higher_x = boundary[1][0]
	# right_higher_y = boundary[1][1]
	# right_higher_z = 45.0
	points_cnt = 0
	points_cur = 0
	points_next = 0
	points_begin = 0
	points_begin_top = 0
	points_begin_bottom = 0
	points_local_num = 0
	points_top = []
	points_bottom = []
	points_top_inside = []
	points_bottom_inside = []
	points_top_nface = []
	points_bottom_nface = []

	lines_cnt = 0
	lines_cur = 0
	lines_next = 0
	lines_begin = 0
	lines_begin_top = 0
	lines_begin_bottom = 0
	lines_begin_side = 0
	lines_local_num = 0

	surfaces_cnt = 0
	surfaces_cur = 0
	surfaces_next = 0
	surfaces_begin = 0
	surfaces_local_num = 0
	surface_temp = []
	lines_in_surface = 0

	volume_temp = []

	height = 1.0
	x = 0.0
	y = 0.0
	z = 0.0

	# layer1: SiO2

	#top surface
	points_local_num = 4
	points_begin = points_cnt + 1
	points_begin_top = points_begin
	lines_begin = lines_cnt + 1
	lines_begin_top = lines_begin
	surfaces_begin = surfaces_cnt
	surface_temp = []

	for i in range(points_local_num):
		x = pos_vector[i][0] * boundary[0]
		y = pos_vector[i][1] * boundary[1]
		z = height
		points.append([x, y, z])
		points_cnt += 1
		points_cur = points_cnt
		points_next = points_cur + 1
		if i + 1 == points_local_num:
			points_next = points_begin
		# points_top.append(points_cur)
		lines.append([points_cur, points_next])
		lines_cnt += 1
		lines_cur = lines_cnt
		surface_temp.append(lines_cur)
	surfaces.append(surface_temp.copy())
	surfaces_cnt += 1
	volume_temp.append(-surfaces_cnt)

	# if _flag:
	# 	print("top:")
	# 	print("points = " + str(points))
	# 	print("lines = " + str(lines))
	# 	print("surfaces = " + str(surfaces))
	# 	print("volume_temp = " + str(volume_temp))
	# 	print()

	#bottom surface
	points_begin = points_cnt + 1
	points_begin_bottom = points_begin
	lines_begin = lines_cnt + 1
	lines_begin_bottom = lines_begin
	surfaces_begin = surfaces_cnt
	del(surface_temp)
	surface_temp = []

	height = -1.0
	for i in range(points_local_num):
		x = pos_vector[i][0] * boundary[0]
		y = pos_vector[i][1] * boundary[1]
		z = height
		points.append([x, y, z])
		points_cnt += 1
		points_cur = points_cnt
		points_next = points_cur + 1
		if i + 1 == points_local_num:
			points_next = points_begin
		lines.append([points_cur, points_next])
		lines_cnt += 1
		lines_cur = lines_cnt
		surface_temp.append(lines_cur)
	surfaces.append(surface_temp.copy())
	surfaces_cnt += 1
	volume_temp.append(surfaces_cnt)

	#side surface
	points_begin = points_cnt + 1
	points_begin_bottom = points_begin
	lines_begin = lines_cnt + 1
	lines_begin_side = lines_begin
	surfaces_begin = surfaces_cnt
	

	lines_local_num = 4
	for k in range(lines_local_num):
		points_cur = points_begin_top + k
		points_next = points_begin_bottom + k
		lines.append([points_cur, points_next])
		lines_cnt += 1
		lines_cur = lines_cnt
		# surface_temp.append(lines_cur)

	surfaces_local_num = 4
	lines_in_surface = 4
	del(surface_temp)
	surface_temp = list(range(lines_in_surface))
	for k in range(surfaces_local_num):
		surface_temp[0] = lines_begin_top + k
		surface_temp[1] = -(lines_begin_bottom + k)
		surface_temp[2] = -(lines_begin_side + k)
		surface_temp[3] = surface_temp[2] + 1
		if k + 1 == surfaces_local_num:
			surface_temp[3] = lines_begin_side
		surfaces.append(surface_temp.copy())
		surfaces_cnt += 1
		volume_temp.append(surfaces_cnt)

	if _flag:
		print("cube:")
		print("points = " + str(points))
		print("lines = " + str(lines))
		print("surfaces = " + str(surfaces))
		print("volume_temp = " + str(volume_temp))
		print()
	
	# for k in range(TSVs_num):
	# 	for i in range(4):
	# 		x = pos_vector[i][0] * boundary[0]
	# 		y = pos_vector[i][1] * boundary[1]
	# 		z = height
	# 		points.append([x, y, z])
	
	
	

	
filename = "cube_test1.geo"
f = open(filename, "w")



points = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0], \
	[0.0, 0.0, 1.0], [1.0, 0.0, 1.0], [1.0, 1.0, 1.0], [0.0, 1.0, 1.0]]

lines = [[1, 2], [2, 3], [3, 4], [4, 1], [5, 6], [6, 7], [7, 8], [8, 5], [1, 5], [2, 6], [3, 7], [4, 8]]

surfaces = [[1, 2, 3, 4], [5, 6, 7, 8], [1, 10, -5, -9], \
	[2, 11, -6, -10], [3, 12, -7, -11], [4, 9, -8, -12]]

volume = [[1, -3, -4, -5, -6, -2]]

points = []
lines = []
surfaces = []
volume = []

point_begin_index = 1
line_begin_index = 1
surface_begin_index = 1
volume_index = 1

f.write("lc = 2.0;\n")
# generate_modules(points, lines, surfaces, volume, point_begin_index, \
# 	line_begin_index, surface_begin_index, volume_index, f)

boundary = [1.0, 1.0]
landing_pad_size = [6.0, 6.0]
center_points = []
generate_TSVs(boundary, landing_pad_size, center_points, points, lines, surfaces, volume)
# print(f.name)
f.close()

# for i in range(1, 3):
# 	print(i)

a1 = [1, 2]
# a1 += 1
b1 = []
b1.append(a1.copy())
a1[0] = 5
# print()
print(b1)
del(a1)
# print(a1)
# print(list(range(2)))
