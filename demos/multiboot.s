
#include "multiboot.h"

     .section  .multiboot

    multiboot:
     required:
        magic: .long 0x1BADB002  // multiboot v.1
        flags: .long (1<<0|1<<2) // align 4K | videoinit
     checksum: .long 0x1BADB002  //
       memory:
  header_addr: .long 0
    load_addr: .long 0
load_end_addr: .long 0
 bss_end_addr: .long 0
   entry_addr: .long 0
 askvideomode:
    mode_type: .long 0           // ask linear buffer
        width: .long 640
       height: .long 480
        depth: .long 24

