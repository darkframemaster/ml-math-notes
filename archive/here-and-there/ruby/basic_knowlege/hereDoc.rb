#!/usr/bin/ruby 

print <<EOF
	You can use '<<' to set a EOF of a here document.
	AND THE '<<' SHOULD NOT FOLLOWED BY ' '.
	
	for ex:
		print <<"something in here"
			something you want to print out.
			maybe it is a long story.
		something in here


EOF

print <<EOF
	this is the first way of creating a here document.
	it can contain many lines of word.
EOF
print <<"EOF";
	this is the second way of creating a here document.
	Say something i dont know.

EOF

print <<`EOC`
	echo you can run some command in here like 'ls'
	ls | less
EOC

print <<"foo", <<"bar"

	And you can use not just one EOF to end document.
	I said foo.
foo
	I said bar.
bar
