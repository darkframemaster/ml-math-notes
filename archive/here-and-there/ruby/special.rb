#!/usr/bin/ruby

puts "1.Pack and unpack, this is awesome!"
x,y,z = "I"," love ","U"
puts x+y+z
x,y,z = z,y,x
puts x+y+z
puts "\n\n"

puts "2.Some methods."
puts "2.1 Get part of a string!"
string = 'This is a normal string!'
puts "Full string is:\t\t" + string
puts "This is part of the string:\t\t" + string[-10..-1]
puts ""

puts "2.2 Get Ascii!"
puts ?a
