import os
import re
from queue import Queue
import argparse

def strip_nq(s):
	return strip_name(strip_quotes(s))

def strip_name(n):
	return n[:n.find(".")]

def strip_quotes(s):
	return s[s.find("\"")+1:-1]

def find_includes(file):
	include_pattern = re.compile("^#include \".*\"$")
	nonstl_dependencies = []
	with open(file) as fp:
		lines = fp.readlines()
		nonstl_dependencies = [strip_nq(include_pattern.match(l)[0]) \
			for l in lines if include_pattern.match(l)]
	return nonstl_dependencies

def parse_dependencies(directory): 
	build_files = [f for f in os.listdir(directory) if (".cpp" in f or ".h" in f)]
	dependencies = { strip_name(f) : [] for f in build_files }
	for f in build_files:
		k = strip_name(f)
		dependencies[k] += list(set(find_includes(f)) - {k})
	return dependencies

def build_dependency_list(target, dependencies):
	mf_lines = []
	objs = []
	q = Queue()
	q.put(strip_name(target))
	while not q.empty():
		obj = q.get()
		l = obj + ".o:"
		objs += [l[:-1]]
		if dependencies[obj]:
			for d in dependencies[obj]:
				q.put(d)
				l += " " + d + ".h"
			mf_lines += [l]
	return mf_lines, list(set(objs))

def build_obj_list(dependencies):
	objs = [d + ".o" for d in dependencies.keys()]
	return " ".join(objs)

def write_makefile(mf):
	with open("Makefile", "w") as f:
		for l in mf:
			f.write(l + '\n')

##############################

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--directory", "-d", dest = "dir", default = ".")
	parser.add_argument("--cppflags", "-f", dest = "cppflags", default = "--std=c++17")
	parser.add_argument("-cxxflags", "-xf", dest = "cxxflags", default = "-Wall -g")
	parser.add_argument("target")
	parser.add_argument("--executable", "-e", dest = "exec", default = "main")
	args = parser.parse_args()

	d = parse_dependencies(args.dir)
	l, o = build_dependency_list(args.target, d)
	mf = [
		"CXX = g++", 
		"CPPFLAGS = " + args.cppflags, 
		"CXXFLAGS = " + args.cxxflags, 
		"OBJS = " + " ".join(o),
		"TARGET = " + args.exec, 
		"",
		"$(TARGET) : $(OBJS)" + '\n\t' + "$(CXX) $(CPPFLAGS) $(CXXFLAGS) -o $(TARGET) $(OBJS)",
		""
	]
	mf += l
	mf += [
		"", 
		"clean:" + '\n\t' + "$(RM) *.o $(TARGET)"
	]	 
	write_makefile(mf)
