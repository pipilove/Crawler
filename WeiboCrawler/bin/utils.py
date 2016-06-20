def load_set(filename):
	set_ = set()
	f = open(filename)
	for line in f:
		line = line.strip()
		if line == '':
			continue
		set_.add(line)
	f.close()
	return set_

def load_list(filename):
	list_ = []
	f = open(filename)
	for line in f:
		line = line.strip()
		if line == '':
			continue
		list_.append(line)
	f.close()
	return list_

