section .text
dump:
    mov     r9, -3689348814741910323
    sub     rsp, 40
    mov     BYTE [rsp+31], 10
    lea     rcx, [rsp+30]

.L2:
    mov     rax, rdi
    lea     r8, [rsp+32]
    mul     r9
    mov     rax, rdi
    sub     r8, rcx
    shr     rdx, 3
    lea     rsi, [rdx+rdx*4]
    add     rsi, rsi
    sub     rax, rsi
    add     eax, 48
    mov     BYTE [rcx], al
    mov     rax, rdi
    mov     rdi, rdx
    mov     rdx, rcx
    sub     rcx, 1
    cmp     rax, 9
    ja      .L2
    lea     rax, [rsp+32]
    mov     edi, 1
    sub     rdx, rax
    xor     eax, eax
    lea     rsi, [rsp+32+rdx]
    mov     rdx, r8
    mov     rax, 1
    syscall
    add     rsp, 40
    ret

printStr:
    mov       rax, 1                  ; system call for write
    mov       rdi, 1                  ; file handle 1 is stdout
    mov       rsi, str                ; address of string to output
    mov       rdx, [strlen]           ; number of bytes
    syscall

    ret   


global _start
_start:
    ;print msg
    mov rax, `tests\n`
    mov rbx, 8
    mov [str], rax
    mov [strlen], rbx
    call printStr

    mov       rax, 60
    xor       rdi, rdi
    syscall

section .data
str: db "maxLen=100, aaaaaaaamaxLen=100, aaaaaaaamaxLen=100, aaaaaaaamaxLen=100, aaaaaaaamaxLen=100, aaaaaaaa", 10
strlen: db 100
