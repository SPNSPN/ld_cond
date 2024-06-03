#! -*- coding: utf-8 -*-

def roule1 (cond1, cond2):
	if cond1[1] == cond2[1] and cond1[2] == cond2[2]:
		return [{"type": "or", "values": [cond1[0], cond2[0]]}, cond1[1], cond1[2]]
	return False

def roule2 (cond1, cond2):
	if cond1[2] == [cond2[0]] and [cond1[0]] == cond2[1]:
		return [{"type": "and", "values": [cond1[0], cond2[0]]}, cond1[1], cond2[2]]
	if cond2[2] == [cond1[0]] and [cond2[0]] == cond1[1]:
		return [{"type": "and", "values": [cond2[0], cond1[0]]}, cond2[1], cond1[2]]
	return False


def compress1 (roule, arr):
	if all(map(lambda e: e in arr, roule["values"])):
		return list(filter(lambda e: e not in roule["values"], arr)) + [roule]
	return arr

def compress2 (roule, arr):
	if roule["values"][-1] in arr:
		return list(filter(lambda e: e != roule["values"][-1], arr)) + [roule]
	return arr

def apply_roule (roule, compress, conds):
	for i1 in range(0, len(conds)):
		for i2 in range(0, len(conds)):
			if i1 == i2:
				continue
			accepted = roule(conds[i1], conds[i2])
			if accepted:
				rest_conds = filter(lambda c: c != conds[i1] and c != conds[i2], conds)
				crest_conds = map(lambda c: [c[0], compress(accepted[0], c[1]), compress(accepted[0], c[2])], rest_conds)
				return list(crest_conds) + [accepted]
	return conds

def cond2nim (cond):
	nims = []
	if isinstance(cond, dict):
		v1 = cond["values"][0]
		v2 = cond["values"][1]
		if "or" == cond["type"]:
			if not (isinstance(v1, dict) or isinstance(v2, dict)):
				nims.extend(cond2nim(v1))
				tnim = cond2nim(v2)
				nims.append(["OR", tnim[0][1]])
			else:
				nims.extend(cond2nim(v1))
				nims.extend(cond2nim(v2))
				nims.append(["ORB"])
		elif "and" == cond["type"]:
			if not isinstance(v2, dict):
				nims.extend(cond2nim(v1))
				tnim = cond2nim(v2)
				nims.append(["AND", tnim[0][1]])
			else:
				nims.extend(cond2nim(v1))
				nims.extend(cond2nim(v2))
				nims.append(["ANB"])
		else:
			raise RuntimeError("Unknown cond type: {0}".format(cond))
	else:
		nims.append(["LD", cond])
	return nims


cond = []
cond.append([1, [0], [3, 4]])
cond.append([2, [0], [3, 4]])
cond.append([3, [1, 2], [6]])
cond.append([4, [1, 2], [6]])
cond.append([5, [0], [6]])
cond.append([6, [3, 4, 5], [7]])

print("[INFO]: start")
[print(e) for e in cond]

print("[INFO]: connection -> logic")
r1 = cond
while True:
	pre_r1 = r1
	r1 = apply_roule(roule2, compress2, apply_roule(roule1, compress1, pre_r1))
	if pre_r1 == r1:
		break
[print(e) for e in r1]

print("[INFO]: logic -> nimonic")
nims = cond2nim(r1[0][0])
[print(nim) for nim in nims]
