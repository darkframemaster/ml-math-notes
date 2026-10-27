#!/usr/bin/env python3

import argparse, multiprocessing, os, sys


class Qtrac():
	def report(message = "", error = False):
		if len(message) >= 70 and not error:
			message = message[:67] + "..."
		sys.stdout.write("\r{:70}{}".format(message, "\n" if error else ""))
		sys.stdout.flush()

	def summarize(summary, concurrency):
		message =  "\ncopied {}\nscaled {}\n".format(summary.copied, summary.scaled)
		difference = summary.todo - (summary.copied + summary.scaled)
		if difference:
			message += "skipped {}\n".format(difference)
		message += "using {} processes".format(concurrency)
		if summary.canceled:
			message += " [canceled]"
		Qtrac.report(message)
		print()

def handle_commandline():
	parse = argparse.ArgumentParser()
	parse.add_argument("-c ", "--concurrency", type = int, 
			default = multiprocessing.cpu_count(),
			help = "specify the concurrency (for debugging and "
				"timing) [default: %(default)d]"
			)
	parse.add_argument("-s", "--size", default = 400, type = int,
			help = "make a scaled image that fits the given " 
				"dimension [default: %(default)d]"
			)
	parse.add_argument("-S", "--smooth", action="store_true",
			help = "use smooth scaling (slow but good for text)"
			)
	parse.add_argument("source",
			help = "the directory containing the original .xpm images"
			)
	parse.add_argument("target",
			help = "the directory for the scaled .xpm images")
	args = parse.parse_args()
	source = os.path.abspath(args.source)
	target = os.path.abspath(args.target)
	if source == target:
		args.error("source and target must be different")
	if not os.path.exists(args.target):
		os.makedirs(target)
	return args.size, args.smooth, source, target, args.concurrency

