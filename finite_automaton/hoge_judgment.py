from typing import List, Dict, Tuple
import string

class FiniteAutomaton:
    def __init__(self):
        # 状態
        self.states: List[str] = ['q1', 'q2', 'q3', 'q4', 'q5']

        # アルファベット
        self.alphabet_list: List[str] = list(string.ascii_lowercase[:26])

        # 遷移関数 (状態, 入力) -> 次の状態
        self.transition_function: Dict[Tuple[str, str], str] = {}

        # 遷移関数としては以上
        # ループの条件式で入力値に対して遷移関数が一致しない場合、q1に戻すようにする
        for alphabet in self.alphabet_list:
            if alphabet == 'h':
                self.transition_function[('q1', 'h')] = 'q2'
            elif alphabet == 'o':
                self.transition_function[('q2', 'o')] = 'q3'
            elif alphabet == 'g':
                self.transition_function[('q3', 'g')] = 'q4'
            elif alphabet == 'e':
                self.transition_function[('q4', 'e')] = 'q5'
            else:
                self.transition_function[('q5', alphabet)] = 'q5'

        # 開始状態
        self.start_state: str = 'q1'

        # 受理状態
        self.accept_states: List[str] = ['q5']

    def process(self, input_string: str) -> bool:
        current_state: str = self.start_state

        for char in input_string:
            state: Tuple[str, str] = (current_state, char)

            if (state in self.transition_function):
                current_state = self.transition_function[state]
            else:
                current_state = self.start_state

        return current_state in self.accept_states

automaton = FiniteAutomaton()

# テストケース
text1 = 'hoge'
text2 = 'hage'
text3 = 'hoga'
text4 = 'abchdefoghigjkle'
text5 = 'abchoagexyz'
text6 = 'abchaogexyz'
text7 = 'abchogexyz'

# 結果を確認
print(automaton.process(text1))  # True
print(automaton.process(text2))  # False
print(automaton.process(text3))  # False
print(automaton.process(text4))  # False
print(automaton.process(text5))  # False
print(automaton.process(text6))  # False
print(automaton.process(text7))  # True
