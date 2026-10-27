#include <iostream>
#include <iomanip>
#include <limits>

using namespace std;

int main(){
	int int_one = 1, int_two;
	double double_one = 2.0, double_two;
	string string_one = "my name is ", string_two;

	cout << "input a int, a double and a string" << endl;
	cin >> int_two >> double_two >> string_two;
	cout << "[+] first cout:" << endl;
	cout << int_two << double_two << string_two << endl;

	// this is the correct way to input a string
	//getline(cin, string_two);

	cout << "[+] second cout:" << endl;
	cout << int_one + int_two << endl;
	cout << showpoint << setprecision(2)  << double_one + double_two << endl;
	cout << string_one << string_two << endl;
	return 0;
}
