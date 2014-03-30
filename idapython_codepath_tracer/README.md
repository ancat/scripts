# tracer.py

A simple script that pops out a gdbinit file that allows you to track code
coverage. It's helpful in figuring out what functionality goes down which path,
making figuring out what to reverse a little easier.

## Usage

Right now, there's no interface so you need to edit the file to do what you
want. It should be fairly straight forward, though.

There are three "modes":

- `BASIC_FUNCTION_TRACE`: Track which functions are called
- `SPECIFIC_FUNCTION_TRACE`: Track all the codepaths within a specific function
- `FULL_FUNCTION_TRACE`: Track every codepath in every function

Steps:

1. Select a mode
2. Load up tracer.py
3. Save gdbinit file somewhere
4. Run binary with `gdb -x gdbinit ./binary`
5. Load `crunchatize.py` with the resulting `traces.txt` file. 

## Future

- Different debugger support
- Show diffs for multiple executions (paimei process stalker style)

