
prog_O1:     file format elf64-x86-64


Disassembly of section .init:

0000000000401000 <_init>:
  401000:	f3 0f 1e fa          	endbr64
  401004:	48 83 ec 08          	sub    rsp,0x8
  401008:	48 8b 05 d1 2f 00 00 	mov    rax,QWORD PTR [rip+0x2fd1]        # 403fe0 <__gmon_start__>
  40100f:	48 85 c0             	test   rax,rax
  401012:	74 02                	je     401016 <_init+0x16>
  401014:	ff d0                	call   rax
  401016:	48 83 c4 08          	add    rsp,0x8
  40101a:	c3                   	ret

Disassembly of section .plt:

0000000000401020 <.plt>:
  401020:	ff 35 ca 2f 00 00    	push   QWORD PTR [rip+0x2fca]        # 403ff0 <_GLOBAL_OFFSET_TABLE_+0x8>
  401026:	ff 25 cc 2f 00 00    	jmp    QWORD PTR [rip+0x2fcc]        # 403ff8 <_GLOBAL_OFFSET_TABLE_+0x10>
  40102c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
  401030:	f3 0f 1e fa          	endbr64
  401034:	68 00 00 00 00       	push   0x0
  401039:	e9 e2 ff ff ff       	jmp    401020 <_init+0x20>
  40103e:	66 90                	xchg   ax,ax

Disassembly of section .plt.sec:

0000000000401040 <__stack_chk_fail@plt>:
  401040:	f3 0f 1e fa          	endbr64
  401044:	ff 25 b6 2f 00 00    	jmp    QWORD PTR [rip+0x2fb6]        # 404000 <__stack_chk_fail@GLIBC_2.4>
  40104a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

Disassembly of section .text:

0000000000401080 <_start>:
  401080:	f3 0f 1e fa          	endbr64
  401084:	31 ed                	xor    ebp,ebp
  401086:	49 89 d1             	mov    r9,rdx
  401089:	5e                   	pop    rsi
  40108a:	48 89 e2             	mov    rdx,rsp
  40108d:	48 83 e4 f0          	and    rsp,0xfffffffffffffff0
  401091:	50                   	push   rax
  401092:	54                   	push   rsp
  401093:	45 31 c0             	xor    r8d,r8d
  401096:	31 c9                	xor    ecx,ecx
  401098:	48 c7 c7 80 11 40 00 	mov    rdi,0x401180
  40109f:	ff 15 33 2f 00 00    	call   QWORD PTR [rip+0x2f33]        # 403fd8 <__libc_start_main@GLIBC_2.34>
  4010a5:	f4                   	hlt
  4010a6:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
  4010ad:	00 00 00 

00000000004010b0 <_dl_relocate_static_pie>:
  4010b0:	f3 0f 1e fa          	endbr64
  4010b4:	c3                   	ret
  4010b5:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
  4010bc:	00 00 00 
  4010bf:	90                   	nop

00000000004010c0 <deregister_tm_clones>:
  4010c0:	b8 18 40 40 00       	mov    eax,0x404018
  4010c5:	48 3d 18 40 40 00    	cmp    rax,0x404018
  4010cb:	74 13                	je     4010e0 <deregister_tm_clones+0x20>
  4010cd:	b8 00 00 00 00       	mov    eax,0x0
  4010d2:	48 85 c0             	test   rax,rax
  4010d5:	74 09                	je     4010e0 <deregister_tm_clones+0x20>
  4010d7:	bf 18 40 40 00       	mov    edi,0x404018
  4010dc:	ff e0                	jmp    rax
  4010de:	66 90                	xchg   ax,ax
  4010e0:	c3                   	ret
  4010e1:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
  4010e5:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  4010ec:	00 00 00 00 

00000000004010f0 <register_tm_clones>:
  4010f0:	be 18 40 40 00       	mov    esi,0x404018
  4010f5:	48 81 ee 18 40 40 00 	sub    rsi,0x404018
  4010fc:	48 89 f0             	mov    rax,rsi
  4010ff:	48 c1 ee 3f          	shr    rsi,0x3f
  401103:	48 c1 f8 03          	sar    rax,0x3
  401107:	48 01 c6             	add    rsi,rax
  40110a:	48 d1 fe             	sar    rsi,1
  40110d:	74 11                	je     401120 <register_tm_clones+0x30>
  40110f:	b8 00 00 00 00       	mov    eax,0x0
  401114:	48 85 c0             	test   rax,rax
  401117:	74 07                	je     401120 <register_tm_clones+0x30>
  401119:	bf 18 40 40 00       	mov    edi,0x404018
  40111e:	ff e0                	jmp    rax
  401120:	c3                   	ret
  401121:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
  401125:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  40112c:	00 00 00 00 

0000000000401130 <__do_global_dtors_aux>:
  401130:	f3 0f 1e fa          	endbr64
  401134:	80 3d e5 2e 00 00 00 	cmp    BYTE PTR [rip+0x2ee5],0x0        # 404020 <completed.0>
  40113b:	75 13                	jne    401150 <__do_global_dtors_aux+0x20>
  40113d:	55                   	push   rbp
  40113e:	48 89 e5             	mov    rbp,rsp
  401141:	e8 7a ff ff ff       	call   4010c0 <deregister_tm_clones>
  401146:	c6 05 d3 2e 00 00 01 	mov    BYTE PTR [rip+0x2ed3],0x1        # 404020 <completed.0>
  40114d:	5d                   	pop    rbp
  40114e:	c3                   	ret
  40114f:	90                   	nop
  401150:	c3                   	ret
  401151:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
  401155:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  40115c:	00 00 00 00 

0000000000401160 <frame_dummy>:
  401160:	f3 0f 1e fa          	endbr64
  401164:	eb 8a                	jmp    4010f0 <register_tm_clones>
  401166:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
  40116d:	00 00 00 
  401170:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
  401177:	00 00 00 
  40117a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]

0000000000401180 <main>:
unsigned int checksum = 0;
int decrypt_ok = 0;

unsigned int rotl(unsigned int, int);

int main() {
  401180:	f3 0f 1e fa          	endbr64
  401184:	48 81 ec 98 00 00 00 	sub    rsp,0x98
  40118b:	64 48 8b 04 25 28 00 	mov    rax,QWORD PTR fs:0x28
  401192:	00 00 
  401194:	48 89 84 24 88 00 00 	mov    QWORD PTR [rsp+0x88],rax
  40119b:	00 
  40119c:	31 c0                	xor    eax,eax

    const int SID = 1230009;

    // LCG calc
    unsigned int x = (unsigned int)SID;
    for (int i = 0; i < N; i++) {
  40119e:	48 8d 3d bb 2e 00 00 	lea    rdi,[rip+0x2ebb]        # 404060 <v>
  4011a5:	48 8d b7 84 00 00 00 	lea    rsi,[rdi+0x84]
int main() {
  4011ac:	49 89 f8             	mov    r8,rdi
    unsigned int x = (unsigned int)SID;
  4011af:	b9 b9 c4 12 00       	mov    ecx,0x12c4b9
  4011b4:	90                   	nop
  4011b5:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  4011bc:	00 00 00 00 
        x = 1664525 * x + 1013904223U;
  4011c0:	69 c9 0d 66 19 00    	imul   ecx,ecx,0x19660d
  4011c6:	81 c1 5f f3 6e 3c    	add    ecx,0x3c6ef35f
        v[i] = (int)(((x >> 16) % 26) + 65);
  4011cc:	89 ca                	mov    edx,ecx
  4011ce:	c1 ea 10             	shr    edx,0x10
  4011d1:	89 d0                	mov    eax,edx
  4011d3:	48 69 c0 4f ec c4 4e 	imul   rax,rax,0x4ec4ec4f
  4011da:	48 c1 e8 23          	shr    rax,0x23
  4011de:	6b c0 1a             	imul   eax,eax,0x1a
  4011e1:	29 c2                	sub    edx,eax
  4011e3:	83 c2 41             	add    edx,0x41
  4011e6:	41 89 10             	mov    DWORD PTR [r8],edx
    for (int i = 0; i < N; i++) {
  4011e9:	49 83 c0 04          	add    r8,0x4
  4011ed:	49 39 f0             	cmp    r8,rsi
  4011f0:	75 ce                	jne    4011c0 <main+0x40>
  4011f2:	48 89 e2             	mov    rdx,rsp
  4011f5:	4c 8d 84 24 84 00 00 	lea    r8,[rsp+0x84]
  4011fc:	00 
  4011fd:	48 89 e0             	mov    rax,rsp
  401200:	48 89 f9             	mov    rcx,rdi
  401203:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
  40120a:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  401211:	00 00 00 00 
  401215:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  40121c:	00 00 00 00 
    }

    // keep original input
    int orig[N];
    for (int i = 0; i < N; i++) {
        orig[i] = v[i];
  401220:	44 8b 09             	mov    r9d,DWORD PTR [rcx]
  401223:	44 89 08             	mov    DWORD PTR [rax],r9d
    for (int i = 0; i < N; i++) {
  401226:	48 83 c1 04          	add    rcx,0x4
  40122a:	48 83 c0 04          	add    rax,0x4
  40122e:	4c 39 c0             	cmp    rax,r8
  401231:	75 ed                	jne    401220 <main+0xa0>
  401233:	48 89 f8             	mov    rax,rdi
  401236:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
  40123d:	00 00 00 
    }

    // doing XOR
    for (int i = 0; i < N; i++) {
        v[i] = v[i] ^ K;
  401240:	81 30 b9 00 00 00    	xor    DWORD PTR [rax],0xb9
    for (int i = 0; i < N; i++) {
  401246:	48 83 c0 04          	add    rax,0x4
  40124a:	48 39 f0             	cmp    rax,rsi
  40124d:	75 f1                	jne    401240 <main+0xc0>
  40124f:	48 89 f9             	mov    rcx,rdi
    }

    // checksum hesabı
    unsigned int c = 0;
  401252:	b8 00 00 00 00       	mov    eax,0x0
  401257:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
  40125e:	00 00 
        decrypt_ok = 1;
    } else { decrypt_ok = 0;}
}

unsigned int rotl(unsigned int v, int shift) {
    return (v << shift) | (v >> (32 - shift));
  401260:	d1 c0                	rol    eax,1
        c = rotl(c, 1) + (unsigned int)v[i];
  401262:	03 01                	add    eax,DWORD PTR [rcx]
    for (int i = 0; i < N; i++) {
  401264:	48 83 c1 04          	add    rcx,0x4
  401268:	48 39 f1             	cmp    rcx,rsi
  40126b:	75 f3                	jne    401260 <main+0xe0>
    checksum = c;
  40126d:	89 05 d1 2d 00 00    	mov    DWORD PTR [rip+0x2dd1],eax        # 404044 <checksum>
  401273:	48 89 f8             	mov    rax,rdi
  401276:	66 2e 0f 1f 84 00 00 	cs nop WORD PTR [rax+rax*1+0x0]
  40127d:	00 00 00 
        v[i] = v[i] ^ K;
  401280:	81 30 b9 00 00 00    	xor    DWORD PTR [rax],0xb9
    for (int i = 0; i < N; i++) {
  401286:	48 83 c0 04          	add    rax,0x4
  40128a:	48 39 f0             	cmp    rax,rsi
  40128d:	75 f1                	jne    401280 <main+0x100>
    int matches = 0;
  40128f:	b8 00 00 00 00       	mov    eax,0x0
  401294:	90                   	nop
  401295:	66 66 2e 0f 1f 84 00 	data16 cs nop WORD PTR [rax+rax*1+0x0]
  40129c:	00 00 00 00 
            matches++;
  4012a0:	8b 32                	mov    esi,DWORD PTR [rdx]
  4012a2:	39 37                	cmp    DWORD PTR [rdi],esi
  4012a4:	0f 94 c1             	sete   cl
  4012a7:	0f b6 c9             	movzx  ecx,cl
  4012aa:	01 c8                	add    eax,ecx
    for (int i = 0; i < N; i++) {
  4012ac:	48 83 c7 04          	add    rdi,0x4
  4012b0:	48 83 c2 04          	add    rdx,0x4
  4012b4:	4c 39 c2             	cmp    rdx,r8
  4012b7:	75 e7                	jne    4012a0 <main+0x120>
    if (matches == N) {
  4012b9:	83 f8 21             	cmp    eax,0x21
  4012bc:	0f 94 c0             	sete   al
  4012bf:	0f b6 c0             	movzx  eax,al
  4012c2:	89 05 78 2d 00 00    	mov    DWORD PTR [rip+0x2d78],eax        # 404040 <decrypt_ok>
}
  4012c8:	48 8b 84 24 88 00 00 	mov    rax,QWORD PTR [rsp+0x88]
  4012cf:	00 
  4012d0:	64 48 2b 04 25 28 00 	sub    rax,QWORD PTR fs:0x28
  4012d7:	00 00 
  4012d9:	75 0d                	jne    4012e8 <main+0x168>
  4012db:	b8 00 00 00 00       	mov    eax,0x0
  4012e0:	48 81 c4 98 00 00 00 	add    rsp,0x98
  4012e7:	c3                   	ret
  4012e8:	e8 53 fd ff ff       	call   401040 <__stack_chk_fail@plt>

00000000004012ed <rotl>:
unsigned int rotl(unsigned int v, int shift) {
  4012ed:	f3 0f 1e fa          	endbr64
    return (v << shift) | (v >> (32 - shift));
  4012f1:	89 f8                	mov    eax,edi
  4012f3:	89 f1                	mov    ecx,esi
  4012f5:	d3 c0                	rol    eax,cl
}
  4012f7:	c3                   	ret

Disassembly of section .fini:

00000000004012f8 <_fini>:
  4012f8:	f3 0f 1e fa          	endbr64
  4012fc:	48 83 ec 08          	sub    rsp,0x8
  401300:	48 83 c4 08          	add    rsp,0x8
  401304:	c3                   	ret
