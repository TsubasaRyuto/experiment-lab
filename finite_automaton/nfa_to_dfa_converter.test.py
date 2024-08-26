'''
This module tests the NFA to DFA conversion using the NfaToDfaConverter class.
'''

import unittest
from nfa_to_dfa_converter import NfaToDfaConverter

class TestNfaToDfaConverter(unittest.TestCase):
    '''
    Test cases for verifying the correctness of the NFA to DFA conversion process.
    '''
    def test_case1(self):
        '''Tests a simple linear NFA conversion.'''
        states = { 'q0', 'q1', 'q2' }
        alphabet_list = { 'a', 'b' }
        transitions = {
            ('q0', 'a'): { 'q1' },
            ('q1', 'b'): { 'q2' },
        }
        start_state = 'q0'
        accept_states = { 'q2' }

        converter = NfaToDfaConverter({
            'states': states,
            'alphabet_list': alphabet_list,
            'transition_functions': transitions,
            'start_state': start_state,
            'accept_states': accept_states
        })
        result = converter.execute()

        expected_dfa_states = [ { 'q0' }, { 'q1' }, { 'q2' }, { 'φ' }]
        expected_dfa_transitions = {
            ('q0', 'a'): { 'q1' },
            ('q0', 'b'): { 'φ' },
            ('q1', 'a'): { 'φ' },
            ('q1', 'b'): { 'q2' },
            ('q2', 'a'): { 'φ' },
            ('q2', 'b'): { 'φ' },
            ('φ', 'a'): { 'φ' },
            ('φ', 'b'): { 'φ' }
        }
        expected_dfa_accept_states = [{ 'q2' }]

        self.assertEqual(
            sorted([sorted(list(s)) for s in result['dfa_states']]),
            sorted([sorted(list(s)) for s in expected_dfa_states])
        )
        self.assertEqual(result['dfa_transition_functions'], expected_dfa_transitions)
        self.assertEqual(result['dfa_accept_states'], expected_dfa_accept_states)

    def test_case2(self):
        '''
        Tests the conversion of a specific NFA to its corresponding DFA and validates
        the states, transitions, and accept states of the resulting DFA.
        '''
        # NFAの定義
        states = { 'q1', 'q2', 'q3' }
        alphabet_list = { 'a', 'b' }
        transitions = {
            ('q1', 'ε'): { 'q2' },
            ('q1', 'a'): { 'q3' },
            ('q2', 'a'): { 'q1' },
            ('q3', 'a'): { 'q2' },
            ('q3', 'b'): { 'q2', 'q3' },
        }
        start_state = 'q1'
        accept_states = { 'q2' }

        # 変換器の初期化
        converter = NfaToDfaConverter({
            'states': states,
            'alphabet_list': alphabet_list,
            'transition_functions': transitions,
            'start_state': start_state,
            'accept_states': accept_states
        })
        result = converter.execute()

        # DFAの状態、遷移関数、受理状態のテスト
        expected_dfa_start_states = { 'q1', 'q2' }
        expected_dfa_states = [
            { 'q1', 'q2' },
            { 'q1', 'q2', 'q3' },
            { 'q2', 'q3' },
            { 'φ' }
        ]
        expected_dfa_transitions = {
            ('q1, q2', 'a'): { 'q1', 'q2', 'q3' },
            ('q1, q2', 'b'): { 'φ' },
            ('q1, q2, q3', 'a'): { 'q1', 'q2', 'q3' },
            ('q1, q2, q3', 'b'): { 'q2', 'q3' },
            ('q2, q3', 'a'): { 'q1', 'q2' },
            ('q2, q3', 'b'): { 'q2', 'q3' },
            ('φ', 'a'): { 'φ' },
            ('φ', 'b'): { 'φ' }
        }
        expected_dfa_accept_states = [
            { 'q1', 'q2' },
            { 'q1', 'q2', 'q3' },
            { 'q2', 'q3' }
        ]

        self.assertEqual(
            sorted([sorted(list(s)) for s in result['dfa_states']]),
            sorted([sorted(list(s)) for s in expected_dfa_states])
        )
        self.assertEqual(result['dfa_transition_functions'], expected_dfa_transitions)
        self.assertEqual(result['dfa_start_states'], expected_dfa_start_states)
        self.assertEqual(result['dfa_accept_states'], expected_dfa_accept_states)

    def test_case3(self):
        '''
        Tests the conversion of a specific NFA to its corresponding DFA and validates
        the states, transitions, and accept states of the resulting DFA.
        '''
        # NFAの定義
        states = { 'q0', 'q1', 'q2' }
        alphabet_list = { '1', '0' }
        transitions = {
            ('q0', 'ε'): { 'q2' },
            ('q0', '1'): { 'q1' },
            ('q1', '0'): { 'q1', 'q2' },
            ('q1', '1'): { 'q2' },
            ('q2', '0'): { 'q0' },
            ('φ', '0'): { 'φ' },
            ('φ', '1'): { 'φ' }
        }
        start_state = 'q0'
        accept_states = { 'q0' }

        # 変換器の初期化
        converter = NfaToDfaConverter({
            'states': states,
            'alphabet_list': alphabet_list,
            'transition_functions': transitions,
            'start_state': start_state,
            'accept_states': accept_states
        })
        result = converter.execute()

        # DFAの状態、遷移関数、受理状態のテスト
        expected_dfa_start_states = { 'q0', 'q2' }
        expected_dfa_states = [
            { 'q1' },
            { 'q2' },
            { 'q0', 'q2' },
            { 'q1', 'q2' },
            { 'q0', 'q1', 'q2' },
            { 'φ' }
        ]
        expected_dfa_transitions = {
            ('q0, q1, q2', '0'): { 'q0', 'q1', 'q2' },
            ('q0, q1, q2', '1'): { 'q1', 'q2' },
            ('q0, q2', '0'): { 'q0', 'q2' },
            ('q0, q2', '1'): { 'q1' },
            ('q1', '0'): { 'q1', 'q2' },
            ('q1', '1'): { 'q2' },
            ('q1, q2', '0'): { 'q0', 'q1', 'q2' },
            ('q1, q2', '1'): {'q2'},
            ('q2', '0'): { 'q0', 'q2' },
            ('q2', '1'): { 'φ' },
            ('φ', '0'): { 'φ' },
            ('φ', '1'): { 'φ' }
        }
        expected_dfa_accept_states = [
            { 'q0', 'q2' },
            { 'q0', 'q1', 'q2' }
        ]

        self.assertEqual(
            sorted([sorted(list(s)) for s in result['dfa_states']]),
            sorted([sorted(list(s)) for s in expected_dfa_states])
        )
        self.assertEqual(result['dfa_transition_functions'], expected_dfa_transitions)
        self.assertEqual(result['dfa_start_states'], expected_dfa_start_states)
        self.assertEqual(result['dfa_accept_states'], expected_dfa_accept_states)

if __name__ == '__main__':
    unittest.main()
    def test_case3(self):
        '''
        Tests the conversion of a specific NFA to its corresponding DFA and validates
        the states, transitions, and accept states of the resulting DFA.
        '''
        # NFAの定義
        states = { 'q0', 'q1', 'q2' }
        alphabet_list = { '1', '0' }
        transitions = {
            ('q0', 'ε'): { 'q2' },
            ('q0', '1'): { 'q1' },
            ('q1', '0'): { 'q1', 'q2' },
            ('q1', '1'): { 'q2' },
            ('q2', '0'): { 'q0' },
            ('φ', '0'): { 'φ' },
            ('φ', '1'): { 'φ' }
        }
        start_state = 'q0'
        accept_states = { 'q0' }

        # 変換器の初期化
        converter = NfaToDfaConverter({
            'states': states,
            'alphabet_list': alphabet_list,
            'transition_functions': transitions,
            'start_state': start_state,
            'accept_states': accept_states
        })
        result = converter.execute()

        # DFAの状態、遷移関数、受理状態のテスト
        expected_dfa_start_states = { 'q0', 'q2' }
        expected_dfa_states = [
            { 'q1' },
            { 'q2' },
            { 'q0', 'q2' },
            { 'q1', 'q2' },
            { 'q0', 'q1', 'q2' },
            { 'φ' }
        ]
        expected_dfa_transitions = {
            ('q0, q1, q2', '0'): { 'q0', 'q1', 'q2' },
            ('q0, q1, q2', '1'): { 'q1', 'q2' },
            ('q0, q2', '0'): { 'q0', 'q2' },
            ('q0, q2', '1'): { 'q1' },
            ('q1', '0'): { 'q1', 'q2' },
            ('q1', '1'): { 'q2' },
            ('q1, q2', '0'): { 'q0', 'q1', 'q2' },
            ('q1, q2', '1'): {'q2'},
            ('q2', '0'): { 'q0', 'q2' },
            ('q2', '1'): { 'φ' },
            ('φ', '0'): { 'φ' },
            ('φ', '1'): { 'φ' }
        }
        expected_dfa_accept_states = [
            { 'q0', 'q2' },
            { 'q0', 'q1', 'q2' }
        ]

        self.assertEqual(
            sorted([sorted(list(s)) for s in result['dfa_states']]),
            sorted([sorted(list(s)) for s in expected_dfa_states])
        )
        self.assertEqual(result['dfa_transition_functions'], expected_dfa_transitions)
        self.assertEqual(result['dfa_start_states'], expected_dfa_start_states)
        self.assertEqual(result['dfa_accept_states'], expected_dfa_accept_states)

if __name__ == '__main__':
    unittest.main()
