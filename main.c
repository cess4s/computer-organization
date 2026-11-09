/* Emir Çalışkan, 5001230009(1230009), G3 */
#define N 33
#define K 185
int v[N];
unsigned int checksum = 0;
int decrypt_ok = 0;

unsigned int rotl(unsigned int, int);

int main() {

    const int SID = 1230009;

    // LCG calc
    unsigned int x = (unsigned int)SID;
    for (int i = 0; i < N; i++) {
        x = 1664525 * x + 1013904223U;
        v[i] = (int)(((x >> 16) % 26) + 65);
    }

    // keep original input
    int orig[N];
    for (int i = 0; i < N; i++) {
        orig[i] = v[i];
    }

    // doing XOR
    for (int i = 0; i < N; i++) {
        v[i] = v[i] ^ K;
    }

    // checksum hesabı
    unsigned int c = 0;
    for (int i = 0; i < N; i++) {
        c = rotl(c, 1) + (unsigned int)v[i];
    }
    checksum = c;

    // decrypt
    for (int i = 0; i < N; i++) {
        v[i] = v[i] ^ K;
    }

    // check if its same with orig
    int matches = 0;
    for (int i = 0; i < N; i++) {
        if (v[i] == orig[i]) {
            matches++;
        }
    }
    if (matches == N) {
        decrypt_ok = 1;
    } else { decrypt_ok = 0;}
}

unsigned int rotl(unsigned int v, int shift) {
    return (v << shift) | (v >> (32 - shift));
}
