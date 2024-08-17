from typing import List, Dict, Tuple

# M = ({q1, q2}, {0, 1}, δ, q1, {q2})
# L(M) = { w | wは1でおわる }

class FiniteAutomaton:
    def __init__(self):
        # 状態
        self.states: List[str] = ['q1', 'q2']

        # アルファベット
        self.alphabet: List[int] = [0, 1]

        # 遷移関数 (状態, 入力) -> 次の状態
        self.transition_function: Dict[Tuple[str, int], str] = {
            ('q1', 0): 'q1',
            ('q1', 1): 'q2',
            ('q2', 0): 'q1',
            ('q2', 1): 'q2',
        }

        # 開始状態
        self.start_state: str = 'q1'

        # 受理状態
        self.accept_states: List[str] = ['q2']

    def process(self, input_string: str) -> bool:
        current_state: str = self.start_state

        for char in input_string:
            state: Tuple[str, int] = (current_state, int(char))
            if (state in self.transition_function):
                current_state = self.transition_function[state]
            else:
                print('入力に誤りがあります')
                return False

        # 受理状態に到達していれば True を返す
        return current_state in self.accept_states


automaton = FiniteAutomaton()

# テストケース
text1 = '0'
text2 = '1'
text3 = '01'
text4 = '00'
text5 = '010101'
text6 = '0101010'

# 結果を確認
print(automaton.process(text1))  # False を返す
print(automaton.process(text2))  # True を返す
print(automaton.process(text3))  # True を返す
print(automaton.process(text4))  # False を返す
print(automaton.process(text5))  # True を返す
print(automaton.process(text6))  # Flase を返す
