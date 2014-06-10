define dump_full_chain
    if $argc == 1
        set $start = $arg0 - 4
        set $current = $start
        set $size = *($current)
        set $counter = 0
        set $in_use = *($current + $size) & 1
        while $size != 0
            if mem == ($current+4)
                printf "Address: 0x%x; Previous: 0x%x; Size: 0x%x (%d); Data: 0x%x (InUse: %x)<- current\n", $current+4, (*($current-4)), (*($current)&0xFFFFFFFE), (*($current)&0xFFFFFFFE), *($current+4), $in_use
            else
                printf "Address: 0x%x; Previous: 0x%x; Size: 0x%x (%d); Data: 0x%x (InUse: %x)\n", $current+4, (*($current-4)), (*($current)&0xFFFFFFFE), (*($current)&0xFFFFFFFE), *($current+4), $in_use
            end

            set $current = $current + (*($current)&0xFFFFFFFE)
            set $size = (*($current)&0xFFFFFFFE)
            set $in_use = *($current + $size) & 1
            set $counter = $counter + 1
            if $counter > 30
                printf "you buggin\n"
                break
            end
        end
    end
end

break free
commands
    silent
    if mem==0x0
        continue
    else
        dump_full_chain $root
    end
end
