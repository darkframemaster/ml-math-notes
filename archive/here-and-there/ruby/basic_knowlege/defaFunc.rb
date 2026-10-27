#!/usr/bin/ruby 

def first_func
print <<EOF
OK, here is how to define a function in ruby:
	
	"""
	def func_name	#keyword def to naming a func.
		
		Do something in here
	
	end		#keyword end to ending a func.
	"""
	
little bit like python.
EOF
end

def func_with_yield
	puts "\n" + "This func contains a keyword yield. Let's see how it works!"
	puts "\n"

	yield	
	
	puts "\n" + "Sames like we can use some codes to be the arguments and it will get executed by 'yield'"
end

first_func	#we use the function in here.
func_with_yield{ puts "How can you see me!"}
