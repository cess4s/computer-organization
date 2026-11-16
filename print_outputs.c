/* Dogrulama araci (proje kodu degil): programi calistirir ve Y7 ciktilarini ekrana basar.
   Derleme: gcc -O0 -no-pie -c -Dmain=proje_main main.c -o main_renamed.o
            gcc -O0 -no-pie -c print_outputs.c -o print_outputs.o
            gcc -no-pie main_renamed.o print_outputs.o -o print_outputs
   Calistirma: ./print_outputs */
#include <stdio.h>
extern unsigned int checksum;
extern int decrypt_ok;
int proje_main(void);
int main(void) {
    proje_main();
    printf("checksum   @ %p = 0x%08x\n", (void*)&checksum, checksum);
    printf("decrypt_ok @ %p = %d\n", (void*)&decrypt_ok, decrypt_ok);
    return 0;
}
