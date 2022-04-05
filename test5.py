import self_gmsh_generator

#Si   1
#Cu   2
#SiO2 3
#ILD  4
#BCB  5
_flag = 0

def generate_TSVs(boundary, landing_pad_size, TSV_size, heights, center_points, points, lines, surfaces, volume):
	global _flag
	TSVs_num = len(center_points)
	points_num = 8 + TSVs_num * 4
	gap_num = 3
	pos_vector = [[-1, -1], [1, -1], [1, 1], [-1, 1]]
	interval = 0
	offset = 0

	points_cnt = 0 # 点的数目
	points_cur = 0 # 当前点的标号
	points_next = 0 # 下一个点的标号
	points_begin = 0 # 点的开始位置
	points_begin_top = 0 # 顶部面点的开始位置
	points_begin_bottom = 0 # 底部面点的开始位置
	points_local_num = 0 # 面的顶点数
	point_size = 10.0

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
	surfaces_in_volume = 0

	height = heights[0]
	x = 0.0
	y = 0.0
	z = 0.0

	polygon_n = 6
	cylinder_bound = self_gmsh_generator.generate_polygen(polygon_n)
	radius1 = TSV_size[0]
	radius2 = TSV_size[1]

	#---------------------- layer1: SiO2 ----------------------#
	## top
	points_local_num = 4
	points_begin = points_cnt + 1
	points_begin_top = points_begin
	lines_begin = lines_cnt + 1
	lines_begin_top = lines_begin
	surface_temp = []

	height = heights[0]
	point_size = 60.0
	for i in range(points_local_num):
		x = pos_vector[i][0] * boundary[0]
		y = pos_vector[i][1] * boundary[1]
		z = height
		points.append([x, y, z, point_size])
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

	if _flag:
		print("top:")
		print("points = " + str(points))
		print("lines = " + str(lines))
		print("surfaces = " + str(surfaces))
		print("volume_temp = " + str(volume_temp))
		print()
	# return

	## bottom
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

	height = heights[1]
	point_size = 10.0
	for i in range(points_local_num):
		x = pos_vector[i][0] * boundary[0]
		y = pos_vector[i][1] * boundary[1]
		z = height
		points.append([x, y, z, point_size])
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
	# return

	### bottom inside
	points_local_num = 4
	point_size = 10.0
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
			# x = center_points[k][0] + radius1 * cylinder_bound[i][0]
			# y = center_points[k][1] + radius1 * cylinder_bound[i][1]
			points.append([x, y, z, point_size])
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
	# return

	## side
	points_begin = points_cnt + 1
	lines_begin = lines_cnt + 1
	lines_begin_side = lines_begin
	
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

	if _flag:
		print("cube:")
		print("points = " + str(points))
		print("lines = " + str(lines))
		print("surfaces = " + str(surfaces))
		print("volume_temp = " + str(volume_temp))
		print()
	# return
	
	#---------------------- layer2: ILD & landing_pad(Cu) ----------------------#
	## top = layer1 bottom
	del(points_top)
	del(points_top_inside)
	points_top = points_bottom.copy()
	points_top_inside = points_bottom_inside.copy()
	del(points_bottom)
	points_bottom = []
	del(points_bottom_inside)
	points_bottom_inside = []

	del(lines_top)
	del(lines_top_inside)
	lines_top = lines_bottom.copy()
	lines_top_inside = lines_bottom_inside.copy()
	del(lines_side)
	lines_side = []
	del(lines_side_inside)
	lines_side_inside = []
	del(lines_bottom)
	lines_bottom = []
	del(lines_bottom_inside)
	lines_bottom_inside = []

	del(surfaces_top)
	del(surfaces_top_inside)
	surfaces_top = surfaces_bottom.copy()
	surfaces_top_inside = surfaces_bottom_inside.copy()
	del(surfaces_side)
	surfaces_side = []
	del(surfaces_side_inside)
	surfaces_side_inside = []
	del(surfaces_bottom)
	surfaces_bottom = []
	del(surfaces_bottom_inside)
	surfaces_bottom_inside = []

	## bottom
	height = heights[2]
	point_size = 10.0
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
			points.append([x, y, z, point_size])
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
		lines_bottom.append(curve_loop.copy())
		points_bottom.append(points_loop.copy())
	
	point_size = 10.0
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
			points.append([x, y, z, point_size])
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
		lines_bottom_inside.append(curve_loop.copy())
		points_bottom_inside.append(points_loop.copy())
	
	point_size = 10.0
	for k in range(len(center_points)):
		z = height
		points_begin = points_cnt + 1
		del(surface_inside)
		surface_inside = []
		del(curve_loop)
		curve_loop = []
		del(points_loop)
		points_loop = []
		points_local_num = len(cylinder_bound)
		for i in range(points_local_num):
			x = center_points[k][0] + radius1 * cylinder_bound[i][0]
			y = center_points[k][1] + radius1 * cylinder_bound[i][1]
			points.append([x, y, z, point_size])
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
		lines_bottom_inside.append(curve_loop.copy())
		points_bottom_inside.append(points_loop.copy())
	
	point_size = 10.0
	for k in range(len(center_points)):
		z = height
		points_begin = points_cnt + 1
		del(surface_inside)
		surface_inside = []
		del(curve_loop)
		curve_loop = []
		del(points_loop)
		points_loop = []
		points_local_num = len(cylinder_bound)
		for i in range(points_local_num):
			x = center_points[k][0] + radius2 * cylinder_bound[i][0]
			y = center_points[k][1] + radius2 * cylinder_bound[i][1]
			points.append([x, y, z, point_size])
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
		lines_bottom_inside.append(curve_loop.copy())
		points_bottom_inside.append(points_loop.copy())
	# return

	### bottom surface
	del(surface_temp)
	surface_temp = []
	del(surface_temp2)
	surface_temp2 = []
	for i in lines_bottom[0]:
		surface_temp.append(i)
	for k in range(TSVs_num):
		for i in lines_bottom_inside[k]:
			surface_temp.append(-i)
	surfaces.append(surface_temp.copy())
	surfaces_cnt += 1	
	surfaces_bottom.append(surfaces_cnt)

	gap_num = 3
	for k in range(TSVs_num):
		for tt in range(0, gap_num-1):
			del(surface_temp)
			surface_temp = []
			for i in lines_bottom_inside[tt * TSVs_num + k]:
				surface_temp.append(i)
			for i in lines_bottom_inside[(tt+1) * TSVs_num + k]:
				surface_temp.append(-i)
			surfaces.append(surface_temp.copy())
			surfaces_cnt += 1	
			surfaces_bottom_inside.append(surfaces_cnt)
		del(surface_temp)
		surface_temp = []
		for i in lines_bottom_inside[(gap_num-1) * TSVs_num + k]:
			surface_temp.append(-i)
		surfaces.append(surface_temp.copy())
		surfaces_cnt += 1	
		surfaces_bottom_inside.append(surfaces_cnt)
		
	# return

	## side 
	del(curve_loop)
	curve_loop = []
	points_local_num = len(points_top[0])
	for i in range(points_local_num):
		points_cur = points_top[0][i]
		points_next = points_bottom[0][i]
		lines.append([points_cur, points_next])
		lines_cnt += 1
		lines_cur = lines_cnt
		curve_loop.append(lines_cnt)
	lines_side.append(curve_loop.copy())
	# return

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
	
	### side surface
	del(surface_temp)
	lines_in_surface = 4
	surface_temp = list(range(lines_in_surface))

	del(volume_temp)
	volume_temp = []
	for i in surfaces_top:
		volume_temp.append(-i)
		# print(surfaces[i-1])
	for i in surfaces_bottom:
		volume_temp.append(i)
		# print(surfaces[i-1])

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
			surfaces_side.append(surfaces_cnt)
	# print(lines_top_inside)
	# return

	for k in range(len(lines_top_inside)):
		lines_local_num = len(lines_top_inside[k])
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
			volume_temp.append(-surfaces_cnt)
			surfaces_side_inside.append(surfaces_cnt)
	volume.append(volume_temp.copy())

	# print(surfaces_top_inside)
	# print(surfaces_bottom_inside)
	# print(surfaces_side_inside)
	
	for k in range(TSVs_num):
		del(volume_temp)
		volume_temp = []
		lines_local_num = len(surfaces_top_inside)
		lines_local_num = int(lines_local_num / TSVs_num)
		for i in range(lines_local_num):
			volume_temp.append(-surfaces_top_inside[k*lines_local_num+i])

		lines_local_num = len(surfaces_bottom_inside)
		lines_local_num = int(lines_local_num / TSVs_num)
		for i in range(lines_local_num):
			volume_temp.append(surfaces_bottom_inside[k*lines_local_num+i])

		lines_local_num = len(surfaces_side_inside)
		lines_local_num = int(lines_local_num / TSVs_num)
		for i in range(lines_local_num):
			volume_temp.append(-surfaces_side_inside[k*lines_local_num+i])
		# print(str(k)+" volume: "+str(volume_temp))
		# for i in surfaces_top_inside:
		# 	volume_temp.append(-i)
		# 	# print(surfaces[i-1])
		# for i in surfaces_bottom_inside:
		# 	volume_temp.append(i)
		# 	# print(surfaces[i-1])
		# for i in surfaces_side_inside:
		# 	volume_temp.append(-i)
		volume.append(volume_temp.copy())
	# return

	#---------------------- layer3: dielectric(SiO2) & liner(SiO2) & TSV(Cu) ----------------------#
	## top = layer2 bottom
	del(points_top)
	del(points_top_inside)
	points_top = points_bottom.copy()
	points_top_inside = points_bottom_inside.copy()
	del(points_bottom)
	points_bottom = []
	del(points_bottom_inside)
	points_bottom_inside = []

	del(lines_top)
	del(lines_top_inside)
	lines_top = lines_bottom.copy()
	lines_top_inside = lines_bottom_inside.copy()
	del(lines_side)
	lines_side = []
	del(lines_side_inside)
	lines_side_inside = []
	del(lines_bottom)
	lines_bottom = []
	del(lines_bottom_inside)
	lines_bottom_inside = []

	del(surfaces_top)
	del(surfaces_top_inside)
	surfaces_top = surfaces_bottom.copy()
	surfaces_top_inside = surfaces_bottom_inside.copy()
	del(surfaces_side)
	surfaces_side = []
	del(surfaces_side_inside)
	surfaces_side_inside = []
	del(surfaces_bottom)
	surfaces_bottom = []
	del(surfaces_bottom_inside)
	surfaces_bottom_inside = []

	## bottom
	height = heights[3]
	point_size = 10.0
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
			points.append([x, y, z, point_size])
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
			points.append([x, y, z, point_size])
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
		lines_bottom_inside.append(curve_loop.copy())
		points_bottom_inside.append(points_loop.copy())
	# return
	
	### bottom surface
	del(surface_temp)
	surface_temp = []
	del(surface_temp2)
	surface_temp2 = []
	for i in lines_bottom[0]:
		surface_temp.append(i)
	for k in range(TSVs_num):
		for i in lines_bottom_inside[k]:
			surface_temp.append(-i)
	surfaces.append(surface_temp.copy())
	surfaces_cnt += 1	
	surfaces_bottom.append(surfaces_cnt)
	# return

	gap_num = 3
	for k in range(TSVs_num):
		for tt in range(0, gap_num-1):
			del(surface_temp)
			surface_temp = []
			for i in lines_bottom_inside[tt * TSVs_num + k]:
				surface_temp.append(i)
			for i in lines_bottom_inside[(tt+1) * TSVs_num + k]:
				surface_temp.append(-i)
			surfaces.append(surface_temp.copy())
			surfaces_cnt += 1	
			surfaces_bottom_inside.append(surfaces_cnt)
		del(surface_temp)
		surface_temp = []
		for i in lines_bottom_inside[(gap_num-1) * TSVs_num + k]:
			surface_temp.append(-i)
		surfaces.append(surface_temp.copy())
		surfaces_cnt += 1	
		surfaces_bottom_inside.append(surfaces_cnt)
	# return

	## side 
	del(curve_loop)
	curve_loop = []
	points_local_num = len(points_top[0])
	for i in range(points_local_num):
		points_cur = points_top[0][i]
		points_next = points_bottom[0][i]
		lines.append([points_cur, points_next])
		lines_cnt += 1
		lines_cur = lines_cnt
		curve_loop.append(lines_cnt)
	lines_side.append(curve_loop.copy())
	# return

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
	
	### side surface
	del(surface_temp)
	lines_in_surface = 4
	surface_temp = list(range(lines_in_surface))

	del(volume_temp)
	volume_temp = []
	for i in surfaces_top:
		volume_temp.append(-i)
	for i in surfaces_bottom:
		volume_temp.append(i)
	# print(surfaces_bottom_inside)
	# print(lines_top)
	# print(lines_bottom)
	# print(lines_side)
	# return

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
			# volume_temp.append(-surfaces_cnt)
			surfaces_side.append(surfaces_cnt)
	# print(lines_top_inside)
	# print(lines_bottom_inside)
	# return
	
	###------- surfaces_top_inside是排完一个TSV的全部top面，再排下一个；lines_top_inside是排完最外层，再排内层 -------###
	gap_num = 3
	for k in range(TSVs_num):
		for tt in range(gap_num):
			lines_local_num = len(lines_top_inside[tt*TSVs_num + k])
			for i in range(lines_local_num):
				surface_temp[0] = -lines_top_inside[tt*TSVs_num + k][i]
				surface_temp[1] = lines_bottom_inside[tt*TSVs_num + k][i]
				surface_temp[2] = lines_side_inside[tt*TSVs_num + k][i]
				if i + 1 < lines_local_num:
					surface_temp[3] = -lines_side_inside[tt*TSVs_num + k][i+1]
				else:
					surface_temp[3] = -lines_side_inside[tt*TSVs_num + k][0]
				surfaces.append(surface_temp.copy())
				surfaces_cnt += 1
				# volume_temp.append(surfaces_cnt)
				# volume_temp2.append(-surfaces_cnt)
				surfaces_side_inside.append(surfaces_cnt)
			# volume.append(volume_temp2.copy())
		# volume.append(volume_temp.copy())
	# return

	print(surfaces_top)
	print(surfaces_top_inside)
	print(surfaces_bottom)
	print(surfaces_bottom_inside)
	# print(surfaces_side)
	# print(surfaces_side_inside)

	### boundary volume
	del(volume_temp)
	volume_temp = []
	for i in surfaces_top:
		volume_temp.append(-i)
	for i in surfaces_bottom:
		volume_temp.append(i)
	for i in surfaces_side:
		volume_temp.append(-i)
	surfaces_in_volume = 4
	interval = surfaces_in_volume + polygon_n * (gap_num - 1)
	for k in range(TSVs_num):
		for i in range(surfaces_in_volume):
			volume_temp.append(surfaces_side_inside[k*interval + i])
	# print(volume_temp)
	# print(len(surfaces_side_inside))
	# print(interval)
	volume.append(volume_temp)
	# return

	### internal volumes
	for k in range(TSVs_num):
		for tt in range(gap_num-1):
			del(volume_temp)
			volume_temp = []
			volume_temp.append(-surfaces_top_inside[k*gap_num + tt])
			volume_temp.append(surfaces_bottom_inside[k*gap_num + tt])
			if tt == 0:
				surfaces_in_volume = 4
				offset = 0
			else:
				surfaces_in_volume = polygon_n
				offset = 4 + polygon_n*(tt-1)
			# print(" k = "+str(k)+", tt = "+str(tt)+", offset = "+str(offset))
			for i in range(surfaces_in_volume):
				volume_temp.append(-surfaces_side_inside[k*interval + offset + i])
			offset = offset + surfaces_in_volume
			surfaces_in_volume = polygon_n
			# print(k*interval + offset + i)
			for i in range(surfaces_in_volume):
				volume_temp.append(surfaces_side_inside[k*interval + offset + i])
				# print(k*interval + offset + i)
			volume.append(volume_temp)
			# print(volume_temp)
			# return
		del(volume_temp)
		volume_temp = []
		volume_temp.append(-surfaces_top_inside[k*gap_num + gap_num-1])
		volume_temp.append(surfaces_bottom_inside[k*gap_num + gap_num-1])
		offset = 4 + polygon_n*(gap_num-2)
		for i in range(surfaces_in_volume):
			volume_temp.append(-surfaces_side_inside[k*interval + offset + i])
		volume.append(volume_temp)

	
	# for k in range(TSVs_num):
	# 	lines_local_num = len(lines_top_inside[k+TSVs_num])
	# 	del(volume_temp)
	# 	volume_temp = []
	# 	volume_temp.append(-surfaces_top_inside[2*k+1])
	# 	volume_temp.append(surfaces_bottom_inside[2*k+1])
	# 	for i in range(lines_local_num):
	# 		volume_temp.append(-surfaces_side_inside[lines_local_num * (k+TSVs_num) + i])
	# 	volume.append(volume_temp.copy())

	# print(volume)
	
	
filename = "cube_test5.geo"
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

boundary = [50.0, 50.0]
landing_pad_size = [10.0, 10.0]
center_points = [[0.0, 0.0], [0.0, 25.0], [25.0, 0.0]]
TSV_size = [8.625, 2.5]
heights = [45.0, 30.0, 24.87, 14.70, 0.0, -12.70, -20.87, -30.0, -45.0]
generate_TSVs(boundary, landing_pad_size, TSV_size, heights, center_points, points, lines, surfaces, volume)
self_gmsh_generator.generate_modules(points, lines, surfaces, volume, point_begin_index, \
	line_begin_index, surface_begin_index, volume_index, f, 0)
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
