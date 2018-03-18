# TuringScript
Language I made up to write Turing machines.

## How to use
Scripts can be ran by passing them as an argument to TuringVM.py (Python 3)

## Explanation
Within TuringScript files, every state is defined, followed by the inital tape configuration (optional) and tape head position (also optional)

States are defined as:
```
[state name][start flag]{
[contents]
}
```
where:

`[state name]` is a label that the state is identified by.

`[start flag]` is either nothing or an asterisk `*`. An asterisk indicates that the state is the start state of the machine.

`[contents]` is a list of instructions for the state.
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
