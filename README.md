windbgdiff
==========

This script compares the instructions between two WinDbg debugging sessions.

# Usage

Debug a program twice, saving the WinDbg console output from each into separate
files. Then compare them like so:

```bash
python3 windbgdiff.py examples/a1 examples/a2
```

You should get some output like the following:

```bash
0x400000  mov eax,dword ptr [ebp+30h]   0x400000  mov eax,dword ptr [ebp+30h]
0x400001  cmp eax,8h                    0x400001  cmp eax,8h
0x400002  jle (00400005)                0x400002  jle (00400005)
0x400005  dec edx
                                        0x400003  inc edx
                                        0x400004  jmp (00400006)
0x400006  add ebx, edx                  0x400006  add ebx, edx
```
