
// hsv to rgb formula given by:
// https://www.rapidtables.com/convert/color/hsv-to-rgb.html

#include <math.h>
#include <string>
#include <iostream>
using namespace std;

/**
 * utils
 * */
const double FIXED_SATURATION = 0.80;
const double FIXED_BRIGHTNESS = 1.00;

char hex_digits[] = {
	'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f',
};
string dec_to_hex(int a) {
	string res = "";
	//
	while (a > 0) {
		res += hex_digits[a % 16];
		a /= 16;
	}
	if (res.length() == 1) res = '0' + res;
	//
	return res;
}

string hsv_to_rgb(double h, double s, double v) {
	/**
	 * params:
	 * 0 <= h < 360
	 * 0 <= s <= 1
	 * 0 <= v <= 1
	 * */
	double  temp = 2.0;
	double  c = v*s,
			x = c * (1 - abs(modf((h / 60.0), &temp) - 1)),
			m = v - c;
	double  r, g, b;
	//
	if (h < 0) {
		r = 0; g = 0; b = 0;
	} else if (h < 60) {
		r = c; g = x; b = 0;
	} else if (h < 120) {
		r = x; g = c; b = 0;
	} else if (h < 180) {
		r = 0; g = c; b = x;
	} else if (h < 240) {
		r = 0; g = x; b = c;
	} else if (h < 300) {
		r = x; g = 0; b = c;
	} else if (h < 360) {
		r = c; g = 0; b = x;
	} else {
		r = 0; g = 0; b = 0;
	}
	//
	return dec_to_hex((r+m)*255) + 
		   dec_to_hex((g+m)*255) + 
		   dec_to_hex((b+m)*255);
}

/**
 * drivers
 * */
int main() {
	// inp
	string s; getline(cin, s);
	int len = s.length();
	// calc
	for (int i = 0; i < len; i++) {
		double h = ((double) i / len) * 360.0;
		string v = hsv_to_rgb(h, FIXED_SATURATION, FIXED_BRIGHTNESS);
		// out
		cout << "[color=#" << v << "]" << s.at(i) << "[/color]";
	}
	// returns
	cin >> s;
	return 0;
}
