import os 
import utils
base_path = ''

def set_seeds(flag):
	seen = set()
	queue = set()
	if flag:
		path = '%s../data/' % base_path
		old_queue = utils.load_set('%squeue'%path)
		old_seen = utils.load_set('%sseen'%path)
		for q in old_queue:
			if q not in old_seen:
				queue.add(q)
		seen = old_seen
	else:
		queue = utils.load_set('%sseeds'%base_path)
	return queue,seen
if __name__ == '__main__':
	queue,seen = set_seeds(False)
	print(len(seen),len(queue))
