
#include <math.h>
#include <iostream>
using namespace std;


// code by:
// https://stackoverflow.com/questions/3018313/algorithm-to-convert-rgb-to-hsv-and-hsv-to-rgb-in-range-0-255-for-both

typedef struct {
    double r;       // a fraction between 0 and 1
    double g;       // a fraction between 0 and 1
    double b;       // a fraction between 0 and 1
} rgb;

typedef struct {
    double h;       // angle in degrees
    double s;       // a fraction between 0 and 1
    double v;       // a fraction between 0 and 1
} hsv;

rgb hsv2rgb(hsv in)
{
    double      hh, p, q, t, ff;
    long        i;
    rgb         out;

    if(in.s <= 0.0) {       // < is bogus, just shuts up warnings
        out.r = in.v;
        out.g = in.v;
        out.b = in.v;
        return out;
    }
    hh = in.h;
    if(hh >= 360.0) hh = 0.0;
    hh /= 60.0;
    i = (long)hh;
    ff = hh - i;
    p = in.v * (1.0 - in.s);
    q = in.v * (1.0 - (in.s * ff));
    t = in.v * (1.0 - (in.s * (1.0 - ff)));

    switch(i) {
    case 0:
        out.r = in.v;
        out.g = t;
        out.b = p;
        break;
    case 1:
        out.r = q;
        out.g = in.v;
        out.b = p;
        break;
    case 2:
        out.r = p;
        out.g = in.v;
        out.b = t;
        break;

    case 3:
        out.r = p;
        out.g = q;
        out.b = in.v;
        break;
    case 4:
        out.r = t;
        out.g = p;
        out.b = in.v;
        break;
    case 5:
    default:
        out.r = in.v;
        out.g = p;
        out.b = q;
        break;
    }
    return out;     
}

/**
 * from now on is my stuff
 * */

const double FIXED_SATURATION = 0.80;
const double FIXED_BRIGHTNESS = 0.80;

char hex_digits[] = {
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f',
};

string to_hex(int a) {
    string res = "";
    //
    while (a > 0) {
        res = hex_digits[a % 16] + res;
        a /= 16;
    }
    if (res.length() == 1) res = '0' + res;
    //
    return res;
}

string rgb_to_hex(rgb c) {
    return to_hex(c.r * 255) +
           to_hex(c.g * 255) + 
           to_hex(c.b * 255);
}

int main() {
    // inp
    cout << "text:\n";
    string s; getline(cin, s);
    int len = s.length();
    // preferences
    double hue_start, hue_range;
    double hue_lim = 360.0;
    cout << "hue degree start [0;1]: "; scanf("%lf", &hue_start);
    cout << "hue degree range [0;1]: "; scanf("%lf", &hue_range);
    // calc
    string res;
    hsv hsv_value;
    hsv_value.s = FIXED_SATURATION;
    hsv_value.v = FIXED_BRIGHTNESS;
    for (int i = 0; i < len; i++) {
        double one = 1.0;
        double h = modf(hue_start + ((double) i * hue_range / len), &one) * hue_lim;
        // prepare hsv object
        hsv_value.h = h;
        // trans
        rgb rgb_value = hsv2rgb(hsv_value);
        string hex_code = rgb_to_hex(rgb_value);
        // out
        string cr = "[color=#" + hex_code + "]" + s.at(i) + "[/color]";
        res = res + cr;
    }
    // returns
    string cmd = "xsel --clipboard \"" + res + "\"";
    system(cmd.c_str());
    cout << "copied to clipboard!\n";
    return 0;
}
