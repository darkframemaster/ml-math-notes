#!/usr/bin/env python3

import collections, multiprocessing, os, time

from PIL import Image

from common import Qtrac, handle_commandline

Result = collections.namedtuple("Result", "copied scaled name")
Summary = collections.namedtuple(
			"Summary", 
			"todo copied scaled canceled"
			)


def scale_one(size, smooth, sourceImage, targetImage):
	oldImage = Image.open(sourceImage)
	if oldImage.width <= size and oldImage.height <= size:
		oldImage.save(targetImage)
		return Result(1, 0, targetImage)
	else:
		if smooth:
			newImage = oldImage.thumbnail((size, size))
		else:
			newImage = oldImage.resize((size, size))
		newImage.save(targetImage)
		return Result(0, 1, targetImage) 


def worker(size, smooth, jobs, results):
	while True:
		try:
			sourceImage, targetImage = jobs.get()
			try: 
				result = scale_one(size, smooth, sourceImage, targetImage)
				Qtrac.report("{}{}".format(
						"copied " if result.copied else "scaled",
						os.path.basename(result.name)
						)
					)
				results.put(result)
			except Exception as err:
				Qtrac.report(str(err), True)
		finally:
			jobs.task_done()


def create_processes(size, smooth, jobs, results, concurrency):
	for core in range(concurrency):
		process = multiprocessing.Process(
					target = worker,
					args = (size, smooth, jobs, results)
					)
		process.daemon = True
		process.start()

def add_jobs(source, target, jobs):
	for todo, name in enumerate(os.listdir(source), start = 1):
		sourceImage = os.path.join(source, name)
		targetImage = os.path.join(target, name)
		jobs.put((sourceImage, targetImage))
	return todo

def scale(size, smooth, source, target, concurrency):
	canceled = False
	jobs = multiprocessing.JoinableQueue()
	results = multiprocessing.Queue()
	create_processes(size, smooth, jobs, results, concurrency)
	todo = add_jobs(source, target, jobs)

	try:
		jobs.join()
	except KeyboardInterrupt:
		Qtrac.report("canceling...")
		canceled = True
	copied = scaled = 0
	while not results.empty():
		result = results.get_nowait()
		copied += result.copied
		scaled += result.scaled
	return Summary(todo, copied, scaled, canceled)

def main():
	st = time.time()
	size, smooth, source, target, concurrency = handle_commandline()
	Qtrac.report("starting...")
	summary = scale(size, smooth, source, target, concurrency)
	Qtrac.summarize(summary, concurrency)
	ed = time.time()
	print("\nTotal cost: {}".format(ed-st))

if __name__ == '__main__':
	main()
