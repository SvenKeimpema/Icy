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
global _start
_start:
    jmp L1
L1:
    mov rax, [b]
    mov rbx, 0
    mov rcx, 0
    mov rdx, 1
    cmp rbx, rax
    cmovg rcx, rdx
    push rcx
    pop rax
    test rax, rax
    jz L3
    jmp L2
L2:
    mov rax, [b]
    push rax
    mov rax, [b]
    mov rbx, 1
    sub rbx, rax
    push rbx
    pop rax
    pop rbx
    mov [b], rax
    jmp L1
L3:
    mov       rax, 60
    xor       rdi, rdi
    syscall

section .data
    b: dq 1000000000
