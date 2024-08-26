"""Module for converting NFA to DFA."""

from typing import Set, Dict, Tuple

class NfaToDfaConverter:
    """Converts NFA to DFA"""

    def __init__(self, config: Dict[str, Set[str] | Dict[Tuple[str, str], Set[str]] | str]):
        self.states = config['states']
        self.alphabet_list = config['alphabet_list']
        self.transition_functions = config['transition_functions']
        self.start_state = config['start_state']
        self.accept_states = config['accept_states']

    def execute(self):
        """Executes the conversion from NFA to DFA and returns the DFA components."""
        dfa_start_state = self.epsilon_closure({self.start_state}, self.transition_functions)
        result = self.search_dfa_state_and_transitions(dfa_start_state)

        return {
            'dfa_states': result['dfa_states'],
            'dfa_transition_functions': result['dfa_transitions'],
            'dfa_start_states': dfa_start_state,
            'dfa_accept_states': result['dfa_accept_states'],
        }

    def epsilon_closure(self, states: Set[str], transitions: Dict[Tuple[str, str], Set[str]]):
        """Calculate the epsilon-closure of the given states."""
        closure = set(states)
        stack = list(states)
        while stack:
            current_state = stack.pop()
            for next_state in transitions.get((current_state, 'ε'), []):
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
        return closure

    def search_dfa_state_and_transitions(self, dfa_start_states: Set[str]):
        """Search and build the DFA states and transitions based on NFA transitions."""
        dfa_states = []
        dfa_transitions = {}
        unmarked_states_list = [dfa_start_states]

        while unmarked_states_list:
            states = unmarked_states_list.pop()
            dfa_states.append(states)
            for alphabet in self.alphabet_list:
                if alphabet == 'ε':
                    continue
                next_states = set()
                for state in states:
                    if (state, alphabet) in self.transition_functions:
                        next_states.update(
                            self.epsilon_closure(
                                self.transition_functions[(state, alphabet)],
                                self.transition_functions
                            )
                        )
                if not next_states:
                    next_states.add('φ')
                dfa_transitions[(", ".join(sorted(states)), alphabet)] = next_states
                if next_states not in dfa_states and next_states not in unmarked_states_list:
                    unmarked_states_list.append(next_states)

        dfa_accept_states = [
            state for state in dfa_states if any(s in self.accept_states for s in state)
        ]
        return {
            "dfa_states": dfa_states,
            "dfa_accept_states": dfa_accept_states,
            "dfa_transitions": dfa_transitions
        }
