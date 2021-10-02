#include <fstream>
#include <string>
#include <ctime>
using namespace std;

string out, typ, cwd;

/**
 * path utils
 * */
string get_typ(string &t) {
	int len = t.length();
	for (int i = len-1; i >= 0; i--) {
		if (t[i] == '.') return t.substr(i, len-i);
	}
	return ".cpp";
}

string get_cwd(string t) {
	int len = t.length();
	for (int i = len-1; i >= 0; i--) {
		if (t[i] == '\\') return t.substr(0, i+1);
	}
	return "";
}


/**
 * template generator
 * */
void gen_template() {
	ifstream tsrc(cwd + "template\\t" + typ);
	ofstream csrc(cwd + "template\\c" + typ);
	//
	string line;
	time_t t = time(0);
	while (getline(tsrc, line)) {
		// maybe we should add more macro in the future
		if (line == "{{date}}") {
			csrc << "created:\t" << ctime(&t);
		} else {
			csrc << line << "\n";
		}
	}
}


/**
 * drivers
 * */
int main(int argc, char const *argv[]) {
	cwd = get_cwd(argv[0]);
	out = argv[1];
	typ = get_typ(out);
	//
	gen_template();
	string exec = "copy " + cwd + "template\\c" + typ + " " + out;
	system(exec.c_str());
	return 0;
}
