#include <string>
#include <iostream>
using namespace std;

string src, folder, cmdc;

void getfolder() {
	for (int i = src.length() - 1; i >= 0; i--) {
		if (src.at(i) == '\\') {
			folder = src.substr(0, i+1);
			return;
		}
	}
}

void getinp() {
	cout << "source file:\n";
	getline(cin, src);
	getfolder();
	// .\docto.exe -f "{src}" -O "{save_folder}" -T wdFormatPDF -OX .pdf
	cmdc = ".\\docto.exe -f \"" + src + "\" -O \"" + folder + "\" -T wdFormatPDF -OX .pdf";
}

void report() {
	cout << "execute: " << cmdc << endl;
	cout << "converting..." << endl;
}

int main() {
	getinp();
	report();
	system(cmdc.c_str());
	//
	return 0;
}
