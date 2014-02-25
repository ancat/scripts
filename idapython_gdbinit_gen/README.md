# gdbinit_gen.py

This script just generates a .gdbinit for gdb. It sets aliases for anything
that has a name associated with an address (for example, a function renamed
from sub_8048DB0 to some_function). Using this gdbinit, you can break on 
functions or read memory using their names instead of addresses.

## Example Generated .gdbinit

```
set $_init_proc=0x80486bc
set $_printf=0x80486f0
set $_fflush=0x8048700
set $__exit=0x8048710
set $_wattr_on=0x8048720
set $_waddch=0x8048730
set $_gettimeofday=0x8048740
set $_init_pair=0x8048750
set $_wrefresh=0x8048760
set $_initscr=0x8048770
set $_start_color=0x8048780
set $_wattr_off=0x8048790
set $_puts=0x80487a0
set $___gmon_start__=0x80487b0
set $_strtoul=0x80487c0
set $_printw=0x80487d0
set $___libc_start_main=0x80487e0
set $_endwin=0x80487f0
set $_wgetch=0x8048800
set $_noecho=0x8048810
set $___isoc99_scanf=0x8048820
set $_wmove=0x8048830
set $start=0x8048840
set $play_game=0x8049283
set $main_thing=0x8049748
set $nullsub_1=0x8049930
set $_term_proc=0x8049934
set $_IO_stdin_used=0x804994c
set $aUseHLToMovePre=0x8049950
set $aEndPressEnterT=0x8049975
set $s=0x804998f
set $format=0x8049999
set $__gmon_start___ptr=0x804affc
set $stdscr=0x804b080
set $stdout=0x804b0a0
set $printf=0x804b4a8
set $fflush=0x804b4ac
set $_exit=0x804b4b0
set $wattr_on=0x804b4b4
set $waddch=0x804b4b8
set $gettimeofday=0x804b4bc
set $init_pair=0x804b4c0
set $wrefresh=0x804b4c4
set $initscr=0x804b4c8
set $start_color=0x804b4cc
set $wattr_off=0x804b4d0
set $puts=0x804b4d4
set $strtoul=0x804b4d8
set $printw=0x804b4dc
set $__libc_start_main=0x804b4e0
set $endwin=0x804b4e4
set $wgetch=0x804b4e8
set $noecho=0x804b4ec
set $__isoc99_scanf=0x804b4f0
set $wmove=0x804b4f4
```

## Using the .gdbinit

```
gdb-peda$ source .gdbinit
gdb-peda$ break *$play_game
Breakpoint 1 at 0x8049283
gdb-peda$ run
Starting program: /home/jesus/test/4stone
[----------------------------------registers-----------------------------------]
EAX: 0x804c190 --> 0x0
EBX: 0xf7f7c000 --> 0x1a5d7c
ECX: 0xff
EDX: 0x0
ESI: 0x0
EDI: 0x0
EBP: 0xffffd9c8 --> 0x0
ESP: 0xffffd97c --> 0x804977f (mov    DWORD PTR [esp+0x24],eax)
EIP: 0x8049283 (push   ebp)
EFLAGS: 0x282 (carry parity adjust zero SIGN trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x804927c:   call   0x8048790 <wattr_off@plt>
   0x8049281:   leave
   0x8049282:   ret
=> 0x8049283:   push   ebp
   0x8049284:   mov    ebp,esp
   0x8049286:   sub    esp,0x38
   0x8049289:   mov    DWORD PTR [ebp-0x20],0x0
   0x8049290:   mov    DWORD PTR [ebp-0x18],0x0
[------------------------------------stack-------------------------------------]
0000| 0xffffd97c --> 0x804977f (mov    DWORD PTR [esp+0x24],eax)
0004| 0xffffd980 --> 0xffffd9a8 --> 0x530beaf6
0008| 0xffffd984 --> 0x0
0012| 0xffffd988 --> 0x0
0016| 0xffffd98c --> 0x80486c5 (<_init+9>:  add    ebx,0x293b)
0020| 0xffffd990 --> 0xf7f7c3e4 --> 0xf7f7d1e0 --> 0x0
0024| 0xffffd994 --> 0xd ('\r')
0028| 0xffffd998 --> 0x804b000 --> 0x804af04 --> 0x1
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value

Breakpoint 1, 0x08049283 in ?? ()
```
