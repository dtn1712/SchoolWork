// RAM interpreter
// Purpose: To simulate the execution of a RAM (random access machine)
// Author: Jeremy Johnson
// Date: 9/25/00

#include <iostream>
#include "ram.h"
#include "inst.h"
using namespace std;

int main()
{
	int pSize, mSize;
	char pName[80], mName[80];

	cout << "Enter program size:  ";
	cin >> pSize;
	cout << "Enter memory size:  " ;
	cin >> mSize;
	RAM M(pSize,mSize);  // Create RAM with space for a program of size pSize
	                     // and memory of size mSize

	cout << "Enter name of file containing RAM program:  ";
	cin >> pName;
	cout << "Enter name of file containing RAM initial memory configuration:  ";
	cin >> mName;

	M.init(pName,mName);  // Initialize RAM with program in pName and
	                               // initial memory configuration in mName

	cout << "Initial Memory Configuration" << endl;
	M.dump();

	M.execute();  // Execute RAM with given program and memory configuration

	cout << endl << "Final Memory Configuration" << endl;
	M.dump();

	//system("PAUSE");
}
