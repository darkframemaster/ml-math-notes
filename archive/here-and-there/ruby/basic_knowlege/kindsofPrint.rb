#!/usr/bin/ruby

puts "1. Use puts and print to print out!\n"
puts "To print out a normal sentence use 'puts',puts end with a '\\n' while print not"
puts "puts part one" << " << part two"
puts "puts part one" + " + part two\n"

print "To print out a normal sentence use 'print'\n"
print "print part one" << " << part two\n"
print "print part one" + " + part two\n\n"

print <<EOF
	May you want to print out a very long text.
	And it can cost a lot of lines.
	Like this...
	
	And you can use "print <<something"
	something in  here most follow '<<' without any space,something can be a string or "string" 
	
EOF

puts "2.To print out variables!"
puts "Why it turns warn when you get a argument for command line. The Error sames like happend in gets part, how to fix it?"
action = "Hello"
name = "Myfriend"
puts action + " " +  name + "\n"
puts "#{action} #{name}, you can use '\#{variable_name}' to get value of variables in a string,kind of str.format() in python"
puts "Hello #{ARGV[0]}, you can use '\#{ARGV[0]} to get a command line argument! This is awesome!'"
puts "Hello %s ,you can use \ to format your output!" % name
puts "You can use 'gets' to get things form keyborad input! Now input a person you like!"
person_u_like = gets
puts "I like " + person_u_like

puts "\n" + "3.To print a sentence for many times"
puts "To puts/print a sentence for many times use 'string*number'\n" * 2
2.times {puts "another way by using 'number.times{puts/print 'string'}'"}
