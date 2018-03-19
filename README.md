# TuringScript
Language I made up to write Turing machines.

## How to use
Scripts can be ran by passing them as an argument to TuringVM.py (Python 3)

## Explanation
Within TuringScript files, every state is defined, followed by the inital tape configuration (optional) and tape head position (also optional)

**States are defined as:**
```
[state name][start flag]{
[contents]
}
```
where:

- `[state name]` is a label that the state is identified by.

- `[start flag]` is either nothing or an asterisk `*`. An asterisk indicates that the state is the start state of the machine.

- `[contents]` is a list of instructions for the state.

Instructions are defined within the scope of their parent state, and describe how the machine will act when reading characters in the given state.

**Instructions are defined as:**
```
[read character]:[write character],[move direction],[new state]
```
where:

- `[read character]` is the character that upon being read will cause the instruction to execute. Consists of a single character surrounded by quotation marks.

- `[write character]` is the character that the machine will write upon execution of the instruction. Consists of a single character surrounded by quotation marks.

- `[move direction]` is the direction that the 'tape head' of the machine will move upon execution of the instruction. 'Left' and 'right' are represented by `R` and `L`.

- `[new state]` is the label of a state in the machine. To accept the string, `accept` can be used instead of a state label. 

**The initial configuration of the tape and tape head can be defined by including the following at the end of the script:**
```
[tape contents]
[tape head position]
```
where:

`[tape contents]` is a string of characters bounded by quotation marks, or nothing (indicating tape is empty).

`[tape head position]` is the inital position of the 'tape head' on the tape, represented by an integer, with 0 being the first character in `[tape contents]`. If no value is supplied, then the inital position is set to 0.

## Example Script
```
q0*{
"1": "1", R, q0
"0": "0", R, q0
" ": " ", L, q1
}
q1{
"1": "0", L, q1
"0": "1", L, accept
" ": "1", R, accept
}
"1010101010"
```

This script adds 1 to a binary number on the tape.
