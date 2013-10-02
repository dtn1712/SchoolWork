// Implementation of RAM class

#include <iostream>
#include <fstream>
#include <string>
#include "ram.h"
#include "inst.h"
#include <cstdlib>

using namespace std;

// Constructors

RAM::RAM() { 
	const int DEFMEMSIZE = 100;
	const int DEFPROGSIZE = 50;
	memorySize = DEFMEMSIZE;
	programSize = DEFPROGSIZE;
	memory = new int[memorySize+1];
	program = new Instruction[programSize+1];
	pc = 1;  ac = 0;
	for (int i=0;i<=memorySize;i++)
		memory[i] = 0;
}

RAM::RAM(int pSize, int mSize)
{
	memorySize = mSize;
	programSize = pSize;
	memory = new int[memorySize+1];  // indexing for RAM memory starts at 1
	program = new Instruction[programSize+1]; // indexing for RAM program starts at 1
	pc = 1;  ac = 0;
	for (int i=0;i<=memorySize;i++)
		memory[i] = 0;
}

// Initialize RAM with hardwired program and memory
// pc is set to 1 and ac is set to 0.
void RAM::init()
{
	program[1].opcode = LDA;
	program[1].operand = 3;
	program[2].opcode = SUB;
	program[2].operand = 4;
	program[3].opcode = JMZ;
	program[3].operand = 7;
	program[4].opcode = LDA;
	program[4].operand = 1;
	program[5].opcode = STA;
	program[5].operand = 5;
	program[6].opcode = HLT;
	program[7].opcode = LDA;
	program[7].operand = 2;
	program[8].opcode = STA;
	program[8].operand = 5;
	program[9].opcode = HLT;
	programSize = 9;

	memory[1] = 0;
	memory[2] = 1;
	memory[3] = 2;
	memory[4] = 1;
	memory[5] = 3;
	pc = 1;  ac = 0;
}

// Initialize RAM with program in file with the name pInput
// and initial memory configuration in the file with name mInput
// pc is set to 1 and ac is set to 0.  programSize is set to the number
// of instructions read.
void RAM::init(const char *pInput, const char *mInput) {
	// Initialize Memory
	int addr, value;
	const int MAXSTRSIZE = 160;
	char str[MAXSTRSIZE];

	// Initialize memory
	ifstream mFile(mInput,ios::in);
	if (! mFile) {
		cerr << "Error: program file not found" << endl;
		exit(1);
	}

	while (mFile >> addr >> value) {
		if (addr < 1 || addr > memorySize) {
			cerr << "Error:  illegal memory location" << endl;
			exit(1);
		}
		memory[addr] = value;
		mFile.getline(str,MAXSTRSIZE);  // flush line (possibly contains comment)
	}

	// Initialize program
	string instName;

	ifstream pFile(pInput,ios::in);
	if (! pFile) {
		cerr << "Error: program file not found" << endl;
		exit(1);
	}

	pc = 1;
	while (pFile >> str) {
		instName = str;
		if (instName[0] == ';') {
			pFile.getline(str,MAXSTRSIZE); } // flush to end of line
		else if (instName == "LDA") {
			program[pc].opcode = LDA;
			pFile >> program[pc].operand; 
			pFile.getline(str,MAXSTRSIZE);  pc++; } 
		else if (instName == "LDI") {
			program[pc].opcode = LDI;
			pFile >> program[pc].operand; 
			pFile.getline(str,MAXSTRSIZE);  pc++; }
		else if (instName == "STA") {
			program[pc].opcode = STA;
			pFile >> program[pc].operand;
			pFile.getline(str,MAXSTRSIZE);  pc++; }
		else if (instName == "STI") {
			program[pc].opcode = STI;
			pFile >> program[pc].operand; 
			pFile.getline(str,MAXSTRSIZE);  pc++; }
		else if (instName == "ADD") {
			program[pc].opcode = ADD;
			pFile >> program[pc].operand; 
			pFile.getline(str,MAXSTRSIZE);  pc++; }
		else if (instName == "SUB") {
			program[pc].opcode = SUB;
			pFile >> program[pc].operand; 
			pFile.getline(str,MAXSTRSIZE);  pc++; }
		else if (instName == "JMP") {
			program[pc].opcode = JMP;
			pFile >> program[pc].operand;
			pFile.getline(str,MAXSTRSIZE);  pc++; }
		else if (instName == "JMZ") {
			program[pc].opcode = JMZ;
			pFile >> program[pc].operand;
			pFile.getline(str,MAXSTRSIZE);  pc++; }
		else if (instName == "JMN") {
			program[pc].opcode = JMN;
			pFile >> program[pc].operand;
			pFile.getline(str,MAXSTRSIZE);  pc++; }
		else if (instName == "HLT") {
			program[pc].opcode = HLT;
			pFile.getline(str,MAXSTRSIZE);  pc++; }
		else { cerr << "Error:  Illegal Instruction" << endl;
		exit(1); }
		if (pc-1 > programSize) {
			cerr << "Error: program too large";
			exit(1);
		}
	}
	programSize = pc;
	pc = 1;
	ac = 0;
}

// simulate execution of RAM with given program and memory configuration.
// Notes:
//    1. Program may not terminate (if HLT is not executed)
//    2. Currently no error checking is performed.  Checks for valid program 
//       and memory addresses and illegal opcodes should be provided.
void RAM::execute()
{
	int x;
	OPCODES op;
	bool halted = false;

	while (!halted) {
		op = program[pc].opcode;
		switch (op) {
		case LDA:
			x = program[pc].operand;
			ac = memory[x];
			pc++;
			break;

		case LDI:
			x = program[pc].operand;
			ac = memory[memory[x]];
			pc++;
			break;

		case STA:
			x = program[pc].operand;
			memory[x] = ac;
			pc++;
			break;

		case ADD:
			x = program[pc].operand;
			ac = ac + memory[x];
			pc++;
			break;

		case SUB:
			x = program[pc].operand;
			ac = ac - memory[x];
			pc++;
			break;

		case JMP:
			x = program[pc].operand;
			pc = x;
			break;

		case JMZ:
			x = program[pc].operand;
			if (ac == 0)
				pc = x;
			else
				pc++;
			break;

		case JMN:
			x = program[pc].operand;
			if (ac < 0) 
				pc = x;
			else
				pc++;
			break;

		case STI:
			x = program[pc].operand;
			memory[memory[x]] = ac;
			pc++;
			break;

		case HLT:
			halted = true;
			break;
		}
	}
}

// Dump memory contents

void RAM::dump()
{
	cout << "RAM Memory Contents" << endl;
	cout << endl;  
	for (int i=1;i<=memorySize;i++)
		cout << i << "   " << memory[i] << endl;
}
