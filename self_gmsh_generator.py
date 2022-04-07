import math

def generate_polygen(n, type = 1, debug = 0):
	d_theta = math.pi * 2 / n
	x = 0.0
	y = 0.0
	ans = []
	for i in range(n):
		cur = i * d_theta
		if (type == 1):
			x = math.cos(cur - 0.5 * d_theta)
			y = math.sin(cur - 0.5 * d_theta)
			ans.append([x, y])
		elif(type == 2):
			x = math.cos(cur)
			y = math.sin(cur)
			ans.append([x, y])
	if debug:
		print("type = " + str(type))
		print(x)
		print(y)
	return ans

def print_module(module_name, module):
	print(module_name)
	for i in range(len(module)):
		print(str(i) + ": " + str(module[i]))

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

def generate_modules(points, lines, surfaces, volumes, point_begin_index, line_begin_index, \
	surface_begin_index, volume_begin_index, file):
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
		temp = "Point(" + str(point_begin_index + i) + ") = " + point2str(points[i], points[i][3]) + ";\n"
		str_points += temp
	# print(str_points)
	str_points += "\n\n"
	file.write(str_points)

	temp = add_module("Line", line_begin_index, lines)
	str_lines += temp
	# print(str_lines)
	str_lines += "\n\n"
	file.write(str_lines)	

	str_surfaces = add_module("Curve Loop", surface_begin_index, surfaces)
	str_surfaces += "\n"
	for i in range(curve_loop_num):
		temp = "Plane Surface(" + str(i + surface_begin_index) + ")= {" \
			+ str(i + surface_begin_index) + "};\n"
		str_surfaces += temp
	# print(str_surfaces)
	str_surfaces += "\n\n"
	file.write(str_surfaces)

	str_volume = add_module("Surface Loop", volume_begin_index, volumes)
	for i in range(len(volumes)):
		temp = "Volume(" + str(i + volume_begin_index) + ")= {" \
			+ str(i + volume_begin_index) + "};\n"
		str_volume += temp
	# temp = "Volume(" + str(volume_index) + ") = {" + str(volume_index) +"};\n"
	# str_volume += temp
	# print(str_volume)
	str_volume += "\n\n"
	file.write(str_volume)

	temp_ls = []
	for i in range(curve_loop_num):
		temp_ls.append([surface_begin_index + i])
	temp = add_module("Physical Surface", surface_begin_index, temp_ls)
	# print(temp)
	temp += "\n\n"
	file.write(temp)
	del(temp_ls)

	temp_ls = []
	for i in range(len(volumes)):
		temp_ls.append([volume_begin_index + i])
	temp = add_module("Physical Volume", volume_begin_index, temp_ls)
	# temp = "Physical Volume(" + str(volume_index) + ") = {" + str(volume_index) +"};\n"
	# print(temp)
	temp += "\n\n"
	file.write(temp)

	temp = "Mesh 3;\n"
	temp += "Save \""
	temp += file.name.replace(".geo", ".mesh")
	temp += "\";\n"
	file.write(temp)

if __name__ == "__main__":
	ans = generate_polygen(4, type=1, debug=0)
	for p in ans:
		print(p)
	print(str((2**(0.5)) * ans[0][0]))