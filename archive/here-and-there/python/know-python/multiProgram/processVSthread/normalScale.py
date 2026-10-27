#!/usr/bin/env python3

def scale(size, smooth, source, target, concurrency):
	canceled = False
	
	pictures = []
	for todo, name in enumerate(os.listdir(source), start = 1):
		sourceImage = os.path.join(source, name)
		targetImage = os.path.join(target, name)
		pictures.append((sourceImage, targetImage))


def main():
	st = time.time()
	size, smooth, source, target, concurrency = handle_commandline()
	Qtrac.report("starting...")
	summary = scale(size, smooth, source, target, concurrency)
	summarize(summary, concurrency)
	ed = time.time()
	print("\nTotal cost: {}".format(ed-st))

if __name__ == '__main__':
	main()
