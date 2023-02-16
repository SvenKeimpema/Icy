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
    syscall
    ret   





global _start
_start:
    mov rax, [a]
    mov rbx, [b]
    mov rcx, 0
    mov rdx, 1
    cmp rax, rbx
    cmovl rcx, rdx
    push rcx
    pop rax
    test rax, rax
    jz L4
    mov rsi, name0
    mov rdx, [name0len]
    call printStr
    jmp L4
L4:
    mov rax, [a]
    mov rbx, [b]
    add rax, rbx
    mov [b], rax
    jmp L6
L6:
    mov rax, [b]
    mov rbx, [a]
    cmp rax, rbx
    jg L7
    jmp L9
L7:
    mov rdi, [b]
    call dump
    mov rax, [b]
    mov rbx, 1
    sub rax, rbx
    mov [b], rax
    jmp L6
L9:
    mov       rax, 60
    xor       rdi, rdi
    syscall

section .data
    a: dq 5
    b: dq 6
    name0: db `a is less than b\n`
    name0len: dq 18
