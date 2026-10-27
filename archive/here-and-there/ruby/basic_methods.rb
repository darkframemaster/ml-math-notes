#!/usr/bin/ruby

print <<EOF	

Methods from Object:

	1. kind_of?(SOME_TYPE)

	This method is like isinstance in python.
	ex: 
		x = 100
		x.kind_of?(Integer)
		x.kind_of? Integer

	2. to_f

	Change Type to float.
	ex:
		x = 100
		x.to_f
		x = 100.0
	
	3. class
	
	ex:
		x = 100
		x.class
EOF

x = 100
puts x.kind_of? (Integer)
puts x.to_f
puts x.class
