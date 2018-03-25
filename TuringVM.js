var LEFT = -1
var RIGHT = 1

class TuringMachine{
	constructor(){
		this.tape = " ";
		this.position = 0;
		this.currentState = null;
		this.states = {};
	}

	addState(name){
		this.states[name] = new State(name);
	}

	addInstruction(stateName, readSymbol, writeSymbol, moveDirection, newStateName){
		if(newStateName == "accept"){
			this.states[stateName].addInstruction(readSymbol, writeSymbol, moveDirection, newStateName);
		}
		else{
			this.states[stateName].addInstruction(readSymbol, writeSymbol, moveDirection, this.states[newStateName]);
		}
	}

	setConfiguration(tape, position, stateName){
		this.tape = tape;
		this.position = position;
		this.currentState = this.states[stateName];
	}

	readNextSymbol(){
		var action = this.currentState.readSymbol(this.tape.charAt(this.position));
		if(action == "reject"){
			this.currentState = "reject";
		}
		else{
			if(this.position == 0){
				this.tape = action[0] + this.tape.substr(this.position + 1);
			}
			else{
				this.tape = this.tape.substr(0,this.positon).slice(0,-1) + action[0] + this.tape.substr(this.position + 1);
			}
			this.position += action[1];
			if(this.position == -1){
				this.tape = " " + this.tape;
				this.position += 1;
			}
			else if(this.position == this.tape.length){
				this.tape += " ";
			}
			this.currentState = action[2];
		}
	}

	run(trace = false){
		var initalTape = this.tape;
		console.log("initial tape: '" + this.initialTape + "'");
		while(this.currentState != "accept" && this.currentState != "reject"){
			this.readNextSymbol();
			if(trace){
				console.clear();
				console.log("initial tape: '" + this.initialTape + "'");
				console.log(this.tape);
				console.log(" ".repeat(this.position) + "^");
				var currentTime = new Date().getTime();
				while(new Date().getTime() < currentTime + 100){};
			}
		}
		console.log("Final tape: '" + this.tape.trim() + "'");
		console.log("Final state: " + this.currentState);
	}
}

class State{
	constructor(name){
		this.instructions = {};
		this.name = name;
	}

	addInstruction(readSymbol, writeSymbol, moveDirection, newState){
		this.instructions[readSymbol] = [writeSymbol, moveDirection, newState];
	}

	readSymbol(symbol){
		if(Object.keys(this.instructions).indexOf(symbol) > -1){
			return this.instructions[symbol];
		}
		return "reject";
	}
}

tm = new TuringMachine();
tm.addState("b");
tm.addState("c");
tm.addState("e");
tm.addState("f");
tm.addInstruction("b", " ", "0", RIGHT, "c");
tm.addInstruction("c", " ", " ", RIGHT, "e");
tm.addInstruction("e", " ", "1", RIGHT, "f");
tm.addInstruction("f", " ", " ", RIGHT, "b");
tm.setConfiguration(" ", 0, "b")
tm.run(trace = true);