import self_gmsh_generator

#Si   1
#Cu   2
#SiO2 3
#ILD  4
#BCB  5
_flag = 0

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

def generate_TSVs(boundary, landing_pad_size, center_points, points, lines, surfaces, volume):
	global _flag
	TSVs_num = len(center_points)
	points_num = 8 + TSVs_num * 4
	pos_vector = [[-1, -1], [1, -1], [1, 1], [-1, 1]]

	points_cnt = 0 # 点的数目
	points_cur = 0 # 当前点的标号
	points_next = 0 # 下一个点的标号
	points_begin = 0 # 点的开始位置
	points_begin_top = 0 # 顶部面点的开始位置
	points_begin_bottom = 0 # 底部面点的开始位置
	points_local_num = 0 # 面的顶点数

	points_top = [] # 顶部面的边界点
	points_bottom = [] # 底部面的边界点
	points_top_inside = [] # 顶部面的内部点（需要构造平面）
	points_bottom_inside = [] # 底部面的内部点（需要构造平面）
	points_top_nface = [] # 顶部面的内部点（不需要构造平面）
	points_bottom_nface = [] # 底部面的内部点（不需要构造平面）
	points_loop = [] #点集

	lines_cnt = 0 # 边的数目
	lines_cur = 0 # 边的当前标号
	lines_begin = 0 # 边的开始位置
	lines_begin_top = 0 # 顶部面边的开始位置
	lines_begin_bottom = 0 # 底部面边的开始位置
	lines_begin_side = 0 # 侧面边的开始位置
	lines_local_num = 0 # 面的顶边数

	lines_top = [] # 顶部面的边界边
	lines_top_inside = [] # 顶部面的内部边
	lines_bottom = [] # 底部面的边界边
	lines_bottom_inside = [] # 底部面的内部边
	lines_side = [] # 侧面的边界边
	lines_side_inside = [] # 侧面的内部边
	curve_loop = []

	surfaces_cnt = 0 # surface的数目
	surfaces_cur = 0 # surface的当前标号
	surfaces_begin = 0 # surface的开始位置
	surfaces_local_num = 0 # 面的顶surface数
 
	surfaces_top = [] # 顶部面的边界surface
	surfaces_top_inside = [] # 顶部面的内部surface
	surfaces_bottom = [] # 底部面的边界surface
	surfaces_bottom_inside = [] # 底部面的内部surface
	surfaces_side = [] # 侧面的边界surface
	surfaces_side_inside = [] # 侧面的内部surface
	surface_temp = []
	surface_temp2 = []
	surface_inside = []
	lines_in_surface = 0

	volume_temp = []
	volume_temp2 = []

	height = 1.0
	x = 0.0
	y = 0.0
	z = 0.0

	# layer1: SiO2

	# top surface
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
		points.append([x, y, z, 10.0])
		points_cnt += 1
		points_cur = points_cnt
		points_next = points_cur + 1
		if i + 1 == points_local_num:
			points_next = points_begin
		points_loop.append(points_cur)
		lines.append([points_cur, points_next])
		lines_cnt += 1
		lines_cur = lines_cnt
		curve_loop.append(lines_cur)
		surface_temp.append(lines_cur)
	surfaces.append(surface_temp.copy())
	lines_top.append(curve_loop.copy())
	points_top.append(points_loop)
	surfaces_cnt += 1
	volume_temp.append(-surfaces_cnt)
	surfaces_top.append(-surfaces_cnt)

	# if _flag:
	# 	print("top:")
	# 	print("points = " + str(points))
	# 	print("lines = " + str(lines))
	# 	print("surfaces = " + str(surfaces))
	# 	print("volume_temp = " + str(volume_temp))
	# 	print()

	# bottom surface
	points_begin = points_cnt + 1
	points_begin_bottom = points_begin
	lines_begin = lines_cnt + 1
	lines_begin_bottom = lines_begin

	del(surface_temp)
	surface_temp = []
	del(curve_loop)
	curve_loop = []
	del(points_loop)
	points_loop = []

	height = -1.0
	for i in range(points_local_num):
		x = pos_vector[i][0] * boundary[0]
		y = pos_vector[i][1] * boundary[1]
		z = height
		points.append([x, y, z, 0.13])
		points_cnt += 1
		points_cur = points_cnt
		points_next = points_cur + 1
		if i + 1 == points_local_num:
			points_next = points_begin
		points_loop.append(points_cur)
		lines.append([points_cur, points_next])
		lines_cnt += 1
		lines_cur = lines_cnt
		curve_loop.append(lines_cur)
		surface_temp.append(lines_cur)
	lines_bottom.append(curve_loop.copy())
	points_bottom.append(points_loop.copy())
	# surfaces.append(surface_temp.copy())
	# surfaces_cnt += 1
	# volume_temp.append(surfaces_cnt)

	## bottom inside surface
	for k in range(len(center_points)):
		z = height
		points_begin = points_cnt + 1
		del(surface_inside)
		surface_inside = []
		del(curve_loop)
		curve_loop = []
		del(points_loop)
		points_loop = []
		for i in range(points_local_num):
			x = center_points[k][0] + pos_vector[i][0] * landing_pad_size[0]
			y = center_points[k][1] + pos_vector[i][1] * landing_pad_size[1]
			points.append([x, y, z, 0.13])
			points_cnt += 1
			points_cur = points_cnt
			points_next = points_cur + 1
			if i + 1 == points_local_num:
				points_next = points_begin
			points_loop.append(points_cur)
			lines.append([points_cur, points_next])
			lines_cnt += 1
			lines_cur = lines_cnt
			surface_inside.append(lines_cur)
			curve_loop.append(lines_cur)
			surface_temp.append(-lines_cur)
		lines_bottom_inside.append(curve_loop.copy())
		points_bottom_inside.append(points_loop.copy())
		surfaces.append(surface_inside.copy())
		surfaces_cnt += 1
		volume_temp.append(surfaces_cnt)
		surfaces_bottom_inside.append(surfaces_cnt)
	surfaces.append(surface_temp.copy())
	surfaces_cnt += 1
	volume_temp.append(surfaces_cnt)
	surfaces_bottom.append(surfaces_cnt)

	# side surface
	points_begin = points_cnt + 1
	lines_begin = lines_cnt + 1
	lines_begin_side = lines_begin
	surfaces_begin = surfaces_cnt
	
	lines_local_num = 4
	del(curve_loop)
	curve_loop = []
	for k in range(lines_local_num):
		points_cur = points_begin_top + k
		points_next = points_begin_bottom + k
		lines.append([points_cur, points_next])
		lines_cnt += 1
		lines_cur = lines_cnt
		curve_loop.append(lines_cnt)
		# surface_temp.append(lines_cur)
	lines_side.append(curve_loop.copy())

	surfaces_local_num = 4
	lines_in_surface = 4
	del(surface_temp)
	surface_temp = list(range(lines_in_surface))
	for k in range(surfaces_local_num):
		surface_temp[0] = -(lines_begin_top + k)
		surface_temp[1] = (lines_begin_bottom + k)
		surface_temp[2] = (lines_begin_side + k)
		surface_temp[3] = -(surface_temp[2] + 1)
		if k + 1 == surfaces_local_num:
			surface_temp[3] = -lines_begin_side
		surfaces.append(surface_temp.copy())
		surfaces_cnt += 1
		volume_temp.append(-surfaces_cnt)
		surfaces_side.append(surfaces_cnt)
	volume.append(volume_temp.copy())
	# return

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
	
	# layer2: ILD & landing_pad(Cu)
	del(points_top)
	del(points_top_inside)
	points_top = points_bottom.copy()
	points_top_inside = points_bottom_inside.copy()
	del(lines_top)
	lines_top = lines_bottom.copy()
	del(lines_top_inside)
	lines_top_inside = lines_bottom_inside.copy()
	# print(lines_top)
	# return
	del(lines_side)
	lines_side = []
	del(surfaces_top)
	surfaces_top = surfaces_bottom.copy()
	del(surfaces_top_inside)
	surfaces_top_inside = surfaces_bottom_inside.copy()
	del(surfaces_side)
	surfaces_side = []
	del(surfaces_side_inside)
	surfaces_side_inside = []
	# points_begin = points_begin_bottom
	# print(points_begin)

	# top = layer1 bottom
	# points_begin = points_cnt + 1
	# points_begin_bottom = points_begin
	# lines_begin = lines_cnt + 1
	# lines_begin_bottom = lines_begin

	# bottom
	del(surface_temp)
	surface_temp = []
	# del(curve_loop)
	# curve_loop = []
	del(points_bottom)
	points_bottom = []
	del(points_bottom_inside)
	points_bottom_inside = []
	del(lines_bottom)
	lines_bottom = []
	del(lines_bottom_inside)
	lines_bottom_inside = []
	del(surfaces_bottom)
	surfaces_bottom = []
	del(surfaces_bottom_inside)
	surfaces_bottom_inside = []
	# del(points_loop)
	# points_loop = []

	height = -1.2
	# print(points_top)
	# return
	for k in range(len(points_top)):
		points_local_num = len(points_top[k])
		points_begin = points_cnt + 1
		del(curve_loop)
		curve_loop = []
		del(points_loop)
		points_loop = []
		for i in range(points_local_num):
			x = points[points_top[k][i]-1][0]
			y = points[points_top[k][i]-1][1]
			z = height
			points.append([x, y, z, 0.13])
			# print([x, y, z, 0.13])
			# return
			points_cnt += 1
			points_cur = points_cnt
			points_next = points_cur + 1
			if i + 1 == points_local_num:
				points_next = points_begin
			points_loop.append(points_cur)
			lines.append([points_cur, points_next])
			lines_cnt += 1
			lines_cur = lines_cnt
			curve_loop.append(lines_cur)
			# surface_temp.append(lines_cur)
		lines_bottom.append(curve_loop.copy())
		points_bottom.append(points_loop.copy())
	
	for k in range(len(points_top_inside)):
		points_local_num = len(points_top_inside[k])
		points_begin = points_cnt + 1
		del(curve_loop)
		curve_loop = []
		del(points_loop)
		points_loop = []
		for i in range(points_local_num):
			x = points[points_top_inside[k][i]-1][0]
			y = points[points_top_inside[k][i]-1][1]
			z = height
			points.append([x, y, z, 0.13])
			points_cnt += 1
			points_cur = points_cnt
			points_next = points_cur + 1
			if i + 1 == points_local_num:
				points_next = points_begin
			points_loop.append(points_cur)
			lines.append([points_cur, points_next])
			lines_cnt += 1
			lines_cur = lines_cnt
			curve_loop.append(lines_cur)
			# surface_temp.append(lines_cur)
		lines_bottom_inside.append(curve_loop.copy())
		points_bottom_inside.append(points_loop.copy())
	
	for k in range(len(center_points)):
		z = height
		points_begin = points_cnt + 1
		del(surface_inside)
		surface_inside = []
		del(curve_loop)
		curve_loop = []
		del(points_loop)
		points_loop = []
		points_local_num = 4
		for i in range(points_local_num):
			x = center_points[k][0] + pos_vector[i][0] * landing_pad_size[0] * 0.75
			y = center_points[k][1] + pos_vector[i][1] * landing_pad_size[1] * 0.75
			points.append([x, y, z, 0.13])
			points_cnt += 1
			points_cur = points_cnt
			points_next = points_cur + 1
			if i + 1 == points_local_num:
				points_next = points_begin
			points_loop.append(points_cur)
			lines.append([points_cur, points_next])
			lines_cnt += 1
			lines_cur = lines_cnt
			surface_inside.append(lines_cur)
			curve_loop.append(lines_cur)
			# surface_temp.append(-lines_cur)
		lines_bottom_inside.append(curve_loop.copy())
		points_bottom_inside.append(points_loop.copy())
		# surfaces.append(surface_inside.copy())
		# surfaces_cnt += 1
		# volume_temp.append(surfaces_cnt)
		# surfaces_bottom_inside.append(surfaces_cnt)
	# surfaces.append(surface_temp.copy())
	# surfaces_cnt += 1
	# volume_temp.append(surfaces_cnt)
	# surfaces_bottom.append(surfaces_cnt)
	# print_module("points", points)

	# return

	## bottom surface
	del(surface_temp)
	surface_temp = []
	del(surface_temp2)
	surface_temp2 = []
	for i in lines_bottom[0]:
		# print(i)
		surface_temp.append(i)
	for k in range(TSVs_num):
		del(surface_temp2)
		surface_temp2 = []
		for i in lines_bottom_inside[k]:
			surface_temp.append(-i)
			surface_temp2.append(i)
		for i in lines_bottom_inside[TSVs_num + k]:
			surface_temp2.append(-i)
		surfaces.append(surface_temp2.copy())
		surfaces_cnt += 1
		surfaces_bottom_inside.append(surfaces_cnt)

		del(surface_temp2)
		surface_temp2 = []
		for i in lines_bottom_inside[TSVs_num + k]:
			surface_temp2.append(i)
		surfaces.append(surface_temp2.copy())
		surfaces_cnt += 1
		surfaces_bottom_inside.append(surfaces_cnt)

	surfaces.append(surface_temp.copy())
	surfaces_cnt += 1	
	surfaces_bottom.append(surfaces_cnt)
	# print("surfaces_top = " + str(surfaces_top))
	# print("surfaces_top_inside = " + str(surfaces_top_inside))
	# print("surfaces_bottom_inside = " + str(surfaces_bottom_inside))
	# for i in surfaces_bottom_inside:
	# 	print(surfaces[i-1])
	# print("surfaces_bottom = " + str(surfaces_bottom))
	# for i in surfaces_bottom:
	# 	print(surfaces[i-1])
	# return


	# side 
	
	# print(points_top)
	# print(points_top_inside)
	# print(points_bottom)
	# print(points_bottom_inside)
	# print(surfaces_top_inside)

	del(curve_loop)
	curve_loop = []
	points_local_num = len(points_top[0])
	for i in range(points_local_num):
		points_cur = points_top[0][i]
		points_next = points_bottom[0][i]
		# print([points_cur, points_next])
		lines.append([points_cur, points_next])
		lines_cnt += 1
		lines_cur = lines_cnt
		curve_loop.append(lines_cnt)
	lines_side.append(curve_loop.copy())
	# print(curve_loop)

	for k in range(len(points_top_inside)):
		del(curve_loop)
		curve_loop = []
		points_local_num = len(points_top_inside[k])
		for i in range(points_local_num):
			points_cur = points_top_inside[k][i]
			points_next = points_bottom_inside[k][i]
			lines.append([points_cur, points_next])
			lines_cnt += 1
			lines_cur = lines_cnt
			curve_loop.append(lines_cnt)
		lines_side_inside.append(curve_loop.copy())
	
	# return
	
	## side surface
	del(surface_temp)
	lines_in_surface = 4
	surface_temp = list(range(lines_in_surface))
	
	# print("surfaces_top = " + str(surfaces_top))
	# print("surfaces_top_inside = " + str(surfaces_top_inside))
	# print("surfaces_bottom_inside = " + str(surfaces_bottom_inside))
	# for i in surfaces_bottom_inside:
	# 	print(surfaces[i-1])
	# print("surfaces_bottom = " + str(surfaces_bottom))
	# for i in surfaces_bottom:
	# 	print(surfaces[i-1])

	# print(lines_top)
	# print(lines_side)
	del(volume_temp)
	volume_temp = []
	print(surfaces[3])
	print(surfaces_top_inside)
	for i in surfaces_top:
		volume_temp.append(-i)
	for i in surfaces_bottom:
		volume_temp.append(i)
	# for i in range(len(surfaces_top_inside)):
	# 	volume_temp.append(-surfaces_top_inside[i])
	# 	volume_temp.append(surfaces_bottom_inside[i])
	print(surfaces_bottom_inside)
	print(surfaces[10])

	for k in range(len(lines_top)):
		lines_local_num = len(lines_top[k])
		for i in range(lines_local_num):
			surface_temp[0] = -lines_top[k][i]
			surface_temp[1] = lines_bottom[k][i]
			surface_temp[2] = lines_side[k][i]
			if i + 1 < lines_local_num:
				surface_temp[3] = -lines_side[k][i+1]
			else:
				surface_temp[3] = -lines_side[k][0]
			surfaces.append(surface_temp.copy())
			surfaces_cnt += 1
			volume_temp.append(-surfaces_cnt)
			surfaces_side_inside.append(surfaces_cnt)
	# print(lines_top_inside)
	# return
	
	for k in range(len(lines_top_inside)):
		lines_local_num = len(lines_top_inside[k])
		del(volume_temp2)
		volume_temp2 = []
		volume_temp2.append(-surfaces_top_inside[k])
		volume_temp2.append(surfaces_bottom_inside[2*k])
		volume_temp2.append(surfaces_bottom_inside[2*k+1])
		for i in range(lines_local_num):
			surface_temp[0] = -lines_top_inside[k][i]
			surface_temp[1] = lines_bottom_inside[k][i]
			surface_temp[2] = lines_side_inside[k][i]
			if i + 1 < lines_local_num:
				surface_temp[3] = -lines_side_inside[k][i+1]
			else:
				surface_temp[3] = -lines_side_inside[k][0]
			surfaces.append(surface_temp.copy())
			surfaces_cnt += 1
			volume_temp.append(surfaces_cnt)
			volume_temp2.append(-surfaces_cnt)
			surfaces_side_inside.append(surfaces_cnt)
		volume.append(volume_temp2.copy())
	# print(volume_temp)
	volume.append(volume_temp.copy())

	print(volume)
	
	
filename = "cube_test3.geo"
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

f.write("lc = 4.0;\n")
# generate_modules(points, lines, surfaces, volume, point_begin_index, \
# 	line_begin_index, surface_begin_index, volume_index, f)

boundary = [1.0, 1.0]
landing_pad_size = [0.1, 0.1]
center_points = [[0.0, 0.0], [0.5, 0.5]]
generate_TSVs(boundary, landing_pad_size, center_points, points, lines, surfaces, volume)
generate_modules(points, lines, surfaces, volume, point_begin_index, \
	line_begin_index, surface_begin_index, volume_index, f)
# print(f.name)
f.close()

# for i in range(1, 3):
# 	print(i)

# a1 = [1, 2]
# # a1 += 1
# b1 = []
# b1.append(a1.copy())
# a1[0] = 5
# # print()
# print(b1)
# del(a1)
# print(a1)
# print(list(range(2)))
