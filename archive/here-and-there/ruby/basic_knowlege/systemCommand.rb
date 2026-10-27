#!/usr/bin/ruby

puts "\n\t" + "1.use 'system' to run the commands!" + "\n"

system "echo 'Hello,Matz!'"
system "echo", "Hello,","Matz!"

print <<EOF

	another key word is 'exec',but sometimes the 'system' is more likely to  	be used.

EOF

puts "\n\t" + "2.use `command` to run system command! This is awesome!" + "\n" 

puts "\n" + "I am running " + `ruby --version`
puts "\n" + "And processes contain ruby is:"
puts `ps -ax | grep ruby`

puts "\n" + "You can use a variable to save the result!like this"
sys_info = `ps -ax | grep ruby`
puts sys_info
