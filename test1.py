from audioop import add
from fileinput import filename
from glob import glob
import math

point_begin_index = 0
point_end_index = 0

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
		temp = "Point(" + str(point_begin_index + i) + ") = {" + point2str(points[i], "lc") + "};\n"
		str_points += temp
	print(str_points)

	temp = add_module("Line", line_begin_index, lines)
	str_lines += temp
	print(str_lines)	

	str_surfaces = add_module("Curve Loop", surface_begin_index, surfaces)
	for i in range(curve_loop_num):
		temp = "Surface(" + str(i + surface_begin_index) + ")= {" \
			+ str(i + surface_begin_index) + "};\n"
		str_surfaces += temp
	print(str_surfaces)

	str_volume = add_module("Surface Loop", volume_index, volume)
	temp = "Volume(" + str(volume_index) + ") = {" + str(volume_index) +"};\n"
	str_volume += temp
	print(str_volume)

	temp_ls = []
	for i in range(curve_loop_num):
		temp_ls.append([surface_begin_index + i])
	temp = add_module("Physical Surface", surface_begin_index, temp_ls)
	print(temp)
	temp = "Physical Volume(" + str(volume_index) + ") = {" + str(volume_index) +"};\n"
	print(temp)

def generate(n, center_points, cube_len, name):
	d_theta = math.pi * 2 / n
	theta = []
	x = []
	y = []
	normal_x = []
	normal_y = []
	for i in range(n):
		cur = i * d_theta
		theta.append(cur)
    	# x.append(math.cos(cur))
    	# y.append(math.sin(cur))
    	# normal_x.append(math.cos(cur+0.5*d_theta))
    	# normal_y.append(math.sin(cur+0.5*d_theta))
		x.append(math.cos(cur - 0.5 * d_theta))
		y.append(math.sin(cur - 0.5 * d_theta))
		normal_x.append(math.cos(cur))
		normal_y.append(math.sin(cur))

	cube_n = 4
	cube_h = 5.0
	d_theta = math.pi * 2 / cube_n
	cube_x = []
	cube_y = []
	cube_normal_x = []
	cube_normal_y = []
	for i in range(cube_n):
		cur = i * d_theta
		cube_x.append(math.cos(cur) * cube_len)
		cube_y.append(math.sin(cur) * cube_len)
		cube_normal_x.append(math.cos(cur))
		cube_normal_y.append(math.sin(cur))
	with open(name, "w") as f:
		f.write("algebraic3d\n\n")
		for k in range(len(center_points)):
			center_x,center_y = center_points[k]
			center_x = float(center_x)
			center_y = float(center_y)
			f.write("solid fincyl"+str(k)+" = ")
			for i in range(n):
				f.write("plane ({:.16f}, {:.16f}, {:.16f}; {:.16f}, {:.16f}, {:.16f})\n    and " \
         		.format(center_x+x[i],center_y+y[i],0.0,normal_x[i],normal_y[i],0.0))
			f.write("plane ({:.16f}, {:.16f}, {:.16f}; {:.16f}, {:.16f}, {:.16f})\n    and " \
     		.format(0.0,0.0,0.5,0.0,0.0,1.0))
			f.write("plane ({:.16f}, {:.16f}, {:.16f}; {:.16f}, {:.16f}, {:.16f}) -bc=1;" \
     		.format(0.0,0.0,-0.5,0.0,0.0,-1.0))
			f.write("\n\n")
		f.write("solid cube = ")
		for i in range(cube_n):
			f.write("plane ({:.16f}, {:.16f}, {:.16f}; {:.16f}, {:.16f}, {:.16f})\n    and " \
         	.format(cube_x[i],cube_y[i],0.0,cube_normal_x[i],cube_normal_y[i],0.0))
		f.write("plane ({:.16f}, {:.16f}, {:.16f}; {:.16f}, {:.16f}, {:.16f})\n    and " \
     	.format(0.0,0.0,cube_h,0.0,0.0,1.0))
		f.write("plane ({:.16f}, {:.16f}, {:.16f}; {:.16f}, {:.16f}, {:.16f}) -bc=2;" \
     	.format(0.0,0.0,-cube_h,0.0,0.0,-1.0))
		f.write("\n\n")
		f.write("solid sio2 = cube and not fincyl0 and not fincyl1 and not fincyl2 and not fincyl3 and not fincyl4;\n\n")
		f.write("tlo sio2 -col=[0,1,0];\n")
		f.write("tlo fincyl0 -col=[1,1,0];\n")
		f.write("tlo fincyl1 -col=[1,1,0];\n")
		f.write("tlo fincyl2 -col=[1,1,0];\n")
		f.write("tlo fincyl3 -col=[1,1,0];\n")
		f.write("tlo fincyl4 -col=[1,1,0];")

center_points = [[0,0],[-3.0,0],[3.0,0],[0.0,3.0],[0.0,-3.0]]
# generate(72, center_points, 19.0, "hb_1x1_cross4.geo")
# generate(72, center_points, 24.0, "hb_1x1_cross_test24.geo")
# str1 = str(9)
# print(str1)
filename = "cube_test1.mesh"
f = open(filename, "w")
# point = [1.0, 2.0, 3.0]
# print(point2str(point, 1.0))

points = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0], \
	[0.0, 0.0, 1.0], [1.0, 0.0, 1.0], [1.0, 1.0, 1.0], [0.0, 1.0, 1.0]]

lines = [[1, 2], [2, 3], [3, 4], [4, 1], [5, 6], [6, 7], [7, 8], [8, 5], [1, 5], [2, 6], [3, 7], [4, 8]]

surfaces = [[1, 2, 3, 4], [5, 6, 7, 8], [1, 10, -5, -9], \
	[2, 11, -6, -10], [3, 12, -7, -11], [4, 9, -8, -12]]

volume = [[1, -3, -4, -5, -6, -2]]

generate_modules(points, lines, surfaces, volume, 1, 1, 1, 1, f)
